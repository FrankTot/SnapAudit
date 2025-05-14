# SnapAudit/modules/report.py

from datetime import datetime
import os
import sys # Importa sys per stderr

# Assumi che questo modulo riceva dati PARSATI e STRUTTURATI
# come liste di dizionari dai moduli di scansione.

def generate_report(data: dict, output_dir='reports', format='txt'): # Imposta TXT come default
    """
    Genera un report in formato testuale o HTML.
    Accetta dati strutturati (es. liste di dizionari).

    Args:
        data (dict): Un dizionario dove le chiavi sono i nomi delle sezioni
                     e i valori sono i dati raccolti (preferibilmente liste di dizionari).
        output_dir (str): La directory dove salvare il report.
        format (str): Il formato del report ('txt' o 'html').

    Returns:
        str: Il percorso completo del file del report generato, o None in caso di errore.
    """
    print(f"  Generazione report file in formato '{format}'...")
    try:
        # Crea la directory di output se non esiste
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"  Creata directory di output: {output_dir}")

        # Genera il timestamp per il nome del file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if format == 'txt':
            filename = os.path.join(output_dir, f'snap_report_{timestamp}.txt')
            with open(filename, 'w', encoding='utf-8') as f: # Specifica encoding
                f.write(f"SnapAudit Report - {timestamp}\n")
                f.write("="*60 + "\n")
                for section, content in data.items():
                    f.write(f"\n[ {section.upper()} ]\n")
                    f.write("-" * (len(section) + 4) + "\n") # Sottolineatura per la sezione
                    # Gestisci se il contenuto è una lista (dati parsati) o testo grezzo
                    if isinstance(content, list):
                        if content: # Se la lista non è vuota
                            # Stampa le intestazioni se gli elementi sono dizionari
                            if isinstance(content[0], dict):
                                # Usa le chiavi del primo dizionario come intestazioni
                                headers = list(content[0].keys())
                                # Calcola la larghezza massima per ogni colonna per allineamento
                                col_widths = {header: len(header) for header in headers}
                                for item in content:
                                    for header in headers:
                                        value_str = str(item.get(header, ''))
                                        col_widths[header] = max(col_widths[header], len(value_str))

                                # Scrivi l'intestazione della tabella nel file TXT
                                header_line = "+-" + "-+-".join("-" * col_widths[h] for h in headers) + "-+"
                                f.write(header_line + "\n")
                                header_row = "| " + " | ".join(h.ljust(col_widths[h]) for h in headers) + " |"
                                f.write(header_row + "\n")
                                f.write(header_line + "\n")

                                # Scrivi le righe dei dati nel file TXT
                                for item in content:
                                    row_values = []
                                    for header in headers:
                                        value_str = str(item.get(header, '')).ljust(col_widths[header])
                                        row_values.append(value_str)
                                    f.write("| " + " | ".join(row_values) + " |\n")

                                # Scrivi la riga inferiore della tabella nel file TXT
                                f.write(header_line + "\n")

                            else: # Se è una lista di altri tipi (es. stringhe)
                                for item in content:
                                    f.write(str(item) + "\n")
                        else: # Se la lista è vuota
                            f.write("Nessun dato trovato per questa sezione.\n")
                    else: # Contenuto non è una lista (testo grezzo o altro)
                        f.write(str(content) + "\n")
                f.write("\n" + "="*60 + "\n") # Fine report
                f.write(f"Report generato il: {timestamp}\n")

        elif format == 'html':
            # Mantieni la generazione HTML come opzione, anche se non è quella preferita dall'utente ora
            filename = os.path.join(output_dir, f'snap_report_{timestamp}.html')
            with open(filename, 'w', encoding='utf-8') as f: # Specifica encoding
                f.write("<!DOCTYPE html>\n")
                f.write("<html lang='en'>\n")
                f.write("<head>\n")
                f.write("    <meta charset='UTF-8'>\n")
                f.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
                f.write(f"    <title>SnapAudit Security Report - {timestamp}</title>\n")
                # --- CSS per una grafica carina e colori ---
                f.write("    <style>\n")
                f.write("        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #e9ecef; color: #343a40; }\n")
                f.write("        .container { max-width: 1000px; margin: 20px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); }\n")
                f.write("        h1 { color: #007bff; text-align: center; margin-bottom: 30px; padding-bottom: 10px; border-bottom: 2px solid #007bff; }\n")
                f.write("        h2 { margin-top: 25px; padding-bottom: 8px; border-bottom: 1px solid #ccc; }\n")

                # Stili specifici per sezioni con colori e icone (opzionale, richiede font/icone)
                f.write("        .section { margin-bottom: 30px; padding: 15px; border-left: 5px solid; border-radius: 5px; background-color: #f8f9fa; }\n") # Stile base sezione
                f.write("        .section h2 { margin-top: 0; border-bottom: none; padding-bottom: 0; display: flex; align-items: center; }\n") # Rimuove bordo inferiore h2 dentro la sezione, usa flex per allineamento icona/testo
                f.write("        .section h2 i { margin-right: 10px; font-size: 1.2em; }\n") # Spazio e dimensione per l'icona (se usi font awesome o simili)

                # Mappa nomi sezione a colori e classi CSS
                f.write("        .section.services { border-color: #28a745; background-color: #d4edda; color: #155724; }\n") # Verde
                f.write("        .section.ports { border-color: #dc3545; background-color: #f8d7da; color: #721c24; }\n") # Rosso/Rosato
                f.write("        .section.users { border-color: #ffc107; background-color: #fff3cd; color: #856404; }\n") # Giallo
                f.write("        .section.files { border-color: #17a2b8; background-color: #d1ecf1; color: #0c5460; }\n") # Ciano
                f.write("        .section.permissions { border-color: #6f42c1; background-color: #e2d9eb; color: #4f327f; }\n") # Viola
                # Aggiungi stili per i nuovi moduli qui

                f.write("        table { border-collapse: collapse; width: 100%; margin-top: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05); }\n")
                f.write("        th, td { border: 1px solid #dee2e6; padding: 12px; text-align: left; }\n")
                f.write("        th { background-color: #007bff; color: white; font-weight: bold; }\n")
                f.write("        tr:nth-child(even) { background-color: #e9ecef; }\n") # Righe alternate
                f.write("        tr:hover { background-color: #d6d8db; }\n") # Hover sulle righe
                f.write("        pre { background-color: #e9ecef; padding: 15px; border: 1px solid #ced4da; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; border-radius: 5px; margin-top: 10px; }\n") # Preformattato
                f.write("        .info-text { font-size: 0.9em; color: #6c757d; margin-top: 20px; text-align: center; }\n") # Testo informativo in basso

                # Stile specifico per avvisi/problemi nel report (es. permessi)
                f.write("        .warning { color: #dc3545; font-weight: bold; }\n") # Rosso per gli avvisi
                f.write("        .ok { color: #28a745; }\n") # Verde per OK

                f.write("    </style>\n")
                # Puoi aggiungere link a librerie di icone qui, es. Font Awesome (richiede connessione internet)
                # f.write("    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                f.write("    <div class='container'>\n")
                f.write(f"    <h1>SnapAudit Security Report</h1>\n")
                f.write(f"    <p class='info-text'>Report generato il: {timestamp}</p>\n")


                # Mappa nomi sezione a classi CSS per lo stile colorato e potenziali icone
                section_info = {
                    'Servizi Attivi': {'class': 'services', 'icon': 'fas fa-cogs'}, # Esempio icona Font Awesome
                    'Porte Aperte': {'class': 'ports', 'icon': 'fas fa-network-wired'},
                    'Utenti Loggati': {'class': 'users', 'icon': 'fas fa-users'},
                    'Modifiche Recenti (/etc)': {'class': 'files', 'icon': 'fas fa-file-alt'},
                    'Permessi File Critici': {'class': 'permissions', 'icon': 'fas fa-lock'},
                    # Mappa i nomi delle nuove sezioni qui
                }


                for section, content in data.items():
                    # Ottieni le info di stile e icona per la sezione
                    info = section_info.get(section, {'class': '', 'icon': ''})
                    css_class = info['class']
                    icon_class = info['icon']

                    # Applica la classe base 'section' e la classe specifica
                    f.write(f"    <div class='section {css_class}'>\n")
                    # Aggiunge l'icona se specificata
                    f.write(f"    <h2>")
                    # if icon_class:
                    #     f.write(f"<i class='{icon_class}'></i>") # Aggiunge l'elemento icona
                    f.write(f"{section}</h2>\n")


                    # Assicurati che i tuoi moduli di scansione restituiscano una lista
                    # con dentro almeno un dizionario per le sezioni tabellari.
                    # Se non ci sono dati, restituisci una lista vuota [].
                    if isinstance(content, list) and content and isinstance(content[0], dict):
                        # Se è una lista di dizionari, crea una tabella
                        f.write("    <table>\n")
                        # Intestazione tabella (usa le chiavi del primo dizionario come intestazioni)
                        headers = list(content[0].keys()) # Usa list() per garantire l'ordine
                        f.write("        <tr>\n")
                        for header in headers:
                            f.write(f"            <th>{header}</th>\n")
                        f.write("        </tr>\n")
                        # Righe tabella
                        for item in content:
                            f.write("        <tr>\n")
                            for header in headers:
                                # Gestisce valori mancanti o None usando item.get()
                                value = item.get(header, '')
                                # Converto in str per sicurezza e gestisco None o altri tipi
                                display_value = str(value)

                                # Applica stili specifici per la colonna "Avviso di Sicurezza" nel modulo permessi
                                if section == 'Permessi File Critici' and header == 'Avviso di Sicurezza':
                                    if 'AVVISO:' in display_value:
                                        f.write(f"            <td><span class='warning'>{display_value}</span></td>\n")
                                    elif display_value == 'OK':
                                        f.write(f"            <td><span class='ok'>{display_value}</span></td>\n")
                                    else: # Per errori o altri messaggi
                                         f.write(f"            <td>{display_value}</td>\n")
                                else:
                                    f.write(f"            <td>{display_value}</td>\n")
                            f.write("        </tr>\n")
                        f.write("    </table>\n")
                    elif isinstance(content, list) and not content: # Se è una lista vuota
                        f.write("<p>Nessun dato trovato per questa sezione.</p>\n")
                    else:
                        # Altrimenti, lo tratta come testo o output grezzo non strutturato
                         # Avvolge nel tag pre per mantenere la formattazione del testo originale
                        f.write("    <pre>\n")
                        # Assicurati che il contenuto sia una stringa o convertibile
                        f.write(str(content))
                        f.write("\n    </pre>\n")

                    f.write("    </div>\n") # Chiude il div della sezione

                f.write("    <p class='info-text'>Fine del report SnapAudit.</p>\n")
                f.write("    </div>\n") # Chiude il div container
                f.write("</body>\n")
                f.write("</html>\n")

        else:
            print(f"Formato report '{format}' non supportato. Non è stato generato alcun file di report.", file=sys.stderr) # Scrive su stderr
            return None # Restituisce None se il formato non è supportato

        print(f"  Report file '{filename}' generato con successo.")
        return filename # Restituisce il percorso del file generato

    except Exception as e:
        print(f"  Errore critico durante la generazione del report file: {e}", file=sys.stderr)
        return None # Restituisce None in caso di errore critico
