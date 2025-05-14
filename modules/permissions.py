# SnapAudit/modules/permissions.py

import os
import stat
import sys

def get_file_permissions_octal(filepath):
    """
    Ottiene i permessi di un file o directory in formato ottale (es. '0755').

    Args:
        filepath (str): Il percorso del file o directory.

    Returns:
        str: I permessi in formato ottale (4 cifre) o un messaggio di errore.
    """
    try:
        # Ottiene lo status del file/cartella
        st = os.stat(filepath)
        # Converte i permessi (st_mode) in formato ottale
        # stat.S_IMODE maschera solo i bit dei permessi (ultima parte del mode)
        permissions = oct(stat.S_IMODE(st.st_mode))
        # Restituisce le ultime 4 cifre (es. '0o755' -> '0755')
        return permissions[-4:]
    except FileNotFoundError:
        return "File non trovato"
    except PermissionError:
        # Questo accade se l'utente che esegue lo script non ha permessi per stat() il file
        return "Permesso negato (esegui come root?)"
    except Exception as e:
        return f"Errore: {e}"

def check_critical_file_permissions():
    """
    Controlla i permessi di una lista predefinita di file di configurazione critici.
    Segnala i permessi e aggiunge un avviso se sono potenzialmente problematici
    (es. scrivibili da 'group' o 'other').

    Restituisce una lista di dizionari con informazioni sul file, permessi e avvisi.
    """
    print("  Controllo permessi file critici...")
    # Lista di file critici da controllare. Aggiungi o rimuovi secondo necessità.
    # NOTA: L'accesso a /etc/shadow e /etc/sudoers richiede solitamente permessi di root.
    critical_files = [
        '/etc/passwd',
        '/etc/shadow',
        '/etc/group',
        '/etc/sudoers',
        '/etc/crontab',
        '/etc/anacrontab',
        '/etc/ssh/sshd_config',
        '/etc/hosts',
        '/etc/resolv.conf',
        # Puoi aggiungere file di configurazione di servizi specifici (es. web server, database)
    ]

    results = []
    for fpath in critical_files:
        perms = get_file_permissions_octal(fpath)
        warning = ""

        # Logica semplificata per identificare permessi potenzialmente problematici
        # Questa logica può essere resa molto più sofisticata a seconda delle politiche di sicurezza
        if perms not in ["File non trovato", "Permesso negato (esegui come root?)"]:
            try:
                # Converti i permessi ottali in un intero per analisi bit per bit
                # Esempio: '0755' -> 755
                perms_int = int(perms, 8)

                # Controlla i bit di scrittura per 'group' (0o020) e 'other' (0o002)
                # S_IWGRP = 0o020 (write by group)
                # S_IWOTH = 0o002 (write by other)
                # stat.S_ISREG(os.stat(fpath).st_mode) # Controlla se è un file regolare

                # Esempi di controlli:
                # - Se è scrivibile da 'other' (bit 0o002) E non è un file che dovrebbe esserlo (raro)
                # - Se è scrivibile da 'group' (bit 0o020) e il gruppo non è ristretto
                # - Permessi 777, 666, ecc. sono quasi sempre un problema

                # Esempio base: segnala se è scrivibile da 'other'
                if (perms_int & stat.S_IWOTH) and stat.S_ISREG(os.stat(fpath).st_mode):
                     warning += "AVVISO: Scrivibile da 'other'!"
                # Esempio base: segnala se è scrivibile da 'group'
                if (perms_int & stat.S_IWGRP) and stat.S_ISREG(os.stat(fpath).st_mode):
                     if warning: warning += " " # Aggiunge spazio se c'è già un avviso
                     warning += "AVVISO: Scrivibile da 'group'!"
                # Puoi aggiungere controlli specifici per file noti, es. /etc/shadow non dovrebbe essere leggibile da non-root

            except ValueError:
                warning = "Errore nell'analisi dei permessi ottali"
            except FileNotFoundError:
                 # Già gestito da get_file_permissions_octal, ma per sicurezza qui
                 warning = "File non trovato durante il controllo permessi"
            except Exception as e:
                 warning = f"Errore nell'analisi dei permessi: {e}"


        results.append({
            'Percorso File': fpath,
            'Permessi (Ottale)': perms,
            'Avviso di Sicurezza': warning if warning else 'OK' # Mostra OK se non ci sono avvisi
        })

    print(f"  Controllo permessi completato per {len(critical_files)} file.")
    return results
