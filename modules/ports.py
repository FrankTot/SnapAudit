# SnapAudit/modules/ports.py

import subprocess
import sys

def get_open_ports():
    """
    Esegue 'ss -tuln' e parsifica l'output per ottenere una lista di porte aperte.
    Restituisce una lista di dizionari, ognuno rappresentante una porta in ascolto.
    Include gestione errori.
    """
    print("  Esecuzione comando: ss -tuln")
    try:
        # ss -tuln mostra socket in stato di ascolto (LISTEN) per tcp, udp, raw, unix
        # -t: tcp, -u: udp, -l: listening, -n: numeric (non risolvere nomi host/servizi)
        result = subprocess.run(
            ['ss', '-tuln'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output_lines = result.stdout.strip().split('\n')

        # Il parsing è basato sul formato standard di ss -tuln
        # Netid State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
        # tcp   LISTEN     0      128    0.0.0.0:22                       0.0.0.0:*
        # tcp   LISTEN     0      128    [::]:22                          [::]:*
        # udp   UNCONN     0      0      127.0.0.53%lo:53                 0.0.0.0:*
        # ...

        parsed_ports = []
        # Salta la riga di intestazione
        if len(output_lines) > 1:
            port_lines = output_lines[1:]

            for line in port_lines:
                 # Dividi la linea per spazi, gestendo spazi multipli
                parts = line.split()

                if len(parts) >= 5: # Assicurati che ci siano almeno le colonne principali
                    port_info = {
                        'Netid': parts[0].strip(),
                        'State': parts[1].strip(),
                        'Recv-Q': parts[2].strip(),
                        'Send-Q': parts[3].strip(),
                        'Local Address:Port': parts[4].strip(),
                        'Peer Address:Port': parts[5].strip() if len(parts) > 5 else '' # Peer Address:Port può mancare
                    }
                    parsed_ports.append(port_info)
                # Ignora righe che non corrispondono al formato atteso

        print(f"  Trovate {len(parsed_ports)} porte in ascolto.")
        return parsed_ports

    except FileNotFoundError:
        print("  Errore: Il comando 'ss' non è stato trovato.")
        print("  Assicurati che il pacchetto iproute2 sia installato.")
        return [] # Restituisce una lista vuota in caso di errore
    except subprocess.CalledProcessError as e:
        print(f"  Errore durante l'esecuzione di 'ss': {e}")
        print(f"  Stderr: {e.stderr}")
        return [] # Restituisce una lista vuota in caso di errore
    except Exception as e:
        print(f"  Errore generico durante la scansione delle porte: {e}")
        return [] # Restituisce una lista vuota in caso di errore

