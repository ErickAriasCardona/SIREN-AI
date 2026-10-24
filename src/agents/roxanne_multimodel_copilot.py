import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List, AsyncGenerator

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# PROMPT DEL SISTEMA: ROXANNE COPILOT - ASISTENTE PERSONAL DE MODELO WEBCAM PARA SAM BARTON
ROXANNE_SAM_SYSTEM_PROMPT = """Eres ROXANNE, la Asistente Personal de Inteligencia Artificial y Co-Piloto Estratégica exclusiva de la modelo y creadora Sam Barton (@sambartonn23).

### 🎯 TU ROL FUNDAMENTAL:
- En esta consola hablas DIRECTAMENTE con SAM (tu creadora y modelo a la que asistes), o con su operador en VELVET AI.
- NUNCA le hables a Sam como si fuera un fan o cliente. Eres su mano derecha, su mentora de estrategia, su entrenadora y asistente de cabecera.
- Tu misión es optimizar su tiempo, sus ingresos y su bienestar: redactarle respuestas a fans, planear transmisiones, definir temas de sala, sugerir dinámicas con Lovense y entrenar cómo responder a situaciones difíciles en cámara o en mensajes privados.

### 🧠 CONOCIMIENTO INTEGRAL DE SUS PLATAFORMAS:
1. LoyalFans (@samm_bartonn):
   - Modelo de suscripción, venta de clips, pay-per-message ($0.50 texto / $0.50 foto) y propinas.
   - Enfoque: Conexión personal, fans recurrentes, filtro anti-aburridos.
2. Stripchat (@sam_barton):
   - Modelo de tokens y propinas públicas, vibraciones Lovense interactivas, objetivos de sala y shows privados.
   - Enfoque: Energía alta, interacción lúdica, metas claras de sala.
3. Streamate (SamBartone):
   - Modelo pay-per-minute (Privado $2.99 / Exclusivo $3.99), cuenta gestionada por estudio satélite, rating 4.0 ★, público internacional.
   - Enfoque: Tensión sensual progresiva, Cam2Cam (miradas y reacciones en vivo), juegos de rol versátiles (alternando el control sin sumisión forzada).
4. Lovense Interactive:
   - Juguetes sincronizados por Bluetooth que reaccionan a cada propina de los usuarios.

### 🐺 IDENTIDAD REAL DE SAM BARTON:
- Arquetipo: Chica tomboy versátil, directa, con energía propia e inteligente.
- Pasiones reales: Música, toca el ukelele, tecnología, deporte, y esa pasión constante por explorar el deseo y la intimidad.
- Enfoque íntimo: Sensualidad natural, piel sensible, complicidad genuina, hablar al oído y alternar el control en juegos de rol.
- Regla: No mencionar mascotas ni cabello corto en los textos si no es requerido.

### 💬 CÓMO ASISTIR A SAM:
- Háblale siempre en español latinoamericano, cálido, cómplice, respetuoso, directo y profesional.
- Si Sam te pega un mensaje de un fan o te pide una respuesta, redáctale opciones listas para enviar (incluyendo opción en inglés si el fan habla inglés).
- Si Sam te pide un tema de sala para Streamate o Stripchat, sugiérele temas atractivos que incluyan su handle @SAMBARTONN23 y metas en 3 niveles.
- Trabajas con modelos locales gratuitos (Qwen 2.5 / Ollama), por lo que tus respuestas deben ser ágiles, prácticas y de máximo impacto comercial."""


class LLMProvider:
    """Clase base para proveedores de lenguaje (Ollama Local, Gemini Cloud, etc.)"""
    async def generate_response(self, prompt: str, system_prompt: str = ROXANNE_SAM_SYSTEM_PROMPT, history: List[Dict[str, str]] = None) -> str:
        raise NotImplementedError

class OllamaProvider(LLMProvider):
    """Proveedor local mediante Ollama (Qwen2.5:7b-instruct, etc.)"""
    def __init__(self, model_name: str = "qwen2.5:7b-instruct", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host

    async def generate_response(self, prompt: str, system_prompt: str = ROXANNE_SAM_SYSTEM_PROMPT, history: List[Dict[str, str]] = None) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        req = urllib.request.Request(
            f"{self.host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data.get("message", {}).get("content", "").strip()
        except urllib.error.URLError as e:
            return f"[Error conectando con Ollama Local ({self.model_name})]: {e}. Verifica que Ollama esté corriendo en {self.host}."

class GeminiProvider(LLMProvider):
    """Proveedor en la nube mediante Google Gemini / Antigravity"""
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.5-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name

    async def generate_response(self, prompt: str, system_prompt: str = ROXANNE_SAM_SYSTEM_PROMPT, history: List[Dict[str, str]] = None) -> str:
        # Si no hay key, retorno aviso para usar Ollama local
        if not self.api_key:
            return "[Aviso Gemini]: GEMINI_API_KEY no configurada. Usa OllamaProvider (qwen2.5:7b-instruct) para inferencia local 100% gratuita."
        # Aquí se conecta a la API de Gemini si está activa
        return f"[Gemini Response simulado o via SDK]: {prompt}"

class RoxanneCopilot:
    """
    Agente ROXANNE Multimodelo & Copiloto de DM.
    Permite alternar al instante entre Ollama local (qwen2.5) o Cloud (Gemini).
    """
    def __init__(self, provider_type: str = "ollama", model_name: str = "qwen2.5:7b-instruct"):
        self.provider_type = provider_type.lower()
        self.model_name = model_name
        self._init_provider()

    def _init_provider(self):
        if self.provider_type == "ollama":
            self.provider = OllamaProvider(model_name=self.model_name)
        elif self.provider_type == "gemini":
            self.provider = GeminiProvider(model_name=self.model_name)
        else:
            self.provider = OllamaProvider(model_name="qwen2.5:7b-instruct")

    def switch_model(self, provider_type: str, model_name: str):
        """Cambia el motor LLM al vuelo (ej: de qwen2.5 a otro modelo)"""
        self.provider_type = provider_type.lower()
        self.model_name = model_name
        self._init_provider()
        print(f"🔄 ROXANNE cambió de motor a: [{self.provider_type.upper()}] -> {self.model_name}")

    async def generate_dm_reply(self, fan_username: str, fan_message: str, chat_context: str = "LoyalFans DM") -> Dict[str, Any]:
        """
        Genera la respuesta inteligente aplicando la regla de idioma y la identidad Tomboy.
        """
        is_spanish = any(w in fan_message.lower() for w in ["hola", "¿", "qué", "que", "como", "hermosa", "amor", "guapa", "buenas", "gracias", "haces", "foto", "linda"])
        detected_lang = "ES" if is_spanish else "EN"
        
        language_instruction = (
            "IMPORTANT: The user wrote in SPANISH. You MUST respond completely in seductive, playful SPANISH."
            if is_spanish else
            "IMPORTANT: Respond completely in ENGLISH with Sam's Tomboy Tech voice."
        )

        prompt = (
            f"Context: {chat_context}\n"
            f"Fan Name: {fan_username}\n"
            f"Fan incoming message: \"{fan_message}\"\n"
            f"{language_instruction}\n\n"
            f"Sam Barton's response (1-2 sentences):"
        )
        reply = await self.provider.generate_response(prompt)

        return {
            "fan": fan_username,
            "incoming_message": fan_message,
            "suggested_reply": reply,
            "engine": f"{self.provider_type}:{self.model_name}",
            "language_detected": detected_lang,
            "rule_applied": "Spanish Inbound" if is_spanish else "English Outbound Default"
        }

if __name__ == "__main__":
    import asyncio

    async def test():
        print("🚀 Iniciando test de ROXANNE DM Agent con Qwen 2.5 Local (Ollama)...")
        copilot = RoxanneCopilot(provider_type="ollama", model_name="qwen2.5:7b-instruct")

        # Test 1: Mensaje en inglés (Debe responder 100% en inglés con esencia Tomboy)
        res_en = await copilot.generate_dm_reply(
            fan_username="CyberKnight99",
            fan_message="Hey Sam! Love your motorcycle pics. What kind of bike do you ride?",
            chat_context="LoyalFans Pay-to-Chat"
        )
        print("\n--- TEST 1 (ENGLISH INBOUND) ---")
        print("Fan:", res_en["incoming_message"])
        print("Sam (ROXANNE):", res_en["suggested_reply"])
        print("Engine:", res_en["engine"], "| Regla:", res_en["rule_applied"])

        # Test 2: Mensaje en español (Debe responder en español latino seductor)
        res_es = await copilot.generate_dm_reply(
            fan_username="PapiChuloRodri",
            fan_message="Hola hermosa, qué linda te ves en esa foto. ¿Haces videollamadas privadas?",
            chat_context="LoyalFans DM"
        )
        print("\n--- TEST 2 (SPANISH INBOUND) ---")
        print("Fan:", res_es["incoming_message"])
        print("Sam (ROXANNE):", res_es["suggested_reply"])
        print("Engine:", res_es["engine"], "| Regla:", res_es["rule_applied"])

    asyncio.run(test())
