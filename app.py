import tkinter as tk
from tkinter import ttk, messagebox
from modules.restartContainer import mostrar_reinicio_contenedores
from utils.centerWindow import centrar_ventana
from utils.style import setup_style
from utils.updater import chequear_estado_app

def mostrar_proximamente():
    messagebox.showinfo("Próximamente", "Esta funcionalidad estará disponible en futuras versiones.")

def crear_menu_principal(root):
    style = setup_style()

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Herramienta Hospital")
    root.geometry("640x480")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=30)
    frame.pack(expand=True)

    ttk.Button(frame, text="Reiniciar contenedores", width=35,
               command=lambda: mostrar_reinicio_contenedores(root, lambda: crear_menu_principal(root))).pack(pady=15)
    ttk.Button(frame, text="Próximamente", width=35, command=mostrar_proximamente).pack(pady=15)
    ttk.Button(frame, text="Próximamente", width=35, command=mostrar_proximamente).pack(pady=15)

    centrar_ventana(root)

if __name__ == "__main__":
    chequear_estado_app()
    root = tk.Tk()
    root.iconbitmap("icono.ico")
    root.configure(bg="#1e1e1e")

    crear_menu_principal(root)
    root.mainloop()
