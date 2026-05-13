"""
utils/helpers.py - Utilidades comunes
=====================================
"""
import hashlib
import re
from datetime import datetime


def hash_password(plain: str) -> str:
    """SHA-256 hex (suficiente para fines académicos)."""
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


def es_email_valido(email: str) -> bool:
    if not email:
        return True  # email es opcional en algunos casos
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None


def es_telefono_valido(tel: str) -> bool:
    if not tel:
        return True
    # Permite espacios, guiones, paréntesis y signo +; valida solo los dígitos.
    solo_digitos = re.sub(r"[\s\-\(\)\+]", "", tel)
    return bool(re.match(r"^\d{7,15}$", solo_digitos))


def parse_fecha(texto: str, fmt: str = None) -> datetime:
    """Acepta varios formatos: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, YYYY/MM/DD.
    Lanza ValueError si ninguno parsea."""
    texto = texto.strip()
    if fmt:
        return datetime.strptime(texto, fmt)
    formatos = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d")
    for f in formatos:
        try:
            return datetime.strptime(texto, f)
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha inválido: {texto}")


def parse_fecha_hora(texto: str) -> datetime:
    """Acepta varios formatos:
       YYYY-MM-DD HH:MM[:SS]  ·  DD/MM/YYYY HH:MM[:SS]
       Si solo se da la fecha (sin hora), usa 09:00 por defecto.
    """
    texto = texto.strip()
    formatos = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d",        # solo fecha → se asume 09:00
        "%d/%m/%Y",
    )
    for f in formatos:
        try:
            dt = datetime.strptime(texto, f)
            if " " not in texto and ":" not in texto:
                dt = dt.replace(hour=9, minute=0)
            return dt
        except ValueError:
            continue
    raise ValueError(
        f"Formato de fecha/hora inválido: «{texto}». "
        "Usa por ejemplo: 2026-05-15 14:30  ó  15/05/2026 14:30."
    )


def fmt_fecha(dt) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d")


def fmt_fecha_hora(dt) -> str:
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M")
