"""
vistas/pacientes_view.py - CRUD de Pacientes
"""
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.paciente import Paciente
from utils.helpers import (es_email_valido, es_telefono_valido,
                           parse_fecha, fmt_fecha)


COLOR = "#0E9B83"


class PacientesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Pacientes")
        self.geometry("960x560")
        self.minsize(900, 520)
        self.configure(bg="white")
        self._construir()
        self._recargar()

    def _construir(self):
        cab = tk.Frame(self, bg=COLOR, height=50)
        cab.pack(fill="x")
        cab.pack_propagate(False)
        tk.Label(cab, text="  Gestión de Pacientes  ",
                 bg=COLOR, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

        barra = tk.Frame(self, bg="white", padx=10, pady=10)
        barra.pack(fill="x")

        tk.Button(barra, text="+ Agregar", bg=COLOR, fg="white", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  activebackground=COLOR, activeforeground="white",
                  command=self._agregar).pack(side="left")
        tk.Button(barra, text="Editar", bg="#3F77C2", fg="white", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  command=self._editar).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  command=self._eliminar).pack(side="left")

        tk.Label(barra, text="Buscar:", bg="white").pack(side="left", padx=(20, 5))
        self.txt_buscar = ttk.Entry(barra, width=30)
        self.txt_buscar.pack(side="left", ipady=3)
        self.txt_buscar.bind("<KeyRelease>", lambda e: self._recargar())

        tabla_frame = tk.Frame(self, bg="white", padx=10, pady=5)
        tabla_frame.pack(fill="both", expand=True)

        cols = ("id", "nombre", "apellidos", "fecha_nac", "sexo",
                "telefono", "email")
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                 height=15)
        anchos = (50, 130, 150, 95, 50, 110, 200)
        textos = ("ID", "Nombre", "Apellidos", "F. Nac.", "Sexo",
                  "Teléfono", "Email")
        for c, t, w in zip(cols, textos, anchos):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(tabla_frame, orient="vertical",
                           command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.bind("<Double-1>", lambda e: self._editar())

        self.lbl_total = tk.Label(self, text="", bg="white", fg="#555",
                                  font=("Segoe UI", 9))
        self.lbl_total.pack(anchor="w", padx=15, pady=(0, 5))

        tk.Button(self, text="Cerrar", bg="#7F8C8D", fg="white", bd=0,
                  padx=20, pady=6, cursor="hand2",
                  command=self.destroy).pack(pady=8)

    def _recargar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            datos = Paciente.listar(self.txt_buscar.get().strip())
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
            return
        for p in datos:
            self.tree.insert("", "end", values=(
                p["id_paciente"], p["nombre"], p["apellidos"],
                fmt_fecha(p["fecha_nac"]), p["sexo"],
                p["telefono"] or "", p["email"] or ""))
        self.lbl_total.config(text=f"Total: {len(datos)} pacientes")

    def _seleccion_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un paciente.",
                                   parent=self)
            return None
        return int(self.tree.item(sel[0])["values"][0])

    def _agregar(self):
        FormPaciente(self, on_ok=self._recargar)

    def _editar(self):
        pid = self._seleccion_id()
        if pid is None:
            return
        FormPaciente(self, paciente_id=pid, on_ok=self._recargar)

    def _eliminar(self):
        pid = self._seleccion_id()
        if pid is None:
            return
        if not messagebox.askyesno("Confirmar",
                                   "¿Eliminar paciente seleccionado?\n"
                                   "(No se puede eliminar si tiene citas.)",
                                   parent=self):
            return
        try:
            Paciente.eliminar(pid)
            self._recargar()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}",
                                 parent=self)


class FormPaciente(tk.Toplevel):
    def __init__(self, parent, paciente_id=None, on_ok=None):
        super().__init__(parent)
        self.paciente_id = paciente_id
        self.on_ok = on_ok
        self.title("Editar Paciente" if paciente_id else "Agregar Paciente")
        self.geometry("480x620")
        self.minsize(460, 560)
        self.configure(bg="white")
        self.transient(parent)
        self.grab_set()
        self._construir()
        if paciente_id:
            self._cargar()
        self.bind("<Escape>", lambda e: self.destroy())

    def _construir(self):
        # 1) Cabecera arriba
        tk.Label(self, text=("Editar" if self.paciente_id else "Agregar")
                 + " Paciente", bg=COLOR, fg="white",
                 font=("Segoe UI", 13, "bold"),
                 pady=10).pack(side="top", fill="x")

        # 2) Botones FIJOS abajo (clave: side="bottom" ANTES del formulario)
        botones = tk.Frame(self, bg="white", pady=10)
        botones.pack(side="bottom", fill="x")
        tk.Button(botones, text="Guardar", bg=COLOR, fg="white", bd=0,
                  padx=24, pady=8, cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  activebackground=COLOR, activeforeground="white",
                  command=self._guardar).pack(side="left", padx=20)
        tk.Button(botones, text="Cancelar", bg="#7F8C8D", fg="white", bd=0,
                  padx=24, pady=8, cursor="hand2",
                  command=self.destroy).pack(side="right", padx=20)

        # 3) Formulario en el medio
        f = tk.Frame(self, bg="white", padx=20, pady=10)
        f.pack(side="top", fill="both", expand=True)

        self.vars = {}
        campos = [
            ("nombre",    "Nombre *", "entry"),
            ("apellidos", "Apellidos *", "entry"),
            ("fecha_nac", "Fecha nacimiento (YYYY-MM-DD ó dd/mm/yyyy) *", "entry"),
            ("sexo",      "Sexo *", "combo", ["M", "F", "O"]),
            ("telefono",  "Teléfono", "entry"),
            ("email",     "Email", "entry"),
            ("direccion", "Dirección", "entry"),
        ]
        primer = None
        for spec in campos:
            key, label = spec[0], spec[1]
            tipo = spec[2]
            tk.Label(f, text=label, bg="white", anchor="w",
                     font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(6, 2))
            if tipo == "combo":
                v = tk.StringVar()
                ttk.Combobox(f, textvariable=v, state="readonly",
                             values=spec[3]).pack(fill="x", ipady=2)
                self.vars[key] = v
            else:
                v = tk.StringVar()
                e = ttk.Entry(f, textvariable=v)
                e.pack(fill="x", ipady=3)
                if primer is None:
                    primer = e
                self.vars[key] = v

        if not self.paciente_id:
            self.vars["sexo"].set("M")
        if primer:
            primer.focus()

    def _cargar(self):
        p = Paciente.obtener(self.paciente_id)
        if not p:
            messagebox.showerror("Error", "Paciente no encontrado.",
                                 parent=self)
            self.destroy()
            return
        self.vars["nombre"].set(p["nombre"])
        self.vars["apellidos"].set(p["apellidos"])
        self.vars["fecha_nac"].set(fmt_fecha(p["fecha_nac"]))
        self.vars["sexo"].set(p["sexo"])
        self.vars["telefono"].set(p["telefono"] or "")
        self.vars["email"].set(p["email"] or "")
        self.vars["direccion"].set(p["direccion"] or "")

    def _guardar(self):
        d = {k: v.get().strip() for k, v in self.vars.items()}
        if not d["nombre"] or not d["apellidos"] or not d["fecha_nac"] or not d["sexo"]:
            messagebox.showwarning(
                "Faltan datos",
                "Nombre, apellidos, fecha de nacimiento y sexo son obligatorios.",
                parent=self)
            return
        try:
            d["fecha_nac"] = parse_fecha(d["fecha_nac"]).date()
        except ValueError:
            messagebox.showwarning(
                "Fecha inválida",
                "Usa formato YYYY-MM-DD ó dd/mm/yyyy.",
                parent=self)
            return
        if not es_email_valido(d["email"]):
            messagebox.showwarning("Email inválido", "Revisa el email.",
                                   parent=self)
            return
        if not es_telefono_valido(d["telefono"]):
            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe tener entre 7 y 15 dígitos.",
                parent=self)
            return
        try:
            if self.paciente_id:
                Paciente.actualizar(self.paciente_id, d)
            else:
                Paciente.crear(d)
        except Exception as e:
            messagebox.showerror("Error de BD", str(e), parent=self)
            return
        if self.on_ok:
            self.on_ok()
        self.destroy()
