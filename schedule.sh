#!/bin/bash
# SnapAudit/schedule.sh
# Script di esempio per schedulare l'esecuzione di SnapAudit.

# Cambia directory alla posizione dello script
# Questo è importante se lo script viene eseguito da cron o systemd
cd "$(dirname "$0")"

# Esegui lo script Python
# Assicurati che 'python3' punti all'interprete corretto
# Puoi specificare il percorso completo se necessario, es. /usr/bin/python3
/usr/bin/python3 main.py A # Esegue tutte le scansioni ('A') senza mostrare il menu interattivo

# NOTA: Quando eseguito da uno scheduler (cron, systemd), l'apertura automatica
# del report potrebbe non funzionare o non essere desiderata.
# Potresti voler modificare main.py per disabilitare l'apertura automatica
# se rileva di essere eseguito senza un terminale interattivo,
# oppure modificare questo script per gestire l'output del report (es. inviarlo via email).

# Esempio per cron (esegue ogni giorno alle 3:00 AM):
# 0 3 * * * /bin/bash /path/to/your/SnapAudit/schedule.sh > /path/to/your/SnapAudit/cron.log 2>&1
