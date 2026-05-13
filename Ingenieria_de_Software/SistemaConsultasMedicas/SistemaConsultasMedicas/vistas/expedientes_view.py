"""
vistas/expedientes_view.py - CRUD de Expedientes
"""
import traceback
import tkinter as tk
from tkinter import ttk, messagebox

from modelos.expediente import Expediente
from modelos.cita import Cita
from utils.helpers import fmt_fecha_hora


COLOR = "#8E44AD"


class ExpedientesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Expedientes Clínicos")
        self.geometry("1020x600")
        self.minsize(960, 540)
        self.configure(bg="white")
        self._construir()
        self._recargar()

    def _construir(self):
        cab = tk.Frame(self, bg=COLOR, height=50)
        cab.pack(fill="x"); cab.pack_propagate(False)
        tk.Label(cab, text="  Expedientes Clínicos  ",
                 bg=COLOR, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

        bar = tk.Frame(self, bg="white", padx=10, pady=10); bar.pack(fill="x")
        tk.Button(bar, text="+ Nuevo", bg=COLOR, fg="white", bd=0,
                  padx=14, pady=6, font=("Segoe UI", 10, "bold"),
                  command=self._agregar).pack(side="left")
        tk.Button(bar, text="Editar", bg="#3F77C2", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._editar).pack(side="left", padx=5)
        tk.Button(bar, text="Eliminar", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._eliminar).pack(side="left")

        tk.Label(bar, text="Buscar:", bg="white").pack(side="left", padx=(20, 5))
        self.txt_buscar = ttk.Entry(bar, width=30)
        self.txt_buscar.pack(side="left", ipady=3)
        self.txt_buscar.bind("<KeyRelease>", lambda e: self._recargar())

        tabla_frame = tk.Frame(self, bg="white", padx=10, pady=5)
        tabla_frame.pack(fill="both", expand=True)
        cols = ("id", "fecha", "paciente", "medico", "esp", "diagnostico")
        textos = ("ID", "Fecha alta", "Paciente", "Médico",
                  "Especialidad", "Diagnóstico")
        anchos = (50, 120, 170, 170, 120, 380)
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                 height=16)
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
            datos = Expediente.listar(self.txt_buscar.get().strip())
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return
        for e in datos:
            self.tree.insert("", "end", values=(
                e["id_expediente"], fmt_fecha_hora(e["fecha_alta"]),
                e["paciente"], e["medico"], e["especialidad"],
                (e["diagnostico"] or "")[:120]))
        self.lbl_total.config(text=f"Total: {len(datos)} expedientes")

    def _seleccion_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona un expediente.",
                                   parent=self)
            return None
        return int(self.tree.item(sel[0])["values"][0])

    def _agregar(self):
        FormExpediente(self, on_ok=self._recargar)

    def _editar(self):
        eid = self._seleccion_id()
        if eid is None:
            return
        FormExpediente(self, expediente_id=eid, on_ok=self._recargar)

    def _eliminar(self):
        eid = self._seleccion_id()
        if eid is None:
            return
        if not messagebox.askyesno("Confirmar",
                                   "¿Eliminar el expediente?", parent=self):
            return
        try:
            Expediente.eliminar(eid)
            self._recargar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class FormExpediente(tk.Toplevel):
    def __init__(self, parent, expediente_id=None, on_ok=None):
        super().__init__(parent)
        self.expediente_id = expediente_id
        self.on_ok = on_ok
        self.title("Editar Expediente" if expediente_id else "Nuevo Expediente")
        self.geometry("560x600")
        self.minsize(540, 540)
        self.configure(bg="white")
        self.transient(parent)
        self.grab_set()
        self._construir()
        if expediente_id:
            self._cargar()
        else:
            self._cargar_combo_citas()
        self.bind("<Escape>", lambda e: self.destroy())

    def _construir(self):
        # 1) Cabecera
        tk.Label(self, text=("Editar" if self.expediente_id else "Nuevo")
                 + " Expediente", bg=COLOR, fg="white",
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

        # 3) Formulario
        f = tk.Frame(self, bg="white", padx=20, pady=10)
        f.pack(side="top", fill="both", expand=True)

        tk.Label(f, text="Cita asociada (aún sin expediente) *", bg="white",
                 anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(4, 2))
        self.var_cita = tk.StringVar()
        self.cb_citas = ttk.Combobox(f, textvariable=self.var_cita,
                                     state="readonly")
        self.cb_citas.pack(fill="x")

        tk.Label(f, text="Diagnóstico *", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(10, 2))
        self.txt_diag = tk.Text(f, height=4, wrap="word", bd=1, relief="solid")
        self.txt_diag.pack(fill="x")

        tk.Label(f, text="Tratamiento", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(10, 2))
        self.txt_trat = tk.Text(f, height=3, wrap="word", bd=1, relief="solid")
        self.txt_trat.pack(fill="x")

        tk.Label(f, text="Observaciones", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(10, 2))
        self.txt_obs = tk.Text(f, height=3, wrap="word", bd=1, relief="solid")
        self.txt_obs.pack(fill="x")

    def _cargar_combo_citas(self):
        citas = Cita.listar_atendidas_sin_expediente()
        self.map_citas = {
            f"#{c['id_cita']} — {fmt_fecha_hora(c['fecha_hora'])} — "
            f"[{c.get('estado', '')}] {c['paciente']} → {c['medico']}": c["id_cita"]
            for c in citas
        }
        self.cb_citas.configure(values=list(self.map_citas.keys()))
        if not citas:
            messagebox.showinfo(
                "Sin citas disponibles",
                "Todas las citas registradas ya tienen su expediente.\n"
                "Crea primero una cita nueva en el módulo Citas.",
                parent=self)
        elif self.map_citas:
            # Pre-seleccionar la primera para que el usuario solo escriba diagnóstico
            self.cb_citas.current(0)

    def _cargar(self):
        e = Expediente.obtener(self.expediente_id)
        if not e:
            messagebox.showerror("Error", "Expediente no encontrado.",
                                 parent=self); self.destroy(); return
        c = Cita.obtener(e["id_cita"])
        from modelos.paciente import Paciente
        from modelos.medico import Medico
        p = Paciente.obtener(c["id_paciente"])
        m = Medico.obtener(c["id_medico"])
        etiqueta = (f"#{c['id_cita']} — {fmt_fecha_hora(c['fecha_hora'])} — "
                    f"{p['nombre']} {p['apellidos']} → "
                    f"{m['nombre']} {m['apellidos']}")
        self.cb_citas.configure(values=[etiqueta], state="disabled")
        self.var_cita.set(etiqueta)
        self.map_citas = {etiqueta: c["id_cita"]}

        self.txt_diag.insert("1.0", e["diagnostico"] or "")
        self.txt_trat.insert("1.0", e["tratamiento"] or "")
        self.txt_obs.insert("1.0", e["observaciones"] or "")

    def _guardar(self):
        etq = self.var_cita.get()
        if not etq:
            messagebox.showwarning("Faltan datos", "Selecciona una cita.",
                                   parent=self); return
        diag = self.txt_diag.get("1.0", "end").strip()
        if not diag:
            messagebox.showwarning("Faltan datos",
                                   "El diagnóstico es obligatorio.",
                                   parent=self); return
        d = {
            "id_cita":       self.map_citas[etq],
            "diagnostico":   diag,
            "tratamiento":   self.txt_trat.get("1.0", "end").strip(),
            "observaciones": self.txt_obs.get("1.0", "end").strip(),
        }
        try:
            if self.expediente_id:
                Expediente.actualizar(self.expediente_id, d)
            else:
                Expediente.crear(d)
        except Exception as e:
            messagebox.showerror(
                "Error al guardar el expediente",
                f"{type(e).__name__}: {e}\n\n"
                f"Detalle técnico:\n{traceback.format_exc()}",
                parent=self)
            return
        if self.on_ok:
            self.on_ok()
        self.destroy()
