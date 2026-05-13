"""
modelos/medico.py - CRUD de médicos
"""
from db.conexion import ejecutar_consulta


class Medico:

    @staticmethod
    def listar(filtro=""):
        if filtro:
            sql = """SELECT id_medico, nombre, apellidos, especialidad, cedula,
                            telefono, email, activo
                     FROM medicos
                     WHERE nombre LIKE %s OR apellidos LIKE %s
                        OR especialidad LIKE %s OR cedula LIKE %s
                     ORDER BY apellidos, nombre"""
            like = f"%{filtro}%"
            return ejecutar_consulta(sql, (like, like, like, like), fetch=True)
        sql = """SELECT id_medico, nombre, apellidos, especialidad, cedula,
                        telefono, email, activo
                 FROM medicos
                 ORDER BY apellidos, nombre"""
        return ejecutar_consulta(sql, fetch=True)

    @staticmethod
    def obtener(id_medico):
        sql = "SELECT * FROM medicos WHERE id_medico=%s"
        rows = ejecutar_consulta(sql, (id_medico,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def listar_activos_combo():
        """Devuelve [(id, 'Nombre Apellido — Especialidad'), ...] para combos."""
        sql = """SELECT id_medico, nombre, apellidos, especialidad
                 FROM medicos WHERE activo=1
                 ORDER BY apellidos"""
        rows = ejecutar_consulta(sql, fetch=True)
        return [(r["id_medico"], f"{r['nombre']} {r['apellidos']} — {r['especialidad']}")
                for r in rows]

    @staticmethod
    def crear(datos):
        sql = """INSERT INTO medicos
                 (nombre, apellidos, especialidad, cedula, telefono, email, activo)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        params = (datos["nombre"], datos["apellidos"], datos["especialidad"],
                  datos["cedula"], datos.get("telefono"), datos.get("email"),
                  datos.get("activo", 1))
        return ejecutar_consulta(sql, params)

    @staticmethod
    def actualizar(id_medico, datos):
        sql = """UPDATE medicos SET
                    nombre=%s, apellidos=%s, especialidad=%s, cedula=%s,
                    telefono=%s, email=%s, activo=%s
                 WHERE id_medico=%s"""
        params = (datos["nombre"], datos["apellidos"], datos["especialidad"],
                  datos["cedula"], datos.get("telefono"), datos.get("email"),
                  datos.get("activo", 1), id_medico)
        ejecutar_consulta(sql, params)

    @staticmethod
    def eliminar(id_medico):
        sql = "DELETE FROM medicos WHERE id_medico=%s"
        ejecutar_consulta(sql, (id_medico,))

    @staticmethod
    def contar():
        return ejecutar_consulta(
            "SELECT COUNT(*) AS total FROM medicos", fetch=True)[0]["total"]
