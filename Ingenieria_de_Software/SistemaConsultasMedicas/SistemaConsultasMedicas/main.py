"""
main.py - Punto de entrada del sistema
======================================
Inicia el ciclo Login → Menú Principal → (Logout → Login).
"""
from vistas.login import LoginView
from vistas.menu_principal import MenuPrincipal


def abrir_menu(usuario):
    app = MenuPrincipal(on_logout=abrir_login)
    app.mainloop()


def abrir_login():
    app = LoginView(on_success=abrir_menu)
    app.mainloop()


if __name__ == "__main__":
    abrir_login()
