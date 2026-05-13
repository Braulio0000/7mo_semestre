"""
controladores/auth.py - Sesión actual del sistema
"""
from modelos.usuario import Usuario


class Sesion:
    usuario_actual = None  # se asigna tras login exitoso

    @classmethod
    def iniciar(cls, usuario, password):
        u = Usuario.autenticar(usuario, password)
        if u:
            cls.usuario_actual = u
            return u
        return None

    @classmethod
    def cerrar(cls):
        cls.usuario_actual = None

    @classmethod
    def es_admin(cls):
        return cls.usuario_actual and cls.usuario_actual.rol == "Administrador"

    @classmethod
    def es_recepcionista(cls):
        return cls.usuario_actual and cls.usuario_actual.rol == "Recepcionista"
