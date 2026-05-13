"""
db/conexion.py - Capa de acceso al motor MySQL
==============================================
Patrón singleton ligero: una sola conexión activa por proceso.
"""
import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


class Conexion:
    _instancia = None

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.conn.autocommit = False
        except Error as e:
            raise RuntimeError(
                f"No se pudo conectar a MySQL.\n\nDetalle: {e}\n\n"
                "Verifica que:\n"
                " - El servidor MySQL esté en ejecución.\n"
                " - Las credenciales en config.py sean correctas.\n"
                " - La base 'consultas_medicas' exista (corre db/schema.sql)."
            )

    @classmethod
    def get(cls):
        """Obtiene la instancia singleton, reconectando si fue cerrada."""
        if cls._instancia is None or not cls._instancia.conn.is_connected():
            cls._instancia = Conexion()
        return cls._instancia

    def cursor(self, dictionary=True):
        return self.conn.cursor(dictionary=dictionary)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def cerrar(self):
        try:
            self.conn.close()
        except Exception:
            pass


def ejecutar_consulta(sql, params=None, fetch=False):
    """Helper genérico para SELECTs (fetch=True) o DML (fetch=False)."""
    cn = Conexion.get()
    cur = cn.cursor()
    try:
        cur.execute(sql, params or ())
        if fetch:
            return cur.fetchall()
        cn.commit()
        return cur.lastrowid
    except Error as e:
        cn.rollback()
        raise
    finally:
        cur.close()
