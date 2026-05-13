"""
vistas/citas_view.py - CRUD de Citas
"""
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from modelos.cita import Cita, ESTADOS
from modelos.paciente import Paciente
from modelos.medico import Medico
from utils.helpers import parse_fecha_hora, fmt_fecha_hora


COLOR = "#E67E22"


class CitasView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de Citas")
        self.geometry("1020x600")
        self.minsize(960, 540)
        self.configure(bg="white")
        self._construir()
        self._recargar()

    def _construir(self):
        cab = tk.Frame(self, bg=COLOR, height=50)
        cab.pack(fill="x"); cab.pack_propagate(False)
        tk.Label(cab, text="  Registro de Citas  ",
                 bg=COLOR, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

        bar = tk.Frame(self, bg="white", padx=10, pady=10); bar.pack(fill="x")
        tk.Button(bar, text="+ Nueva cita", bg=COLOR, fg="white", bd=0,
                  padx=14, pady=6, font=("Segoe UI", 10, "bold"),
                  command=self._agregar).pack(side="left")
        tk.Button(bar, text="Editar", bg="#3F77C2", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._editar).pack(side="left", padx=5)
        tk.Button(bar, text="Eliminar", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=6,
                  command=self._eliminar).pack(side="left")

        tk.Label(bar, text="Buscar:", bg="white").pack(side="left", padx=(20, 5))
        self.txt_buscar = ttk.Entry(bar, width=24)
        self.txt_buscar.pack(side="left", ipady=3)
        self.txt_buscar.bind("<KeyRelease>", lambda e: self._recargar())

        tk.Label(bar, text="Estado:", bg="white").pack(side="left", padx=(15, 5))
        self.cb_estado = ttk.Combobox(bar, state="readonly", width=12,
                                      values=("Todos",) + ESTADOS)
        self.cb_estado.set("Todos")
        self.cb_estado.pack(side="left")
        self.cb_estado.bind("<<ComboboxSelected>>", lambda e: self._recargar())

        tabla_frame = tk.Frame(self, bg="white", padx=10, pady=5)
        tabla_frame.pack(fill="both", expand=True)
        cols = ("id", "fecha", "paciente", "medico", "esp", "estado", "motivo")
        textos = ("ID", "Fecha y hora", "Paciente", "Médico",
                  "Especialidad", "Estado", "Motivo")
        anchos = (50, 130, 170, 170, 120, 90, 250)
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
            datos = Cita.listar(filtro=self.txt_buscar.get().strip(),
                                estado=self.cb_estado.get())
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return
        for c in datos:
            self.tree.insert("", "end", values=(
                c["id_cita"], fmt_fecha_hora(c["fecha_hora"]),
                c["paciente"], c["medico"], c["especialidad"],
                c["estado"], c["motivo"] or ""))
        self.lbl_total.config(text=f"Total: {len(datos)} citas")

    def _seleccion_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Selecciona una cita.",
                                   parent=self)
            return None
        return int(self.tree.item(sel[0])["values"][0])

    def _agregar(self):
        FormCita(self, on_ok=self._recargar)

    def _editar(self):
        cid = self._seleccion_id()
        if cid is None:
            return
        FormCita(self, cita_id=cid, on_ok=self._recargar)

    def _eliminar(self):
        cid = self._seleccion_id()
        if cid is None:
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar la cita?",
                                   parent=self):
            return
        try:
            Cita.eliminar(cid)
            self._recargar()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)


class FormCita(tk.Toplevel):
    def __init__(self, parent, cita_id=None, on_ok=None):
        super().__init__(parent)
        self.cita_id = cita_id
        self.on_ok = on_ok
        self.title("Editar Cita" if cita_id else "Nueva Cita")
        self.geometry("520x540")
        self.minsize(500, 480)
        self.configure(bg="white")
        self.transient(parent)
        self.grab_set()
        self._cargar_combos()
        self._construir()
        if cita_id:
            self._cargar()
        self.bind("<Escape>", lambda e: self.destroy())

    def _cargar_combos(self):
        self.pacientes = Paciente.listar()
        self.medicos = Medico.listar_activos_combo()
        self.map_pac = {f"{p['nombre']} {p['apellidos']}": p["id_paciente"]
                        for p in self.pacientes}
        self.map_med = {etq: mid for mid, etq in self.medicos}
        # Validación temprana: si no hay pacientes o médicos, avisamos.
        faltan = []
        if not self.map_pac:
            faltan.append("pacientes")
        if not self.map_med:
            faltan.append("médicos activos")
        if faltan:
            messagebox.showwarning(
                "Sin datos",
                "No puedes crear una cita porque no hay "
                + " ni ".join(faltan) +
                " registrados.\n\nAgrega primero esos datos en su módulo.",
                parent=self)

    def _construir(self):
        # 1) Cabecera arriba
        tk.Label(self, text=("Editar" if self.cita_id else "Nueva")
                 + " Cita", bg=COLOR, fg="white",
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

        tk.Label(f, text="Fecha y hora *  (ej: 2026-05-15 14:30  ó  15/05/2026 14:30)",
                 bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(4, 2))
        # Pre-llena con hoy + 09:00 para nuevas citas
        self.var_fecha = tk.StringVar(
            value="" if self.cita_id else
            datetime.now().strftime("%Y-%m-%d 09:00"))
        ttk.Entry(f, textvariable=self.var_fecha).pack(fill="x", ipady=3)

        tk.Label(f, text="Paciente *", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(8, 2))
        self.var_pac = tk.StringVar()
        ttk.Combobox(f, textvariable=self.var_pac, state="readonly",
                     values=list(self.map_pac.keys())).pack(fill="x")

        tk.Label(f, text="Médico *", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(8, 2))
        self.var_med = tk.StringVar()
        ttk.Combobox(f, textvariable=self.var_med, state="readonly",
                     values=list(self.map_med.keys())).pack(fill="x")

        tk.Label(f, text="Estado *", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(8, 2))
        self.var_estado = tk.StringVar(value="Pendiente")
        ttk.Combobox(f, textvariable=self.var_estado, state="readonly",
                     values=ESTADOS).pack(fill="x")

        tk.Label(f, text="Motivo", bg="white", anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(fill="x", pady=(8, 2))
        self.var_motivo = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_motivo).pack(fill="x", ipady=3)

    def _cargar(self):
        c = Cita.obtener(self.cita_id)
        if not c:
            messagebox.showerror("Error", "Cita no encontrada.", parent=self)
            self.destroy(); return
        self.var_fecha.set(fmt_fecha_hora(c["fecha_hora"]))
        for etq, pid in self.map_pac.items():
            if pid == c["id_paciente"]:
                self.var_pac.set(etq); break
        for etq, mid in self.map_med.items():
            if mid == c["id_medico"]:
                self.var_med.set(etq); break
        self.var_estado.set(c["estado"])
        self.var_motivo.set(c["motivo"] or "")

    def _guardar(self):
        try:
            fh = parse_fecha_hora(self.var_fecha.get())
        except ValueError as e:
            messagebox.showwarning("Fecha inválida", str(e), parent=self)
            return
        pac_etq = self.var_pac.get()
        med_etq = self.var_med.get()
        if not pac_etq or not med_etq:
            messagebox.showwarning("Faltan datos",
                                   "Selecciona paciente y médico.",
                                   parent=self); return
        d = {
            "fecha_hora":  fh,
            "estado":      self.var_estado.get() or "Pendiente",
            "motivo":      self.var_motivo.get().strip() or None,
            "id_paciente": self.map_pac[pac_etq],
            "id_medico":   self.map_med[med_etq],
        }
        try:
            if self.cita_id:
                Cita.actualizar(self.cita_id, d)
            else:
                Cita.crear(d)
        except Exception as e:
            # Mostramos el detalle real para poder diagnosticar
            messagebox.showerror(
                "Error al guardar la cita",
                f"{type(e).__name__}: {e}\n\n"
                f"Detalle técnico:\n{traceback.format_exc()}",
                parent=self)
            return
        if self.on_ok:
            self.on_ok()
        self.destroy()
