"""
modelos/expediente.py - CRUD de expedientes médicos
"""
from db.conexion import ejecutar_consulta


class Expediente:

    @staticmethod
    def listar(filtro="", desde=None, hasta=None):
        sql = """SELECT e.id_expediente, e.id_cita, e.fecha_alta,
                        e.diagnostico, e.tratamiento, e.observaciones,
                        CONCAT(p.nombre,' ',p.apellidos) AS paciente,
                        CONCAT(m.nombre,' ',m.apellidos) AS medico,
                        m.especialidad,
                        c.fecha_hora AS fecha_cita
                 FROM expedientes e
                 JOIN citas c     ON c.id_cita     = e.id_cita
                 JOIN pacientes p ON p.id_paciente = c.id_paciente
                 JOIN medicos   m ON m.id_medico   = c.id_medico
                 WHERE 1=1 """
        params = []
        if filtro:
            sql += """ AND (p.nombre LIKE %s OR p.apellidos LIKE %s
                       OR m.nombre LIKE %s OR e.diagnostico LIKE %s) """
            like = f"%{filtro}%"
            params.extend([like, like, like, like])
        if desde:
            sql += " AND DATE(e.fecha_alta) >= %s "
            params.append(desde)
        if hasta:
            sql += " AND DATE(e.fecha_alta) <= %s "
            params.append(hasta)
        sql += " ORDER BY e.fecha_alta DESC"
        return ejecutar_consulta(sql, tuple(params), fetch=True)

    @staticmethod
    def obtener(id_expediente):
        sql = "SELECT * FROM expedientes WHERE id_expediente=%s"
        rows = ejecutar_consulta(sql, (id_expediente,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def crear(datos):
        sql = """INSERT INTO expedientes
                 (id_cita, diagnostico, tratamiento, observaciones)
                 VALUES (%s,%s,%s,%s)"""
        params = (datos["id_cita"], datos["diagnostico"],
                  datos.get("tratamiento"), datos.get("observaciones"))
        return ejecutar_consulta(sql, params)

    @staticmethod
    def actualizar(id_expediente, datos):
        sql = """UPDATE expedientes SET
                    diagnostico=%s, tratamiento=%s, observaciones=%s
                 WHERE id_expediente=%s"""
        params = (datos["diagnostico"], datos.get("tratamiento"),
                  datos.get("observaciones"), id_expediente)
        ejecutar_consulta(sql, params)

    @staticmethod
    def eliminar(id_expediente):
        sql = "DELETE FROM expedientes WHERE id_expediente=%s"
        ejecutar_consulta(sql, (id_expediente,))

    @staticmethod
    def contar():
        return ejecutar_consulta(
            "SELECT COUNT(*) AS total FROM expedientes", fetch=True)[0]["total"]
