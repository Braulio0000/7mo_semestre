"""
modelos/usuario.py - CRUD de usuarios y autenticación
"""
from db.conexion import ejecutar_consulta
from utils.helpers import hash_password


class Usuario:
    def __init__(self, id_usuario=None, usuario="", nombre="", rol="", activo=1):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.nombre = nombre
        self.rol = rol
        self.activo = activo

    @classmethod
    def autenticar(cls, usuario, password):
        """Devuelve un Usuario si las credenciales son válidas, None si no."""
        h = hash_password(password)
        sql = """SELECT id_usuario, usuario, nombre, rol, activo
                 FROM usuarios
                 WHERE usuario=%s AND password=%s AND activo=1"""
        rows = ejecutar_consulta(sql, (usuario, h), fetch=True)
        if not rows:
            return None
        r = rows[0]
        return cls(r["id_usuario"], r["usuario"], r["nombre"], r["rol"], r["activo"])

    @classmethod
    def listar(cls):
        sql = "SELECT id_usuario, usuario, nombre, rol, activo FROM usuarios ORDER BY id_usuario"
        return ejecutar_consulta(sql, fetch=True)
