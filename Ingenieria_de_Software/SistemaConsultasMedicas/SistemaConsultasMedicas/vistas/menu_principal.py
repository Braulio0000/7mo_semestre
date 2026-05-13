"""
vistas/menu_principal.py - Menú Principal con tarjetas de módulo
"""
import tkinter as tk
from tkinter import messagebox

from controladores.auth import Sesion
from config import APP_NAME, APP_VERSION, APP_YEAR

from vistas.pacientes_view   import PacientesView
from vistas.medicos_view     import MedicosView
from vistas.citas_view       import CitasView
from vistas.expedientes_view import ExpedientesView
from vistas.reportes_view    import ReportesView


# ----- Definición de módulos -------------------------------------------------
MODULOS = [
    # (clave, etiqueta, descripción, color, roles_permitidos, vista_clase)
    ("pacientes",   "Pacientes",   "Catálogo de pacientes",
        "#0E9B83",  ("Administrador", "Recepcionista"), PacientesView),
    ("medicos",     "Médicos",     "Personal médico",
        "#1565C0",  ("Administrador",),                 MedicosView),
    ("citas",       "Citas",       "Agenda y registro",
        "#E67E22",  ("Administrador", "Recepcionista"), CitasView),
    ("expedientes", "Expedientes", "Historial clínico",
        "#8E44AD",  ("Administrador",),                 ExpedientesView),
    ("reportes",    "Reportes",    "Informes y estadísticas",
        "#C0392B",  ("Administrador",),                 ReportesView),
]


class MenuPrincipal(tk.Tk):
    def __init__(self, on_logout):
        super().__init__()
        self.on_logout = on_logout
        self.title(f"{APP_NAME} — Menú Principal")
        self.geometry("960x600")
        self.minsize(900, 560)
        self.configure(bg="#F0F2F5")

        self._construir()
        self._centrar()

    def _centrar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _construir(self):
        # ---- Barra superior ----
        barra = tk.Frame(self, bg="#0E4D64", height=60)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        tk.Label(barra, text=f"  🩺  {APP_NAME}",
                 bg="#0E4D64", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)

        u = Sesion.usuario_actual
        tk.Label(barra, text=f"  {u.nombre}  ({u.rol})  ",
                 bg="#0E4D64", fg="#CADCFC",
                 font=("Segoe UI", 10)).pack(side="right", padx=10)

        tk.Button(barra, text="Cerrar Sesión", bg="#C0392B", fg="white",
                  bd=0, padx=14, pady=6, cursor="hand2",
                  font=("Segoe UI", 9, "bold"),
                  activebackground="#922B21", activeforeground="white",
                  command=self._cerrar_sesion).pack(side="right", padx=10, pady=10)

        # ---- Cuerpo: tarjetas de módulo ----
        cuerpo = tk.Frame(self, bg="#F0F2F5", padx=20, pady=20)
        cuerpo.pack(fill="both", expand=True)

        tk.Label(cuerpo, text="Módulos del Sistema",
                 bg="#F0F2F5", fg="#222",
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 15))

        grid = tk.Frame(cuerpo, bg="#F0F2F5")
        grid.pack(fill="both", expand=True)

        cols = 3
        for i, mod in enumerate(MODULOS):
            r, c = divmod(i, cols)
            self._tarjeta(grid, r, c, mod)
        for c in range(cols):
            grid.columnconfigure(c, weight=1, uniform="col")

        # ---- Pie ----
        pie = tk.Frame(self, bg="#F0F2F5", height=30)
        pie.pack(fill="x", side="bottom")
        tk.Label(pie, text=f"Sistema v{APP_VERSION} — {APP_YEAR}  •  "
                           "Braulio Yael Carranza Zamora",
                 bg="#F0F2F5", fg="#888",
                 font=("Segoe UI", 8)).pack(pady=5)

    def _tarjeta(self, parent, r, c, mod):
        clave, etiqueta, desc, color, roles, vista_cls = mod

        habilitada = Sesion.usuario_actual.rol in roles

        card = tk.Frame(parent, bg="white", bd=0, relief="flat",
                        highlightthickness=1, highlightbackground="#DDE2EA")
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)
        parent.rowconfigure(r, weight=1)

        # Banda de color superior
        banda = tk.Frame(card, bg=color, height=8)
        banda.pack(fill="x", side="top")

        contenido = tk.Frame(card, bg="white", padx=15, pady=15)
        contenido.pack(fill="both", expand=True)

        tk.Label(contenido, text=etiqueta, bg="white",
                 fg=color if habilitada else "#999",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(contenido, text=desc, bg="white",
                 fg="#555" if habilitada else "#AAA",
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 12))

        if habilitada:
            tk.Button(contenido, text="Abrir →", bg=color, fg="white",
                      bd=0, padx=14, pady=6, cursor="hand2",
                      font=("Segoe UI", 10, "bold"),
                      activebackground=color, activeforeground="white",
                      command=lambda v=vista_cls: self._abrir(v)).pack(anchor="w")
        else:
            tk.Label(contenido, text="🔒  Sin acceso (rol)",
                     bg="white", fg="#AAA",
                     font=("Segoe UI", 9, "italic")).pack(anchor="w")

    def _abrir(self, vista_cls):
        # Las vistas son ventanas Toplevel: bloquean el menú hasta cerrarse.
        win = vista_cls(self)
        win.grab_set()
        self.wait_window(win)

    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar la sesión actual?"):
            Sesion.cerrar()
            self.destroy()
            self.on_logout()
