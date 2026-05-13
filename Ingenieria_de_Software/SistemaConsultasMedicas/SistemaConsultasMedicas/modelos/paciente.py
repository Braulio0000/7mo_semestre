"""
modelos/paciente.py - CRUD de pacientes
"""
from db.conexion import ejecutar_consulta


class Paciente:

    @staticmethod
    def listar(filtro=""):
        if filtro:
            sql = """SELECT id_paciente, nombre, apellidos, fecha_nac, sexo,
                            telefono, email, direccion
                     FROM pacientes
                     WHERE nombre LIKE %s OR apellidos LIKE %s OR email LIKE %s
                     ORDER BY apellidos, nombre"""
            like = f"%{filtro}%"
            return ejecutar_consulta(sql, (like, like, like), fetch=True)
        sql = """SELECT id_paciente, nombre, apellidos, fecha_nac, sexo,
                        telefono, email, direccion
                 FROM pacientes
                 ORDER BY apellidos, nombre"""
        return ejecutar_consulta(sql, fetch=True)

    @staticmethod
    def obtener(id_paciente):
        sql = "SELECT * FROM pacientes WHERE id_paciente=%s"
        rows = ejecutar_consulta(sql, (id_paciente,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def crear(datos):
        sql = """INSERT INTO pacientes
                 (nombre, apellidos, fecha_nac, sexo, telefono, email, direccion)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        params = (datos["nombre"], datos["apellidos"], datos["fecha_nac"],
                  datos["sexo"], datos.get("telefono"), datos.get("email"),
                  datos.get("direccion"))
        return ejecutar_consulta(sql, params)

    @staticmethod
    def actualizar(id_paciente, datos):
        sql = """UPDATE pacientes SET
                    nombre=%s, apellidos=%s, fecha_nac=%s, sexo=%s,
                    telefono=%s, email=%s, direccion=%s
                 WHERE id_paciente=%s"""
        params = (datos["nombre"], datos["apellidos"], datos["fecha_nac"],
                  datos["sexo"], datos.get("telefono"), datos.get("email"),
                  datos.get("direccion"), id_paciente)
        ejecutar_consulta(sql, params)

    @staticmethod
    def eliminar(id_paciente):
        sql = "DELETE FROM pacientes WHERE id_paciente=%s"
        ejecutar_consulta(sql, (id_paciente,))

    @staticmethod
    def contar():
        sql = "SELECT COUNT(*) AS total FROM pacientes"
        return ejecutar_consulta(sql, fetch=True)[0]["total"]
