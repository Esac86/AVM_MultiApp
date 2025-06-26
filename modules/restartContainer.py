import tkinter as tk
from tkinter import ttk, messagebox
import json, os, subprocess, paramiko
from functools import partial
from utils.centerWindow import centrar_ventana
from utils.style import setup_style
import threading

CONFIG_FILE = "config.json"
PEM_FILE = "Key.pem"
DOCKER_COMMAND = "sudo docker restart blackout-salud"

style = None

def corregir_permisos_pem(path):
    try:
        subprocess.run(f'icacls "{path}" /inheritance:r', shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'icacls "{path}" /grant:r %USERNAME%:R', shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"Error al corregir permisos:\n{e}")

def ejecutar_comando_ssh(ip):
    if not os.path.exists(PEM_FILE):
        messagebox.showerror("Error", f"No se encontró el archivo {PEM_FILE}")
        return

    corregir_permisos_pem(PEM_FILE)

    try:
        key = paramiko.RSAKey.from_private_key_file(PEM_FILE)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username="ubuntu", pkey=key)

        _, stdout, stderr = ssh.exec_command(DOCKER_COMMAND)
        salida = stdout.read().decode().strip()
        errores = stderr.read().decode().strip()
        ssh.close()

        if errores:
            messagebox.showerror("Error al reiniciar", f"{ip}:\n{errores}")
        else:
            messagebox.showinfo("Éxito", "El contenedor ha sido reiniciado con éxito.")
    except Exception as e:
        messagebox.showerror("Error SSH", str(e))

def mostrar_cargando_y_ejecutar(ip):
    cargando = tk.Toplevel()
    cargando.title("Cargando...")
    cargando.geometry("250x100")
    cargando.resizable(False, False)
    cargando.configure(bg="#1e1e1e")

    # Estilo visual
    label = ttk.Label(cargando, text="Reiniciando...", style="Title.TLabel")
    label.pack(pady=10)

    pb_style = ttk.Style()
    pb_style.theme_use("clam")
    pb_style.configure("dark.Horizontal.TProgressbar",
                       troughcolor="#2e2e2e",
                       background="#0e639c",
                       bordercolor="#1e1e1e",
                       lightcolor="#0e639c",
                       darkcolor="#0e639c")
    
    pb = ttk.Progressbar(cargando, mode="indeterminate", style="dark.Horizontal.TProgressbar")
    pb.pack(pady=10, padx=20, fill="x")
    pb.start()

    centrar_ventana(cargando)

    def tarea():
        ejecutar_comando_ssh(ip)
        cargando.destroy()

    threading.Thread(target=tarea, daemon=True).start()


def mostrar_reinicio_contenedores(root, volver_func):
    global style
    if style is None:
        style = setup_style()

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Reinicio de Contenedores")
    root.geometry("640x480")
    root.resizable(False, False)

    canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
    scroll_y = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas, padding=20, style="Dark.TFrame")

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Soporte para scroll con la rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bound_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbound_to_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", _bound_to_mousewheel)
    canvas.bind("<Leave>", _unbound_to_mousewheel)

    ttk.Label(frame, text="Seleccione un servidor:", style="Title.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(0, 20)
    )

    try:
        with open(CONFIG_FILE, "r") as f:
            servidores = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar {CONFIG_FILE}:\n{e}")
        return

    for i, s in enumerate(servidores):
        nombre = s.get("nombre", "Sin nombre")
        ip = s["ip"]
        col_span = 2 if len(servidores) == 1 else 1
        btn = ttk.Button(frame, text=f"{nombre} ({ip})", width=30,
                         command=lambda ip=ip: mostrar_cargando_y_ejecutar(ip))
        btn.grid(row=(i // 2) + 1, column=i % 2 if len(servidores) > 1 else 0,
                 columnspan=col_span, padx=10, pady=8, sticky="ew")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1 if len(servidores) > 1 else 0)

    final_row = (len(servidores) // 2 + 2) if len(servidores) > 1 else 2
    back_btn = ttk.Button(frame, text="← Volver", width=20, command=volver_func)
    back_btn.grid(row=final_row, column=0, columnspan=2, pady=(30, 0))

    centrar_ventana(root)
