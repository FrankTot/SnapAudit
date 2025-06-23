import subprocess
import platform
import os

def open_pdf(filepath):
    if not os.path.exists(filepath):
        print(f"Il file {filepath} non esiste.")
        return

    system_platform = platform.system()

    try:
        if system_platform == "Linux":
            subprocess.Popen(["xdg-open", filepath])
        elif system_platform == "Darwin":  # macOS
            subprocess.Popen(["open", filepath])
        elif system_platform == "Windows":
            os.startfile(filepath)
        else:
            print(f"Sistema non supportato per l'apertura automatica: {system_platform}")
    except Exception as e:
        print(f"Errore nell'apertura del PDF: {str(e)}")
