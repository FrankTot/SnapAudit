# SnapAudit/main.py

import sys
import os
import time
import subprocess
import platform # Per controllare l'OS e aprire il file

# Importa i moduli di scansione
from modules import services, ports, users, files, report, permissions # Importa anche il nuovo modulo

# --- Funzione per l'Animazione di Caricamento ---
def loading_animation(duration=3):
    """
    Mostra un'animazione di caricamento fittizia nel terminale.

    Args:
        duration (int): La durata in secondi dell'animazione.
    """
    chars = "|/-\\"
    end_time = time.time() + duration
    sys.stdout.write("Generazione report... ")
    sys.stdout.flush() # Assicura che il testo venga stampato subito
    while time.time() < end_time:
        for char in chars:
            # Utilizza \r per tornare all'inizio della riga e sovrascrivere
            sys.stdout.write('\r' + "Generazione report... " + char)
            sys.stdout.flush()
            time.sleep(0.1) # Piccola pausa per l'animazione
    sys.stdout.write('\r' + "Generazione report... Fatto!   \n") # Sostituisce l'animazione con "Fatto!" e spazi per pulire la riga


# --- Funzione per Aprire Automaticamente il File ---
def open_report_file(filepath):
    """
    Prova ad aprire il file del report con l'applicazione predefinita del sistema operativo.

    Args:
        filepath (str): Il percorso del file da aprire.
    """
    try:
        if platform.system() == "Linux":
            # xdg-open è il comando standard su molti desktop Linux
            subprocess.run(["xdg-open", filepath], check=True)
        elif platform.system() == "Darwin": # macOS
            subprocess.run(["open", filepath], check=True) # 'open' è il comando su macOS
        elif platform.system() == "Windows":
            os.startfile(filepath) # Metodo specifico di Windows
        else:
            print(f"Impossibile aprire automaticamente il file su questo sistema operativo ({platform.system()}).")
            print(f"Apri manualmente il report: {filepath}")
    except FileNotFoundError:
         print(f"Comando per aprire il file non trovato sul tuo sistema.")
         print(f"Apri manualmente il report: {filepath}")
    except subprocess.CalledProcessError as e:
         print(f"Errore durante l'esecuzione del comando di apertura file: {e}")
         print(f"Apri manualmente il report: {filepath}")
    except Exception as e:
         print(f"Errore generico nell'apertura automatica del file: {e}")
         print(f"Apri manualmente il report: {filepath}")


# --- Funzioni per il Menu ---
def display_menu():
    """Mostra il menu principale delle opzioni di scansione all'utente."""
    print("\n" + "="*40)
    print("        SnapAudit Menu")
    print("="*40)
    print("1. Scansiona Servizi Attivi")
    print("2. Scansiona Porte Aperte")
    print("3. Scansiona Utenti Loggati")
    print("4. Scansiona Modifiche File Recenti (/etc)")
    print("5. Controlla Permessi File Critici") # Opzione per il nuovo modulo
    # Aggiungi qui altre opzioni per i moduli futuri

    print("-" * 40)
    print("A. Esegui TUTTE le Scansioni")
    print("Q. Esci")
    print("="*40)

def get_user_selection():
    """Ottiene la scelta dell'utente dal menu e la valida."""
    while True:
        choice = input("Seleziona un'opzione: ").strip().lower()
        # Lista delle scelte valide (aggiorna se aggiungi opzioni)
        valid_choices = ['1', '2', '3', '4', '5', 'a', 'q'] # Aggiunto '5'
        if choice in valid_choices:
            return choice
        else:
            print("Opzione non valida. Inserisci il numero o la lettera corrispondente.")

# --- Funzione Principale ---
def main():
    # Impostazioni di base (possono diventare argomenti da riga di comando in futuro)
    output_dir = 'reports'
    report_format = 'html' # Impostiamo di default HTML per una migliore grafica

    print("Benvenuto in SnapAudit!")

    while True: # Loop principale del menu
        display_menu()
        choice = get_user_selection()

        if choice == 'q':
            print("Uscita da SnapAudit. Arrivederci!")
            break # Esci dal loop principale

        selected_modules = []
        # Mappa la scelta dell'utente ai nomi interni dei moduli
        if choice == '1' or choice == 'a':
            selected_modules.append('services')
        if choice == '2' or choice == 'a':
            selected_modules.append('ports')
        if choice == '3' or choice == 'a':
            selected_modules.append('users')
        if choice == '4' or choice == 'a':
            selected_modules.append('files')
        if choice == '5' or choice == 'a':
             selected_modules.append('permissions') # Aggiunge il nuovo modulo se selezionato
        # Aggiungi qui la mappatura per i moduli futuri

        if not selected_modules:
             print("Nessuna scansione selezionata. Riprova o esci.")
             continue # Torna all'inizio del loop del menu

        print("\nInizio scansione(i) selezionata(i)...")

        # Raccogli i dati solo per i moduli selezionati
        data = {}
        # Esegui le scansioni e salva i dati parsati nel dizionario 'data'
        if 'services' in selected_modules:
             print("Scansionando Servizi Attivi...")
             data['Servizi Attivi'] = services.get_active_services()
             print("Scansione Servizi Attivi completata.")
        if 'ports' in selected_modules:
             print("Scansionando Porte Aperte...")
             data['Porte Aperte'] = ports.get_open_ports()
             print("Scansione Porte Aperte completata.")
        if 'users' in selected_modules:
             print("Scansionando Utenti Loggati...")
             data['Utenti Loggati'] = users.get_logged_users()
             print("Scansione Utenti Loggati completata.")
        if 'files' in selected_modules:
             print("Scansionando Modifiche Recenti (/etc)...")
             # Puoi rendere '/etc' un parametro configurabile in futuro
             data['Modifiche Recenti (/etc)'] = files.get_recent_file_changes('/etc')
             print("Scansione Modifiche File completata.")
        if 'permissions' in selected_modules:
             print("Controllando Permessi File Critici...")
             data['Permessi File Critici'] = permissions.check_critical_file_permissions()
             print("Controllo Permessi File completato.")
        # Chiama le funzioni dei moduli futuri qui

        # Assicurati che ci siano dati da riportare prima di generare il report
        if not data:
            print("Nessun dato raccolto. Impossibile generare un report.")
            continue # Torna al menu

        print("\nPreparazione report...")
        loading_animation(duration=3) # Esegui l'animazione prima di generare il report

        # Genera il report utilizzando i dati raccolti e il formato scelto
        report_path = report.generate_report(data, output_dir=output_dir, format=report_format)

        # Controlla se il report è stato generato con successo prima di provare ad aprirlo
        if report_path:
            print(f"✅ Report generato con successo: {report_path}")
            print("Apertura report...")
            open_report_file(report_path)
        else:
            print("❌ Errore durante la generazione del report.")

        # Il loop del menu si ripete qui, chiedendo una nuova scelta

if __name__ == '__main__':
    # Controlla se lo script è eseguito come root per le scansioni che lo richiedono
    # Questo è un controllo semplice, potresti volerlo affinare per ogni modulo
    # if os.geteuid() != 0:
    #     print("AVVISO: Alcune scansioni potrebbero richiedere permessi di root per funzionare correttamente.")
    #     print("Esegui lo script con 'sudo python3 main.py' per risultati completi.")

    main()
