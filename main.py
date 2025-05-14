# SnapAudit/main.py

import sys
import os
import time
import subprocess
import platform # Per controllare l'OS e aprire il file
import textwrap # Per formattare il banner
import glob # Per trovare file

# Importa i moduli di scansione
from modules import services, ports, users, files, report, permissions

# --- Banner ASCII ---
# Ho leggermente aggiustato il banner per adattarlo meglio al codice
BANNER = """                                                                                                                 
                                                                                                                       
      *******                                               **                           **                      
    *       ***                                          *****                            **     *         *     
   *         **                                         *  ***                            **    ***       **     
   **        *                                             ***                            **     *        **     
    ***                                     ****          *  **       **   ****           **            ******** 
   ** ***        ***  ****       ****      * ***  *       *  **        **    ***  *   *** **   ***     ********  
    *** ***       **** **** *   * ***  *  *   ****       *    **       **     ****   *********  ***       **     
      *** ***      **   ****   *   ****  **    **        *    **       **      **   **   ****    **       **     
        *** ***    **    **   **    **   **    **       *      **      **      **   **    **     **       **     
          ** ***   **    **   **    **   **    **       *********      **      **   **    **     **       **     
           ** **   **    **   **    **   **    **      *        **     **      **   **    **     **       **     
            * *    **    **   **    **   **    **      *        **     **      **   **    **     **       **     
  ***        *     **    **   **    **   *******      *****      **     ******* **  **    **     **       **     
 *  *********      ***   ***   ***** **  ******      *   ****    ** *    *****   **  *****       *** *     **    
*     *****         ***   ***   ***   ** **         *     **      **                  ***         ***            
*                                        **         *                                                            
 **                                      **          **                                                          
                                          **                                                                     
                                                                                                                 
                                                                                                                 """

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


# --- Funzione per Aprire Automaticamente il File (Usata su richiesta) ---
def open_report_file(filepath):
    """
    Prova ad aprire il file del report con l'applicazione predefinita del sistema operativo.

    Args:
        filepath (str): Il percorso del file da aprire.
    """
    try:
        if not os.path.exists(filepath):
            print(f"Errore: Il file '{filepath}' non esiste.")
            return

        print(f"Tentativo di apertura del file: {filepath}")
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
         print(f"Stderr: {e.stderr.strip()}") # Mostra stderr se disponibile
         print(f"Apri manualmente il report: {filepath}")
    except Exception as e:
         print(f"Errore generico nell'apertura automatica del file: {e}")
         print(f"Apri manualmente il report: {filepath}")

# --- Funzione per trovare l'ultimo report ---
def find_latest_report(output_dir='reports', extension='.txt'):
    """
    Trova il percorso dell'ultimo report generato nella directory specificata.

    Args:
        output_dir (str): La directory dove cercare i report.
        extension (str): L'estensione dei file di report (es. '.txt', '.html').

    Returns:
        str: Il percorso completo dell'ultimo file di report, o None se non trovato.
    """
    # Costruisce il pattern di ricerca
    search_pattern = os.path.join(output_dir, f'snap_report_*{extension}')
    # Trova tutti i file che corrispondono al pattern
    list_of_files = glob.glob(search_pattern)

    if not list_of_files:
        return None

    # Ordina i file per data di ultima modifica (il più recente sarà l'ultimo)
    # key=os.path.getctime usa il tempo di creazione, key=os.path.getmtime usa il tempo di modifica
    latest_file = max(list_of_files, key=os.path.getmtime)

    return latest_file


# --- Funzione per Visualizzare i Dati nel Terminale (Tabella Semplice) ---
def display_data_in_terminal(data: dict):
    """
    Visualizza i dati raccolti in una tabella testuale formattata nel terminale.
    Questa è una versione semplice senza colori ANSI per massima compatibilità.

    Args:
        data (dict): Il dizionario con i dati raccolti per sezione.
    """
    print("\n" + "="*60)
    print("        Risultati Scansione SnapAudit")
    print("="*60)

    for section, content in data.items():
        print(f"\n--- {section.upper()} ---")

        if isinstance(content, list) and content: # Se è una lista non vuota
            if isinstance(content[0], dict): # Se gli elementi sono dizionari (per tabelle)
                # Ottieni le intestazioni (chiavi del primo dizionario)
                headers = list(content[0].keys())
                # Calcola la larghezza massima per ogni colonna
                col_widths = {header: len(header) for header in headers}
                for item in content:
                    for header in headers:
                        # Assicurati che il valore sia una stringa per calcolare la lunghezza
                        value_str = str(item.get(header, ''))
                        col_widths[header] = max(col_widths[header], len(value_str))

                # Disegna l'intestazione della tabella
                header_line = "+-" + "-+-".join("-" * col_widths[h] for h in headers) + "-+"
                print(header_line)
                header_row = "| " + " | ".join(h.ljust(col_widths[h]) for h in headers) + " |"
                print(header_row)
                print(header_line)

                # Disegna le righe dei dati
                for item in content:
                    row_values = []
                    for header in headers:
                        value_str = str(item.get(header, '')).ljust(col_widths[header])
                        row_values.append(value_str)
                    print("| " + " | ".join(row_values) + " |")

                # Disegna la riga inferiore della tabella
                print(header_line)

            else: # Se è una lista di altri tipi (es. stringhe)
                for item in content:
                    print(f"- {item}")
        elif isinstance(content, list) and not content: # Se è una lista vuota
             print("  Nessun dato trovato per questa sezione.")
        else: # Contenuto non è una lista (testo grezzo o altro)
            # Usa textwrap per indentare il testo grezzo
            indented_text = textwrap.indent(str(content), "  ")
            print(indented_text)

    print("\n" + "="*60)
    print("        Fine Risultati")
    print("="*60 + "\n")


# --- Funzioni per il Menu ---
def display_menu():
    """Mostra il menu principale delle opzioni di scansione all'utente con il banner."""
    print(BANNER) # Mostra il banner
    print("\n" + "="*50) # Aumentato la larghezza
    print("        SnapAudit Menu Principale")
    print("="*50)
    print("  1. Scansiona Servizi Attivi")
    print("  2. Scansiona Porte Aperte")
    print("  3. Scansiona Utenti Loggati")
    print("  4. Scansiona Modifiche File Recenti (/etc)")
    print("  5. Controlla Permessi File Critici") # Opzione per il nuovo modulo
    # Aggiungi qui altre opzioni per i moduli futuri

    print("-" * 50) # Aumentato la larghezza
    print("  A. Esegui TUTTE le Scansioni")
    print("  O. Apri Ultimo Report Generato") # Nuova opzione per aprire il report
    print("  Q. Esci")
    print("="*50) # Aumentato la larghezza

def get_user_selection():
    """Ottiene la scelta dell'utente dal menu e la valida."""
    while True:
        choice = input("Seleziona un'opzione (1-5, A, O, Q): ").strip().lower() # Aggiunto 'O'
        # Lista delle scelte valide (aggiorna se aggiungi opzioni)
        valid_choices = ['1', '2', '3', '4', '5', 'a', 'o', 'q'] # Aggiunto 'o'
        if choice in valid_choices:
            return choice
        else:
            print("Opzione non valida. Inserisci il numero o la lettera corrispondente.")

# --- Funzione Principale ---
def main():
    # Impostazioni di base
    output_dir = 'reports'
    report_format_file = 'txt' # Il file report sarà sempre TXT

    # Assicurati che la directory dei report esista all'avvio
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Benvenuto in SnapAudit!")

    while True: # Loop principale del menu
        display_menu()
        choice = get_user_selection()

        if choice == 'q':
            print("Uscita da SnapAudit. Arrivederci!")
            break # Esci dal loop principale

        elif choice == 'o': # Gestisce la nuova opzione "Apri Ultimo Report"
            print("\nRicerca ultimo report generato...")
            latest_report_path = find_latest_report(output_dir=output_dir, extension=f'.{report_format_file}') # Cerca report TXT
            if latest_report_path:
                open_report_file(latest_report_path)
            else:
                print(f"Nessun report '{report_format_file}' trovato nella directory '{output_dir}'.")
            continue # Torna al menu dopo aver provato ad aprire il report

        # Se la scelta non è 'q' o 'o', allora è una o più scansioni
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
             # Questo caso non dovrebbe verificarsi con le scelte attuali, ma è una buona pratica
             print("Nessuna scansione selezionata. Riprova o esci.")
             continue # Torna all'inizio del loop del menu

        print("\nInizio scansione(i) selezionata(i)...")

        # Raccogli i dati solo per i moduli selezionati
        data = {}
        # Esegui le scansioni e salva i dati parsati nel dizionario 'data'
        if 'services' in selected_modules:
             print("  Scansionando Servizi Attivi...")
             # Assumi che get_active_services() ora restituisca dati PARSATI (lista di dict)
             data['Servizi Attivi'] = services.get_active_services()
             print("  Scansione Servizi Attivi completata.")
        if 'ports' in selected_modules:
             print("  Scansionando Porte Aperte...")
             # Assumi che get_open_ports() ora restituisca dati PARSATI (lista di dict)
             data['Porte Aperte'] = ports.get_open_ports()
             print("  Scansione Porte Aperte completata.")
        if 'users' in selected_modules:
             print("  Scansionando Utenti Loggati...")
             # Assumi che get_logged_users() ora restituisca dati PARSATI (lista di dict)
             data['Utenti Loggati'] = users.get_logged_users()
             print("  Scansione Utenti Loggati completata.")
        if 'files' in selected_modules:
             print("  Scansionando Modifiche Recenti (/etc)...")
             # Puoi rendere '/etc' un parametro configurabile in futuro
             # Assumi che get_recent_file_changes() ora restituisca dati PARSATI (lista di dict)
             data['Modifiche Recenti (/etc)'] = files.get_recent_file_changes('/etc')
             print("  Scansione Modifiche File completata.")
        if 'permissions' in selected_modules:
             print("  Controllando Permessi File Critici...")
             # Assumi che check_critical_file_permissions() ora restituisca dati PARSATI (lista di dict)
             data['Permessi File Critici'] = permissions.check_critical_file_permissions()
             print("  Controllo Permessi File completato.")
        # Chiama le funzioni dei moduli futuri qui

        # Assicurati che ci siano dati da riportare prima di generare il report o visualizzare
        if not data or all(not content for content in data.values()):
            print("\nNessun dato raccolto dalle scansioni selezionate. Impossibile generare un report o visualizzare risultati.")
            continue # Torna al menu

        print("\nPreparazione report e visualizzazione...")
        loading_animation(duration=3) # Esegui l'animazione prima di generare il report/visualizzare

        # Genera il report TXT nel file
        report_path = report.generate_report(data, output_dir=output_dir, format=report_format_file)

        # Controlla se il report file è stato generato con successo
        if report_path:
            print(f"✅ Report testuale generato con successo: {report_path}")
        else:
            print("❌ Errore durante la generazione del report testuale.")

        # Visualizza i dati nel terminale
        display_data_in_terminal(data)

        # Il loop del menu si ripete qui, chiedendo una nuova scelta

if __name__ == '__main__':
    # Controlla se lo script è eseguito come root per le scansioni che lo richiedono
    # Questo è un controllo semplice, potresti volerlo affinare per ogni modulo
    # if os.geteuid() != 0:
    #     print("AVVISO: Alcune scansioni (es. permessi file critici) potrebbero richiedere permessi di root per funzionare correttamente.")
    #     print("Esegui lo script con 'sudo python3 main.py' per risultati completi.")

    main()
