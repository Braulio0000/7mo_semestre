"""
vistas/medicos_view.py - CRUD de Médicos
"""
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.medico import Medico
from utils.helpers import es_email_valido, es_telefono_valido


COLOR = "#1565C0"


class MedicosView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Médicos")
        self.geometry("960x560")
        self.minsize(900, 520)
        self.configure(bg="white")
        self._construir()
        self._recargar()

    def _construir(self):
        cab = tk.Frame(self, bg=COLOR, height=50)
        cab.pack(fill="x"); cab.pack_propagate(False)
        tk.Label(cab, text="  Gestión de Médicos  ",
                 bg=COLOR, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

        barra = tk.Frame(self, bg="white", padx=10, pady=10)
        barra.pack(fill="x")
        tk.Button(barra, text="+ Agregar", bg=COLOR, fg="white", bd=0,
                  padx=14, pady=6, font=("Segoe UI", 10, "bold"),
                  command=self._agregar).pack(side="left")
        tk.Button(barra, text="Editar", bg="#3F77C2", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._editar).pack(side="left", padx=5)
        tk.Button(barra, text="Eliminar", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._eliminar).pack(side="left")

        tk.Label(barra, text="Buscar:", bg="white").pack(side="left", padx=(20, 5))
        self.txt_buscar = ttk.Entry(barra, width=30)
        self.txt_buscar.pack(side="left", ipady=3)
        self.txt_buscar.bind("<KeyRelease>", lambda e: self._recargar())

        tabla_frame = tk.Frame(self, bg="white", padx=10, pady=5)
        tabla_frame.pack(fill="both", expand=True)
        cols = ("id", "nombre", "apellidos", "especialidad", "cedula",
                "telefono", "email", "activo")
        textos = ("ID", "Nombre", "Apellidos", "Especialidad", "Cédula",
                  "Teléfono", "Email", "Activo")
        anchos = (50, 110, 130, 130, 90, 100, 180, 60)
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                 height=15)
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
                  padx=20, pady=6, command=self.destroy).pack(pady=8)

    def _recargar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            datos = Medico.listar(self.txt_buscar.get().strip())
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return
        for m in datos:
            self.tree.insert("", "end", values=(
                m["id_medico"], m["nombre"], m["apellidos"],
                m["especialidad"], m["cedula"],
                m["telefono"] or "", m["email"] or "",
                "Sí" if m["activo"] else "No"))
        self.lbl_total.config(text=f"Total: {len(datos)} médicos")

    def _seleccion_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un médico.",
                                   parent=self)
            return None
        return int(self.tree.item(sel[0])["values"][0])

    def _agregar(self):
        FormMedico(self, on_ok=self._recargar)

    def _editar(self):
        mid = self._seleccion_id()
        if mid is None:
            return
        FormMedico(self, medico_id=mid, on_ok=self._recargar)

    def _eliminar(self):
        mid = self._seleccion_id()
        if mid is None:
            return
        if not messagebox.askyesno("Confirmar",
                                   "¿Eliminar médico?\n"
                                   "(No se puede eliminar si tiene citas.)",
                                   parent=self):
            return
        try:
            Medico.eliminar(mid)
            self._recargar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class FormMedico(tk.Toplevel):
    def __init__(self, parent, medico_id=None, on_ok=None):
        super().__init__(parent)
        self.medico_id = medico_id
        self.on_ok = on_ok
        self.title("Editar Médico" if medico_id else "Agregar Médico")
        self.geometry("480x600")
        self.minsize(460, 540)
        self.configure(bg="white")
        self.transient(parent)
        self.grab_set()
        self._construir()
        if medico_id:
            self._cargar()
        self.bind("<Escape>", lambda e: self.destroy())

    def _construir(self):
        # 1) Cabecera arriba
        tk.Label(self, text=("Editar" if self.medico_id else "Agregar")
                 + " Médico", bg=COLOR, fg="white",
                 font=("Segoe UI", 13, "bold"), pady=10).pack(side="top", fill="x")

        # 2) Botones FIJOS abajo
        botones = tk.Frame(self, bg="white", pady=10)
        botones.pack(side="bottom", fill="x")
        tk.Button(botones, text="Guardar", bg=COLOR, fg="white", bd=0,
                  padx=24, pady=8, font=("Segoe UI", 10, "bold"),
                  cursor="hand2",
                  command=self._guardar).pack(side="left", padx=20)
        tk.Button(botones, text="Cancelar", bg="#7F8C8D", fg="white", bd=0,
                  padx=24, pady=8, cursor="hand2",
                  command=self.destroy).pack(side="right", padx=20)

        # 3) Formulario en el medio
        f = tk.Frame(self, bg="white", padx=20, pady=10)
        f.pack(side="top", fill="both", expand=True)

        self.vars = {}
        campos = [
            ("nombre",       "Nombre *"),
            ("apellidos",    "Apellidos *"),
            ("especialidad", "Especialidad *"),
            ("cedula",       "Cédula profesional *"),
            ("telefono",     "Teléfono"),
            ("email",        "Email"),
        ]
        primer = None
        for k, lbl in campos:
            tk.Label(f, text=lbl, bg="white", anchor="w",
                     font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(6, 2))
            v = tk.StringVar()
            e = ttk.Entry(f, textvariable=v); e.pack(fill="x", ipady=3)
            if primer is None:
                primer = e
            self.vars[k] = v
        self.var_activo = tk.IntVar(value=1)
        tk.Checkbutton(f, text="Activo", variable=self.var_activo,
                       bg="white").pack(anchor="w", pady=(10, 0))
        if primer:
            primer.focus()

    def _cargar(self):
        m = Medico.obtener(self.medico_id)
        if not m:
            messagebox.showerror("Error", "Médico no encontrado.",
                                 parent=self); self.destroy(); return
        for k in ("nombre", "apellidos", "especialidad", "cedula",
                  "telefono", "email"):
            self.vars[k].set(m[k] or "")
        self.var_activo.set(1 if m["activo"] else 0)

    def _guardar(self):
        d = {k: v.get().strip() for k, v in self.vars.items()}
        d["activo"] = self.var_activo.get()
        for req in ("nombre", "apellidos", "especialidad", "cedula"):
            if not d[req]:
                messagebox.showwarning(
                    "Faltan datos",
                    f"El campo «{req}» es obligatorio.",
                    parent=self); return
        if not es_email_valido(d["email"]):
            messagebox.showwarning("Email inválido", "Revisa el email.",
                                   parent=self); return
        if not es_telefono_valido(d["telefono"]):
            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe tener entre 7 y 15 dígitos.",
                parent=self); return
        try:
            if self.medico_id:
                Medico.actualizar(self.medico_id, d)
            else:
                Medico.crear(d)
        except Exception as e:
            messagebox.showerror("Error de BD", str(e), parent=self); return
        if self.on_ok:
            self.on_ok()
        self.destroy()
