"""
config.py - Configuración global del sistema
============================================
Modifica las credenciales para apuntar a tu instancia local de MySQL.
"""

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "",            # <-- ajusta tu contraseña de MySQL aquí
    "database": "consultas_medicas",
    "charset":  "utf8mb4",
}

APP_NAME    = "Sistema de Gestión de Consultas Médicas"
APP_VERSION = "1.0"
APP_AUTHOR  = "Braulio Yael Carranza Zamora"
APP_YEAR    = 2026
