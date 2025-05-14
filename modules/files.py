# SnapAudit/modules/files.py

import subprocess
import sys
import os
from datetime import datetime, timedelta

def get_recent_file_changes(path='/etc', days=1):
    """
    Esegue 'find' per trovare file modificati di recente in un percorso specificato.
    Restituisce una lista di dizionari con il percorso del file e la data di ultima modifica.
    Include gestione errori.

    Args:
        path (str): Il percorso della directory da scansionare.
        days (int): Il numero di giorni indietro da considerare per le modifiche recenti.
    """
    print(f"  Esecuzione comando: find {path} -type f -mtime -{days}")
    try:
        # find path -type f -mtime -days
        # -type f: cerca solo file
        # -mtime -days: cerca file modificati negli ultimi 'days' giorni (meno di 'days')
        result = subprocess.run(
            ['find', path, '-type', 'f', '-mtime', f'-{days}'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output_lines = result.stdout.strip().split('\n')

        parsed_files = []
        if output_lines and output_lines != ['']: # Controlla se c'è output e non è solo una riga vuota
            for filepath in output_lines:
                filepath = filepath.strip()
                if filepath: # Assicurati che la riga non sia vuota dopo lo strip
                    try:
                        # Ottieni la data di ultima modifica del file
                        mtime_timestamp = os.path.getmtime(filepath)
                        mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                        parsed_files.append({
                            'Percorso File': filepath,
                            'Ultima Modifica': mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    except FileNotFoundError:
                        # Questo potrebbe accadere se un file viene cancellato tra il find e os.path.getmtime
                        print(f"  Avviso: File non trovato durante l'ottenimento della data di modifica: {filepath}")
                        parsed_files.append({
                            'Percorso File': filepath,
                            'Ultima Modifica': 'Errore: File non trovato'
                        })
                    except Exception as e:
                        print(f"  Errore nell'ottenere la data di modifica per {filepath}: {e}")
                        parsed_files.append({
                            'Percorso File': filepath,
                            'Ultima Modifica': f'Errore: {e}'
                        })


        print(f"  Trovati {len(parsed_files)} file modificati negli ultimi {days} giorni in {path}.")
        return parsed_files

    except FileNotFoundError:
        print("  Errore: Il comando 'find' non è stato trovato.")
        return [] # Restituisce una lista vuota in caso di errore
    except subprocess.CalledProcessError as e:
        print(f"  Errore durante l'esecuzione di 'find': {e}")
        print(f"  Stderr: {e.stderr}")
        # find restituisce codice 1 se non trova nulla, ma check=True lo considera un errore.
        # Se stderr è vuoto, potrebbe essere solo che non ha trovato file.
        if not e.stderr:
             print(f"  Nessun file modificato trovato negli ultimi {days} giorni in {path}.")
             return []
        return [] # Restituisce una lista vuota in caso di errore
    except Exception as e:
        print(f"  Errore generico durante la scansione dei file: {e}")
        return [] # Restituisce una lista vuota in caso di errore
