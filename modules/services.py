# SnapAudit/modules/services.py

import subprocess
import sys

def get_active_services():
    """
    Esegue 'systemctl list-units --type=service --state=running' e parsifica l'output.
    Restituisce una lista di dizionari, ognuno rappresentante un servizio attivo.
    Include gestione errori.
    """
    print("  Esecuzione comando: systemctl list-units --type=service --state=running")
    try:
        # check=True solleva CalledProcessError se il comando restituisce un codice di uscita non zero
        result = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--state=running'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8' # Specifica encoding per evitare errori
        )
        output_lines = result.stdout.strip().split('\n')

        # Il parsing è basato sul formato standard di systemctl list-units
        # UNIT           LOAD   ACTIVE SUB    DESCRIPTION
        # apparmor.service loaded active exited Load AppArmor profiles
        # ...

        parsed_services = []
        # Salta l'intestazione e la riga di riepilogo finale
        if len(output_lines) > 2:
            # Le prime righe sono l'intestazione, l'ultima è il riepilogo
            service_lines = output_lines[1:-1]

            for line in service_lines:
                # Dividi la linea per spazi, ma fai attenzione agli spazi multipli
                # Usiamo split() senza argomenti che gestisce spazi multipli
                parts = line.split(maxsplit=4) # Dividi al massimo 4 volte per mantenere la descrizione intera

                if len(parts) >= 4: # Assicurati che ci siano almeno le colonne principali
                    service_info = {
                        'UNIT': parts[0].strip(),
                        'LOAD': parts[1].strip(),
                        'ACTIVE': parts[2].strip(),
                        'SUB': parts[3].strip(),
                        'DESCRIPTION': parts[4].strip() if len(parts) > 4 else '' # La descrizione può mancare o contenere spazi
                    }
                    parsed_services.append(service_info)
                # Ignora righe che non corrispondono al formato atteso

        print(f"  Trovati {len(parsed_services)} servizi attivi.")
        return parsed_services

    except FileNotFoundError:
        print("  Errore: Il comando 'systemctl' non è stato trovato.")
        print("  Assicurati che systemd sia in uso e accessibile.")
        return [] # Restituisce una lista vuota in caso di errore
    except subprocess.CalledProcessError as e:
        print(f"  Errore durante l'esecuzione di 'systemctl': {e}")
        print(f"  Stderr: {e.stderr}")
        return [] # Restituisce una lista vuota in caso di errore
    except Exception as e:
        print(f"  Errore generico durante la scansione dei servizi: {e}")
        return [] # Restituisce una lista vuota in caso di errore

