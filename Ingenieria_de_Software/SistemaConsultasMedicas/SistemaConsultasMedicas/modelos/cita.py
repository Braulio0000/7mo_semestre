"""
modelos/cita.py - CRUD de citas
"""
from db.conexion import ejecutar_consulta


ESTADOS = ("Pendiente", "Confirmada", "Atendida", "Cancelada")


class Cita:

    @staticmethod
    def listar(filtro="", desde=None, hasta=None, estado=None):
        sql = """SELECT c.id_cita, c.fecha_hora, c.estado, c.motivo,
                        c.id_paciente, c.id_medico,
                        CONCAT(p.nombre,' ',p.apellidos) AS paciente,
                        CONCAT(m.nombre,' ',m.apellidos) AS medico,
                        m.especialidad
                 FROM citas c
                 JOIN pacientes p ON p.id_paciente = c.id_paciente
                 JOIN medicos   m ON m.id_medico   = c.id_medico
                 WHERE 1=1 """
        params = []
        if filtro:
            sql += """ AND (p.nombre LIKE %s OR p.apellidos LIKE %s
                        OR m.nombre LIKE %s OR m.apellidos LIKE %s
                        OR c.motivo LIKE %s) """
            like = f"%{filtro}%"
            params.extend([like, like, like, like, like])
        if desde:
            sql += " AND DATE(c.fecha_hora) >= %s "
            params.append(desde)
        if hasta:
            sql += " AND DATE(c.fecha_hora) <= %s "
            params.append(hasta)
        if estado and estado != "Todos":
            sql += " AND c.estado = %s "
            params.append(estado)
        sql += " ORDER BY c.fecha_hora DESC"
        return ejecutar_consulta(sql, tuple(params), fetch=True)

    @staticmethod
    def obtener(id_cita):
        sql = "SELECT * FROM citas WHERE id_cita=%s"
        rows = ejecutar_consulta(sql, (id_cita,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def crear(datos):
        sql = """INSERT INTO citas (fecha_hora, estado, motivo, id_paciente, id_medico)
                 VALUES (%s,%s,%s,%s,%s)"""
        params = (datos["fecha_hora"], datos.get("estado", "Pendiente"),
                  datos.get("motivo"), datos["id_paciente"], datos["id_medico"])
        return ejecutar_consulta(sql, params)

    @staticmethod
    def actualizar(id_cita, datos):
        sql = """UPDATE citas SET
                    fecha_hora=%s, estado=%s, motivo=%s,
                    id_paciente=%s, id_medico=%s
                 WHERE id_cita=%s"""
        params = (datos["fecha_hora"], datos["estado"], datos.get("motivo"),
                  datos["id_paciente"], datos["id_medico"], id_cita)
        ejecutar_consulta(sql, params)

    @staticmethod
    def eliminar(id_cita):
        sql = "DELETE FROM citas WHERE id_cita=%s"
        ejecutar_consulta(sql, (id_cita,))

    @staticmethod
    def contar_por_estado():
        sql = "SELECT estado, COUNT(*) AS n FROM citas GROUP BY estado"
        return ejecutar_consulta(sql, fetch=True)

    @staticmethod
    def listar_atendidas_sin_expediente():
        """Citas que aún no tienen expediente (cualquier estado).
        Antes filtraba solo 'Atendida'; ahora muestra todas las que estén
        libres para que el usuario siempre tenga opciones que escoger."""
        sql = """SELECT c.id_cita, c.fecha_hora, c.estado,
                        CONCAT(p.nombre,' ',p.apellidos) AS paciente,
                        CONCAT(m.nombre,' ',m.apellidos) AS medico
                 FROM citas c
                 JOIN pacientes p ON p.id_paciente = c.id_paciente
                 JOIN medicos   m ON m.id_medico   = c.id_medico
                 LEFT JOIN expedientes e ON e.id_cita = c.id_cita
                 WHERE e.id_expediente IS NULL
                 ORDER BY c.fecha_hora DESC"""
        return ejecutar_consulta(sql, fetch=True)
