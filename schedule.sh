#!/bin/bash
# SnapAudit/schedule.sh
# Script di esempio per schedulare l'esecuzione di SnapAudit.

# Cambia directory alla posizione dello script
# Questo è importante se lo script viene eseguito da cron o systemd
cd "$(dirname "$0")"

# Esegui lo script Python
# Assicurati che 'python3' punti all'interprete corretto
# Puoi specificare il percorso completo se necessario, es. /usr/bin/python3
# Passa 'A' per eseguire tutte le scansioni.
# L'output a terminale andrà nel file di log specificato nella crontab.
# Quando eseguito in questo modo, il menu interattivo non viene mostrato.
/usr/bin/python3 main.py A

# NOTA: Quando eseguito da uno scheduler (cron, systemd), la visualizzazione
# della tabella a terminale non sarà visibile interattivamente.
# L'output verrà reindirizzato al file di log specificato nella crontab.
# Il report testuale verrà comunque salvato nella directory 'reports/'.
# L'opzione 'O' (Apri Ultimo Report) non è utilizzabile in esecuzione schedulata.

# Esempio per cron (esegue ogni giorno alle 3:00 AM):
# 0 3 * * * /bin/bash /path/completo/alla/tua/directory/SnapAudit/schedule.sh > /path/completo/alla/tua/directory/SnapAudit/cron.log 2>&1
