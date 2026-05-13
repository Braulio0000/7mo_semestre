# Sistema de Gestión de Consultas Médicas

Aplicación de escritorio en Python + Tkinter con base de datos MySQL 8.0.
Implementa CRUD completo para Pacientes, Médicos, Citas y Expedientes,
con autenticación por roles (Administrador / Recepcionista) y exportación
de reportes a PDF y Excel.

**Autor:** Braulio Yael Carranza Zamora
**Materia:** Ingeniería de Software

---

## 1. Requisitos

- Python 3.10 o superior
- MySQL 8.0 (o XAMPP / MariaDB compatible)
- Sistema operativo: Windows / macOS / Linux

## 2. Instalación

```bash
# 1) Clonar/descomprimir el proyecto y entrar a la carpeta
cd SistemaConsultasMedicas

# 2) Instalar las dependencias de Python
pip install -r requirements.txt

# 3) Crear la base de datos en MySQL
mysql -u root -p < db/schema.sql
```

Edita `config.py` y coloca tu contraseña de MySQL en `DB_CONFIG["password"]`.

## 3. Ejecución

```bash
python main.py
```

## 4. Credenciales por defecto

| Usuario | Contraseña | Rol            |
|---------|------------|----------------|
| admin   | admin123   | Administrador  |
| recep   | recep123   | Recepcionista  |

El Administrador tiene acceso a los 5 módulos (Pacientes, Médicos, Citas,
Expedientes, Reportes). La Recepcionista solo puede gestionar Pacientes y
Citas.

## 5. Estructura del proyecto

```
SistemaConsultasMedicas/
├── main.py                  # Punto de entrada
├── config.py                # Configuración (DB, app)
├── requirements.txt
├── README.md
├── db/
│   ├── conexion.py          # Conexión MySQL (singleton)
│   └── schema.sql           # DDL + datos de prueba
├── modelos/                 # Capa de Modelos (acceso a datos)
│   ├── usuario.py
│   ├── paciente.py
│   ├── medico.py
│   ├── cita.py
│   └── expediente.py
├── controladores/           # Capa de Controladores (lógica)
│   ├── auth.py
│   └── reportes.py
├── vistas/                  # Capa de Vistas (Tkinter)
│   ├── login.py
│   ├── menu_principal.py
│   ├── pacientes_view.py
│   ├── medicos_view.py
│   ├── citas_view.py
│   ├── expedientes_view.py
│   └── reportes_view.py
└── utils/
    └── helpers.py           # Utilidades (hash, validaciones, formato)
```

## 6. Arquitectura

Arquitectura en 3 capas (MVC simplificado), tal como se describe en el
diseño lógico-físico (A11):

- **Presentación:** Tkinter (vistas/)
- **Lógica de negocio:** controladores/ + modelos/
- **Datos:** MySQL 8.0 vía mysql-connector (db/)
