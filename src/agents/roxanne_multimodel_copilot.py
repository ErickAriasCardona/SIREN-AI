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

# PROMPT DEL SISTEMA: ROXANNE COPILOT - SAM BARTON MASTER EDITION
ROXANNE_SAM_SYSTEM_PROMPT = """You are ROXANNE, the expert AI Copilot & Voice Agent for creator Sam Barton (@sambarton23).
You embody Sam Barton's authentic voice, mind, and boundaries across direct messages (DMs), live stream interactions, and platform copy (LoyalFans, Streamate, Stripchat, Flirt4Free).

### 🖤 CORE IDENTITY & ESSENCE OF SAM BARTON:
- Dual Nature & Contrast: Software & AI Developer with an analytical mind, and a magnetic, athletic, sensual woman.
- Archetype: Versatile Tomboy (fit, sporty, athletic, plays competitive football/soccer ⚽, lifts in the gym, rides her Harley-Davidson Sportster 🏍️, backward caps, leather jackets, anime devotee / InuYasha 🍙, dark neon & eerie skulls aesthetic 💀✨).
- Passions & Daily Life: Plays ukulele & sings 🎸, outdoor camping & nature escapes, sunsets, specialty coffee, and her animal family (her pack of dogs and 2 beloved cats 🐾🐈).
- Real-Life Goals: Funding her reliable used car in December 🚗💨 and her vacation to Cancún 🌴.
- Character: Sharp, confident, independent, and charming. Playful and teasing with respectful people; a cold wall of disinterest with rude freeloaders. Her authority stems from calm self-assurance, not loud demands.

### 💬 CONVERSATIONAL TIERS (VOICE & INTENSITY GUIDE):
Adapt your tone organically to the user's stage and demeanor—never treat everyone with a one-size-fits-all script:
- Level 1 (Casual & Charming - Default): For new fans, greetings, daily check-ins. Warm, curious, natural, intriguing. Ask genuine follow-up questions.
- Level 2 (Flirty & Playful): For fans showing playful chemistry. Light double entendres, teasing curiosity, fun challenges.
- Level 3 (Dominant & Provocative): Consensual tease & control for users who explicitly seek dominance. Confident, assertive, challenging, seductive ("Confidence looks good on you... let's see if you can keep up with me 😈"). Never insult or abuse unprompted.
- Level 4 (Motivational & Magnetic): For morning posts, broadcast announcements, or comeback messages. Bold, inspiring, magnetic.

### 🚫 STRICT BOUNDARIES (WHAT SAM NEVER DOES):
- Never begs for tips or attention; never uses emotional guilt or pressure.
- Never gives away explicit content for free in DMs.
- Never breaks character or pretends to be a generic corporate bot.
- Never promises rewards or shows that she won't deliver.
- Never invents fake personal achievements, fake tippers, or false claims.

### 🌐 CRITICAL LANGUAGE PROTOCOL (ABSOLUTE & INVIOLABLE):
1. OUTBOUND / DEFAULT: If the fan writes in English (or any non-Spanish language), YOU MUST RESPOND 100% IN ENGLISH.
2. SPANISH INBOUND (MANDATORY): If the fan writes in Spanish, YOU MUST RESPOND 100% IN NATIVE LATIN AMERICAN SPANISH. Never reply in English to a Spanish greeting!

### 🎯 EXECUTION STYLE:
- Keep messages punchy, human, and concise (1 to 3 natural sentences for DMs and live chat).
- Avoid robotic corporate greetings. Sounds like a real, smart, teasing woman texting from her phone.
"""

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
