import subprocess
import os
import time
from datetime import datetime, timedelta

def get_active_services():
    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager", "--no-legend"],
            capture_output=True, text=True, check=True
        )
        services = [line.split()[0] for line in result.stdout.strip().split('\n') if line]
        return "\n".join(services) if services else "Nessun servizio attivo trovato."
    except Exception as e:
        return f"Errore nel recupero servizi attivi: {e}"

def get_logged_users():
    try:
        result = subprocess.run(
            ["who"], capture_output=True, text=True, check=True
        )
        users = set()
        for line in result.stdout.strip().split('\n'):
            if line:
                users.add(line.split()[0])
        return "\n".join(sorted(users)) if users else "Nessun utente loggato."
    except Exception as e:
        return f"Errore nel recupero utenti loggati: {e}"

def get_open_ports():
    try:
        # Richiede net-tools o iproute2, usa ss qui
        result = subprocess.run(
            ["ss", "-tuln"], capture_output=True, text=True, check=True
        )
        ports = []
        for line in result.stdout.strip().split('\n')[1:]:
            parts = line.split()
            if len(parts) >= 5:
                ports.append(parts[4])
        return "\n".join(ports) if ports else "Nessuna porta aperta trovata."
    except Exception as e:
        return f"Errore nel recupero porte aperte: {e}"

def get_recent_etc_modifications(days=7):
    try:
        cutoff = time.time() - days * 86400
        modified_files = []
        for root, dirs, files in os.walk("/etc"):
            for file in files:
                path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(path)
                    if mtime > cutoff:
                        modified_files.append(f"{path} - modificato il {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception:
                    continue
        if modified_files:
            return "\n".join(modified_files)
        else:
            return f"Nessuna modifica nei file /etc negli ultimi {days} giorni."
    except Exception as e:
        return f"Errore nel recupero modifiche /etc: {e}"
