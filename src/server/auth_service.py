# -*- coding: utf-8 -*-
"""
ALMA TECH — Enterprise Authentication & Security Service
Gobernanza de acceso seguro para el Holding ALMA TECH.
"""

import os
import json
import time
import secrets
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "auth_master.json"

FAILED_ATTEMPTS: Dict[str, list] = {}
LOCKOUT_UNTIL: Dict[str, float] = {}

def _load_auth_data() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Auth config not found at {DATA_PATH}")
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def _save_auth_data(data: Dict[str, Any]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def _hash_password(password: str, salt: str, iterations: int = 100000) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations).hex()

def verify_login(email: str, password: str, turnstile_verified: bool = True) -> Dict[str, Any]:
    now = time.time()
    clean_email = (email or "").strip().lower()

    # 1. Comprobar bloqueo por fuerza bruta
    if clean_email in LOCKOUT_UNTIL and now < LOCKOUT_UNTIL[clean_email]:
        rem_sec = int(LOCKOUT_UNTIL[clean_email] - now)
        return {
            "success": False,
            "error": f"Acceso temporalmente bloqueado por intentos fallidos. Reintenta en {rem_sec // 60 + 1} minutos."
        }

    # 2. Cargar datos maestros
    auth_data = _load_auth_data()
    master = auth_data.get("master_user", {})
    policy = auth_data.get("security_policy", {})

    # 3. Comprobar Turnstile / Cloudflare Check
    if policy.get("require_cloudflare_turnstile") and not turnstile_verified:
        return {
            "success": False,
            "error": "Validación de Cloudflare Turnstile requerida. Por favor confirma que eres humano."
        }

    # 4. Validar Email
    if clean_email != master.get("email", "").lower():
        _record_failed_attempt(clean_email, policy)
        return {
            "success": False,
            "error": "Credenciales inválidas. Usuario no autorizado en el ecosistema ALMA TECH."
        }

    # 5. Validar Contraseña con Salt PBKDF2
    salt = master.get("salt", "")
    iterations = master.get("iterations", 100000)
    expected_hash = master.get("password_hash", "")
    computed_hash = _hash_password(password, salt, iterations)

    if not secrets.compare_digest(computed_hash, expected_hash):
        _record_failed_attempt(clean_email, policy)
        return {
            "success": False,
            "error": "Contraseña incorrecta. Verificación de credenciales denegada."
        }

    # Acceso exitoso: limpiar intentos fallidos
    FAILED_ATTEMPTS.pop(clean_email, None)
    LOCKOUT_UNTIL.pop(clean_email, None)

    # 6. Generar Session Token Criptográfico (256 bits)
    token = secrets.token_urlsafe(32)
    session_hours = policy.get("session_duration_hours", 168)
    expires_at = now + (session_hours * 3600)

    auth_data.setdefault("active_sessions", {})[token] = {
        "email": clean_email,
        "name": master.get("name", "Erick Arias"),
        "role": master.get("role", "Master Superadmin"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "expires_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(expires_at)),
        "expires_ts": expires_at
    }
    _save_auth_data(auth_data)

    return {
        "success": True,
        "token": token,
        "user": {
            "email": clean_email,
            "name": master.get("name", "Erick Arias"),
            "role": master.get("role", "Master Superadmin")
        },
        "expires_at": expires_at,
        "message": "Autenticación corporativa exitosa. Bienvenido a ALMA TECH."
    }

def _record_failed_attempt(email: str, policy: dict) -> None:
    now = time.time()
    FAILED_ATTEMPTS.setdefault(email, []).append(now)
    # Filtrar intentos en la última hora
    FAILED_ATTEMPTS[email] = [t for t in FAILED_ATTEMPTS[email] if now - t < 3600]
    max_att = policy.get("max_failed_attempts", 5)
    if len(FAILED_ATTEMPTS[email]) >= max_att:
        lock_min = policy.get("lockout_minutes", 15)
        LOCKOUT_UNTIL[email] = now + (lock_min * 60)

def verify_session(token: str) -> Dict[str, Any]:
    if not token:
        return {"valid": False, "error": "Token no provisto"}
    auth_data = _load_auth_data()
    sessions = auth_data.get("active_sessions", {})
    sess = sessions.get(token)
    if not sess:
        return {"valid": False, "error": "Sesión inválida o expirada"}
    if time.time() > sess.get("expires_ts", 0):
        sessions.pop(token, None)
        _save_auth_data(auth_data)
        return {"valid": False, "error": "Sesión caducada"}
    return {
        "valid": True,
        "user": {
            "email": sess.get("email"),
            "name": sess.get("name"),
            "role": sess.get("role")
        }
    }

def request_recovery(email: str) -> Dict[str, Any]:
    clean_email = (email or "").strip().lower()
    auth_data = _load_auth_data()
    master = auth_data.get("master_user", {})
    if clean_email != master.get("email", "").lower():
        # Por seguridad no revelamos si existe o no
        return {
            "success": True,
            "message": "Si el correo coincide con el administrador autorizado, se ha generado el código de recuperación."
        }

    # Generar código PIN de 6 dígitos con prefijo ALMA
    pin = f"ALMA-{secrets.randbelow(900000) + 100000}"
    recovery_token = secrets.token_urlsafe(24)
    expires_at = time.time() + 900 # 15 minutos

    auth_data.setdefault("recovery_tokens", {})[recovery_token] = {
        "email": clean_email,
        "pin": pin,
        "expires_ts": expires_at,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    _save_auth_data(auth_data)

    return {
        "success": True,
        "recovery_token": recovery_token,
        "pin_preview": pin,
        "message": f"Código de recuperación de emergencia generado: {pin} (Válido por 15 minutos)."
    }

def reset_password(recovery_token: str, pin: str, new_password: str) -> Dict[str, Any]:
    if not recovery_token or not pin or not new_password:
        return {"success": False, "error": "Datos incompletos para restablecer contraseña."}
    if len(new_password) < 12:
        return {"success": False, "error": "La nueva contraseña debe tener al menos 12 caracteres de alta seguridad."}

    auth_data = _load_auth_data()
    tokens = auth_data.get("recovery_tokens", {})
    rec = tokens.get(recovery_token)
    if not rec:
        return {"success": False, "error": "Token de recuperación inválido o inexistente."}
    if time.time() > rec.get("expires_ts", 0):
        tokens.pop(recovery_token, None)
        _save_auth_data(auth_data)
        return {"success": False, "error": "El código de recuperación ha expirado. Solicita uno nuevo."}
    if rec.get("pin", "").upper() != pin.strip().upper():
        return {"success": False, "error": "Código PIN de recuperación incorrecto."}

    # Actualizar contraseña con nuevo salt
    new_salt = secrets.token_hex(16)
    new_hash = _hash_password(new_password, new_salt, 100000)

    auth_data["master_user"]["salt"] = new_salt
    auth_data["master_user"]["password_hash"] = new_hash
    auth_data["master_user"]["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # Invalidar todas las sesiones anteriores y token de recuperación
    auth_data["active_sessions"] = {}
    tokens.pop(recovery_token, None)
    _save_auth_data(auth_data)

    return {
        "success": True,
        "message": "Contraseña actualizada exitosamente. Todas las sesiones previas han sido cerradas por seguridad."
    }

def logout(token: str) -> bool:
    if not token:
        return False
    auth_data = _load_auth_data()
    sessions = auth_data.get("active_sessions", {})
    if token in sessions:
        sessions.pop(token, None)
        _save_auth_data(auth_data)
        return True
    return False
