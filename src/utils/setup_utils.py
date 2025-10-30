# setup_utils.py
def setup_window(window):
    """Configura a janela para iniciar maximizada de forma segura."""
    try:
        window.state("zoomed")
    except Exception:
        pass

    try:
        window.attributes("-fullscreen", False)
        window.overrideredirect(False)
    except Exception:
        pass

    window.update_idletasks()
    if window.state() != "zoomed":
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        safe_width = max(800, width - 8)
        safe_height = max(600, height - 48)
        window.geometry(f"{safe_width}x{safe_height}+0+0")

    def restore_window(event=None):
        try:
            window.state("normal")
        except Exception:
            pass
        window.geometry("900x600")

    window.bind("<Escape>", restore_window)