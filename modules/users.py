# SnapAudit/modules/users.py

import subprocess
import sys

def get_logged_users():
    """
    Esegue 'who' e parsifica l'output per ottenere una lista di utenti loggati.
    Restituisce una lista di dizionari, ognuno rappresentante una sessione utente loggata.
    Include gestione errori.
    """
    print("  Esecuzione comando: who")
    try:
        # 'who' mostra chi è loggato e da dove
        # user     tty      date time        (host)
        # tuo_utente :0       2023-10-27 08:00 (:0)
        # tuo_utente pts/0    2023-10-27 08:01 (192.168.1.100)
        # ...

        result = subprocess.run(
            ['who'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output_lines = result.stdout.strip().split('\n')

        parsed_users = []
        if output_lines: # Controlla se c'è output
            for line in output_lines:
                # Dividi la linea per spazi, gestendo spazi multipli
                parts = line.split(maxsplit=4) # Dividi al massimo 4 volte per catturare data/ora e host

                if len(parts) >= 4: # Assicurati che ci siano almeno le colonne principali (utente, tty, data, ora)
                     # Ricostruisci data e ora se sono in colonne separate
                    datetime_str = f"{parts[2].strip()} {parts[3].strip()}"
                    user_info = {
                        'Utente': parts[0].strip(),
                        'Terminale (TTY)': parts[1].strip(),
                        'Data e Ora Login': datetime_str,
                        'Host Remoto': parts[4].strip().strip('()') if len(parts) > 4 else 'Locale' # Rimuove le parentesi dall'host
                    }
                    parsed_users.append(user_info)
                # Ignora righe che non corrispondono al formato atteso

        print(f"  Trovati {len(parsed_users)} utenti loggati.")
        return parsed_users

    except FileNotFoundError:
        print("  Errore: Il comando 'who' non è stato trovato.")
        return [] # Restituisce una lista vuota in caso di errore
    except subprocess.CalledProcessError as e:
        print(f"  Errore durante l'esecuzione di 'who': {e}")
        print(f"  Stderr: {e.stderr}")
        return [] # Restituisce una lista vuota in caso di errore
    except Exception as e:
        print(f"  Errore generico durante la scansione degli utenti loggati: {e}")
        return [] # Restituisce una lista vuota in caso di errore
