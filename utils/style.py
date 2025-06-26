from tkinter import ttk

def setup_style():
    style = ttk.Style()
    style.theme_use("clam")

    # Colores estilo VS Code oscuro
    bg = "#1e1e1e"
    fg = "#d4d4d4"
    accent = "#0e639c"
    accent_hover = "#1177bb"

    # Fondo general
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 12))
    style.configure("Title.TLabel", background=bg, foreground="#ffffff", font=("Segoe UI", 16, "bold"))
    style.configure("Dark.TFrame", background="#1e1e1e")

    # Botones
    style.configure("TButton",
                    background=accent,
                    foreground="#ffffff",
                    font=("Segoe UI", 11),
                    padding=8,
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor=accent)

    style.map("TButton",
              background=[("active", accent_hover), ("disabled", "#3c3c3c")],
              foreground=[("disabled", "#7f7f7f")])

    return style
