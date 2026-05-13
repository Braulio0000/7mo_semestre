"""
vistas/login.py - Ventana de Inicio de Sesión
"""
import tkinter as tk
from tkinter import ttk, messagebox

from controladores.auth import Sesion
from config import APP_NAME, APP_VERSION


class LoginView(tk.Tk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title(f"{APP_NAME} — Iniciar Sesión")
        self.geometry("420x400")
        self.resizable(False, False)
        self.configure(bg="#0E4D64")

        self._construir()
        self._centrar()
        self.bind("<Return>", lambda e: self._login())

    def _centrar(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _construir(self):
        # Panel central
        panel = tk.Frame(self, bg="white", padx=30, pady=25)
        panel.place(relx=0.5, rely=0.5, anchor="center", width=360, height=340)

        tk.Label(panel, text="🩺", bg="white", font=("Segoe UI", 36)).pack(pady=(0, 5))
        tk.Label(panel, text="Iniciar Sesión", bg="white",
                 font=("Segoe UI", 16, "bold"), fg="#0E4D64").pack()
        tk.Label(panel, text=APP_NAME, bg="white",
                 font=("Segoe UI", 9), fg="#666").pack(pady=(0, 15))

        tk.Label(panel, text="Usuario:", bg="white",
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x")
        self.txt_user = ttk.Entry(panel, font=("Segoe UI", 11))
        self.txt_user.pack(fill="x", pady=(2, 10), ipady=4)
        self.txt_user.focus()

        tk.Label(panel, text="Contraseña:", bg="white",
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x")
        self.txt_pass = ttk.Entry(panel, show="•", font=("Segoe UI", 11))
        self.txt_pass.pack(fill="x", pady=(2, 15), ipady=4)

        btn = tk.Button(panel, text="INICIAR SESIÓN", bg="#0E4D64", fg="white",
                        font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2",
                        activebackground="#0A3A4D", activeforeground="white",
                        command=self._login)
        btn.pack(fill="x", ipady=8)

        tk.Label(panel, text=f"v{APP_VERSION}  •  admin/admin123  recep/recep123",
                 bg="white", fg="#999",
                 font=("Segoe UI", 8)).pack(pady=(15, 0))

    def _login(self):
        user = self.txt_user.get().strip()
        pwd = self.txt_pass.get()
        if not user or not pwd:
            messagebox.showwarning("Datos incompletos", "Ingresa usuario y contraseña.")
            return
        try:
            u = Sesion.iniciar(user, pwd)
        except RuntimeError as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        if u is None:
            messagebox.showerror("Credenciales incorrectas",
                                 "Usuario o contraseña inválidos.")
            self.txt_pass.delete(0, "end")
            return
        self.destroy()
        self.on_success(u)
