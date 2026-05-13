"""
vistas/reportes_view.py - Reportes con exportación a PDF y Excel
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

from modelos.cita import Cita
from modelos.expediente import Expediente
from modelos.paciente import Paciente
from modelos.medico import Medico
from controladores.reportes import exportar_pdf, exportar_excel
from utils.helpers import fmt_fecha_hora, fmt_fecha


COLOR = "#C0392B"


class ReportesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reportes del Sistema")
        self.geometry("1020x620")
        self.minsize(960, 560)
        self.configure(bg="white")
        self._construir()
        self._recargar()

    def _construir(self):
        cab = tk.Frame(self, bg=COLOR, height=50)
        cab.pack(fill="x"); cab.pack_propagate(False)
        tk.Label(cab, text="  Reportes del Sistema  ",
                 bg=COLOR, fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=15)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_citas = tk.Frame(self.notebook, bg="white")
        self.tab_expe = tk.Frame(self.notebook, bg="white")
        self.tab_resumen = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tab_citas,    text="  Citas  ")
        self.notebook.add(self.tab_expe,     text="  Expedientes  ")
        self.notebook.add(self.tab_resumen,  text="  Resumen  ")

        self._tab_citas()
        self._tab_expe()
        self._tab_resumen()

        bot = tk.Frame(self, bg="white"); bot.pack(pady=8)
        tk.Button(bot, text="🔄 Refrescar todo", bg="#0E4D64", fg="white",
                  bd=0, padx=20, pady=6, font=("Segoe UI", 10, "bold"),
                  cursor="hand2",
                  command=self._recargar).pack(side="left", padx=8)
        tk.Button(bot, text="Cerrar", bg="#7F8C8D", fg="white", bd=0,
                  padx=20, pady=6,
                  command=self.destroy).pack(side="left", padx=8)

    # ------- Tab 1: Citas ----------------------------------------------------
    def _tab_citas(self):
        bar = tk.Frame(self.tab_citas, bg="white", padx=10, pady=10)
        bar.pack(fill="x")
        tk.Label(bar, text="Desde (YYYY-MM-DD):",
                 bg="white").pack(side="left")
        self.cit_desde = ttk.Entry(bar, width=12); self.cit_desde.pack(side="left", padx=5)
        tk.Label(bar, text="Hasta:", bg="white").pack(side="left")
        self.cit_hasta = ttk.Entry(bar, width=12); self.cit_hasta.pack(side="left", padx=5)
        tk.Button(bar, text="Filtrar", bg="#0E4D64", fg="white", bd=0,
                  padx=14, pady=4, command=self._recargar_citas).pack(side="left", padx=10)
        tk.Button(bar, text="Exportar PDF", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=4, command=self._exp_pdf_citas).pack(side="right", padx=4)
        tk.Button(bar, text="Exportar Excel", bg="#0E9B83", fg="white", bd=0,
                  padx=14, pady=4, command=self._exp_xlsx_citas).pack(side="right")

        cols = ("id", "fecha", "paciente", "medico", "esp", "estado", "motivo")
        textos = ("ID", "Fecha", "Paciente", "Médico", "Especialidad",
                  "Estado", "Motivo")
        anchos = (50, 130, 170, 170, 110, 90, 250)
        f = tk.Frame(self.tab_citas, bg="white", padx=10, pady=5)
        f.pack(fill="both", expand=True)
        self.tree_cit = ttk.Treeview(f, columns=cols, show="headings", height=15)
        for c, t, w in zip(cols, textos, anchos):
            self.tree_cit.heading(c, text=t)
            self.tree_cit.column(c, width=w, anchor="w")
        self.tree_cit.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(f, orient="vertical",
                           command=self.tree_cit.yview)
        sb.pack(side="right", fill="y")
        self.tree_cit.configure(yscrollcommand=sb.set)

        self.lbl_cit = tk.Label(self.tab_citas, text="", bg="white", fg="#555")
        self.lbl_cit.pack(anchor="w", padx=15, pady=(0, 5))

    def _recargar_citas(self):
        for i in self.tree_cit.get_children():
            self.tree_cit.delete(i)
        try:
            datos = Cita.listar(desde=self.cit_desde.get().strip() or None,
                                hasta=self.cit_hasta.get().strip() or None)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return
        for c in datos:
            self.tree_cit.insert("", "end", values=(
                c["id_cita"], fmt_fecha_hora(c["fecha_hora"]),
                c["paciente"], c["medico"], c["especialidad"],
                c["estado"], c["motivo"] or ""))
        self.lbl_cit.config(text=f"Total: {len(datos)} citas")

    def _filas_citas(self):
        return [(self.tree_cit.item(i)["values"]) for i in self.tree_cit.get_children()]

    def _exp_pdf_citas(self):
        if not self._filas_citas():
            messagebox.showinfo("Sin datos", "No hay citas para exportar.", parent=self); return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
            initialfile="reporte_citas.pdf", parent=self)
        if not ruta:
            return
        try:
            exportar_pdf(ruta, "Reporte de Citas",
                         ["ID", "Fecha", "Paciente", "Médico",
                          "Especialidad", "Estado", "Motivo"],
                         self._filas_citas(),
                         subtitulo=self._subt_rango(self.cit_desde, self.cit_hasta))
            messagebox.showinfo("PDF generado", f"Archivo:\n{ruta}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _exp_xlsx_citas(self):
        if not self._filas_citas():
            messagebox.showinfo("Sin datos", "No hay citas para exportar.", parent=self); return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")],
            initialfile="reporte_citas.xlsx", parent=self)
        if not ruta:
            return
        try:
            exportar_excel(ruta, "Reporte de Citas",
                           ["ID", "Fecha", "Paciente", "Médico",
                            "Especialidad", "Estado", "Motivo"],
                           self._filas_citas())
            messagebox.showinfo("Excel generado", f"Archivo:\n{ruta}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    # ------- Tab 2: Expedientes ----------------------------------------------
    def _tab_expe(self):
        bar = tk.Frame(self.tab_expe, bg="white", padx=10, pady=10)
        bar.pack(fill="x")
        tk.Label(bar, text="Desde:", bg="white").pack(side="left")
        self.exp_desde = ttk.Entry(bar, width=12); self.exp_desde.pack(side="left", padx=5)
        tk.Label(bar, text="Hasta:", bg="white").pack(side="left")
        self.exp_hasta = ttk.Entry(bar, width=12); self.exp_hasta.pack(side="left", padx=5)
        tk.Button(bar, text="Filtrar", bg="#0E4D64", fg="white", bd=0,
                  padx=14, pady=4, command=self._recargar_expe).pack(side="left", padx=10)
        tk.Button(bar, text="Exportar PDF", bg="#C0392B", fg="white", bd=0,
                  padx=14, pady=4, command=self._exp_pdf_expe).pack(side="right", padx=4)
        tk.Button(bar, text="Exportar Excel", bg="#0E9B83", fg="white", bd=0,
                  padx=14, pady=4, command=self._exp_xlsx_expe).pack(side="right")

        cols = ("id", "fecha", "paciente", "medico", "esp", "diag")
        textos = ("ID", "Fecha alta", "Paciente", "Médico",
                  "Especialidad", "Diagnóstico")
        anchos = (50, 120, 170, 170, 110, 380)
        f = tk.Frame(self.tab_expe, bg="white", padx=10, pady=5)
        f.pack(fill="both", expand=True)
        self.tree_exp = ttk.Treeview(f, columns=cols, show="headings", height=15)
        for c, t, w in zip(cols, textos, anchos):
            self.tree_exp.heading(c, text=t)
            self.tree_exp.column(c, width=w, anchor="w")
        self.tree_exp.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(f, orient="vertical", command=self.tree_exp.yview)
        sb.pack(side="right", fill="y")
        self.tree_exp.configure(yscrollcommand=sb.set)

        self.lbl_exp = tk.Label(self.tab_expe, text="", bg="white", fg="#555")
        self.lbl_exp.pack(anchor="w", padx=15, pady=(0, 5))

    def _recargar_expe(self):
        for i in self.tree_exp.get_children():
            self.tree_exp.delete(i)
        try:
            datos = Expediente.listar(desde=self.exp_desde.get().strip() or None,
                                      hasta=self.exp_hasta.get().strip() or None)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return
        for e in datos:
            self.tree_exp.insert("", "end", values=(
                e["id_expediente"], fmt_fecha_hora(e["fecha_alta"]),
                e["paciente"], e["medico"], e["especialidad"],
                (e["diagnostico"] or "")[:200]))
        self.lbl_exp.config(text=f"Total: {len(datos)} expedientes")

    def _filas_expe(self):
        return [(self.tree_exp.item(i)["values"]) for i in self.tree_exp.get_children()]

    def _exp_pdf_expe(self):
        if not self._filas_expe():
            messagebox.showinfo("Sin datos", "No hay expedientes para exportar.",
                                parent=self); return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
            initialfile="reporte_expedientes.pdf", parent=self)
        if not ruta:
            return
        try:
            exportar_pdf(ruta, "Reporte de Expedientes",
                         ["ID", "Fecha alta", "Paciente", "Médico",
                          "Especialidad", "Diagnóstico"],
                         self._filas_expe(),
                         subtitulo=self._subt_rango(self.exp_desde, self.exp_hasta))
            messagebox.showinfo("PDF generado", f"Archivo:\n{ruta}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _exp_xlsx_expe(self):
        if not self._filas_expe():
            messagebox.showinfo("Sin datos", "No hay expedientes para exportar.",
                                parent=self); return
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")],
            initialfile="reporte_expedientes.xlsx", parent=self)
        if not ruta:
            return
        try:
            exportar_excel(ruta, "Reporte de Expedientes",
                           ["ID", "Fecha alta", "Paciente", "Médico",
                            "Especialidad", "Diagnóstico"],
                           self._filas_expe())
            messagebox.showinfo("Excel generado", f"Archivo:\n{ruta}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    # ------- Tab 3: Resumen --------------------------------------------------
    def _tab_resumen(self):
        f = tk.Frame(self.tab_resumen, bg="white", padx=20, pady=20)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="Resumen general del sistema", bg="white",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")

        self.tarjetas = tk.Frame(f, bg="white"); self.tarjetas.pack(fill="x", pady=15)
        # se llenan en _recargar()

        tk.Label(f, text="Citas por estado:", bg="white",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.tabla_estado = ttk.Treeview(f, columns=("estado", "n"),
                                         show="headings", height=5)
        self.tabla_estado.heading("estado", text="Estado")
        self.tabla_estado.heading("n", text="Cantidad")
        self.tabla_estado.column("estado", width=200)
        self.tabla_estado.column("n", width=120, anchor="center")
        self.tabla_estado.pack(anchor="w")

    def _refrescar_resumen(self):
        for w in self.tarjetas.winfo_children():
            w.destroy()
        try:
            n_pac = Paciente.contar()
            n_med = Medico.contar()
            n_exp = Expediente.contar()
            por_estado = Cita.contar_por_estado()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self); return

        for color, texto, valor in [
            ("#0E9B83", "Pacientes",   n_pac),
            ("#1565C0", "Médicos",     n_med),
            ("#8E44AD", "Expedientes", n_exp),
            ("#E67E22", "Total citas", sum(r["n"] for r in por_estado)),
        ]:
            card = tk.Frame(self.tarjetas, bg=color, padx=18, pady=14)
            card.pack(side="left", padx=8)
            tk.Label(card, text=str(valor), bg=color, fg="white",
                     font=("Segoe UI", 20, "bold")).pack()
            tk.Label(card, text=texto, bg=color, fg="white",
                     font=("Segoe UI", 10)).pack()

        for i in self.tabla_estado.get_children():
            self.tabla_estado.delete(i)
        for r in por_estado:
            self.tabla_estado.insert("", "end", values=(r["estado"], r["n"]))

    def _recargar(self):
        self._recargar_citas()
        self._recargar_expe()
        self._refrescar_resumen()

    @staticmethod
    def _subt_rango(e_desde, e_hasta):
        d = e_desde.get().strip(); h = e_hasta.get().strip()
        if d or h:
            return f"Período: {d or '...'}  →  {h or '...'}"
        return ""
