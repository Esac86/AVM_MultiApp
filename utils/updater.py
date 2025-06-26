import urllib.request
import json
import os
import sys
import subprocess
from tkinter import messagebox
import time

STATUS_URL = "https://raw.githubusercontent.com/Esac86/AVM_MultiApp/main/status.json"
VERSION_LOCAL = "1.0.0"
DOWNLOAD_PATH = "AVM_MultiApp_Update.exe"

def chequear_estado_app():
    try:
        url = f"{STATUS_URL}?t={int(time.time())}" 
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())

            if not data.get("active", False):
                messagebox.showerror("Aplicación deshabilitada", "Esta aplicación no está disponible.\nConsulta con soporte.")
                sys.exit()

            version_remota = data.get("version")
            if version_remota and version_remota != VERSION_LOCAL:
                url = data.get("url")
                if url and messagebox.askyesno("Actualización disponible", f"Versión nueva {version_remota} disponible.\n¿Deseas descargarla e instalarla ahora?"):
                    descargar_y_ejecutar(url)
                    eliminar_actual()
                    sys.exit()

    except Exception as e:
        messagebox.showwarning("Error de conexión", f"No se pudo verificar el estado de la app.\n\n{e}")

def descargar_y_ejecutar(url):
    try:
        if os.path.exists(DOWNLOAD_PATH):
            os.remove(DOWNLOAD_PATH)

        with urllib.request.urlopen(url) as response, open(DOWNLOAD_PATH, 'wb') as out_file:
            out_file.write(response.read())

        subprocess.Popen([DOWNLOAD_PATH], shell=True)
        messagebox.showinfo("Actualización iniciada", "Se descargó y ejecutó la nueva versión. Cerrando esta...")

    except Exception as e:
        messagebox.showerror("Error de actualización", f"No se pudo descargar o ejecutar la nueva versión:\n\n{e}")

def eliminar_actual():
    try:
        actual_path = sys.argv[0]
        if actual_path.endswith(".exe"):
            bat_content = f"""@echo off
ping 127.0.0.1 -n 3 > nul
del "{actual_path}"
del "%~f0"
"""
            with open("delete_self.bat", "w") as f:
                f.write(bat_content)
            subprocess.Popen("delete_self.bat", shell=True)

    except Exception as e:
        print(f"Error eliminando ejecutable actual: {e}")
