SnapAudit
SnapAudit è uno strumento Python per eseguire snapshot di sicurezza di base su sistemi Linux. Aiuta a monitorare lo stato del sistema e identificare potenziali aree di interesse per la sicurezza.

Funzionalità
Menu Interattivo: Scegli quali scansioni eseguire all'avvio.

Report HTML Accattivante: Genera report formattati e colorati per una facile lettura.

Apertura Automatica Report: Il report generato viene aperto automaticamente nel browser predefinito.

Animazione di Caricamento: Feedback visivo durante la generazione del report.

Scansioni Modulari:

Servizi attivi

Porte di rete aperte

Utenti loggati

Modifiche recenti ai file in /etc (e altre directory configurabili)

Controllo permessi di file critici (richiede permessi di root per alcuni file come /etc/shadow)

Gestione degli Errori: Implementata una gestione base degli errori per l'esecuzione dei comandi.

Struttura del Progetto
SnapAudit/
├── main.py             # Script principale con menu e logica di esecuzione
├── modules/            # Directory contenente i moduli di scansione e reporting
│   ├── services.py     # Modulo per la scansione dei servizi attivi
│   ├── ports.py        # Modulo per la scansione delle porte aperte
│   ├── users.py        # Modulo per la scansione degli utenti loggati
│   ├── files.py        # Modulo per la scansione delle modifiche recenti ai file
│   ├── permissions.py  # Modulo per il controllo dei permessi dei file critici
│   └── report.py       # Modulo per la generazione dei report (TXT/HTML)
├── reports/            # Directory dove vengono salvati i report generati
├── schedule.sh         # Script di esempio per l'esecuzione schedulata
├── requirements.txt    # Elenco delle dipendenze Python
└── README.md           # Questo file

Installazione
Clona o scarica il progetto nella directory desiderata.

Assicurati di avere Python 3 installato.

Installa le dipendenze (se presenti in requirements.txt):

pip install -r requirements.txt

Nota: Attualmente non ci sono dipendenze esterne richieste.

Utilizzo
Naviga nella directory principale del progetto (SnapAudit/).

Esegui lo script principale:

python3 main.py

Segui le istruzioni del menu interattivo per selezionare le scansioni da eseguire.

Esecuzione Schedulata
Puoi utilizzare lo script schedule.sh per eseguire SnapAudit automaticamente tramite cron o systemd.

Rendi lo script eseguibile:

chmod +x schedule.sh

Modifica schedule.sh se necessario (es. per specificare il percorso di python3).

Aggiungi una voce a cron (esegui crontab -e) per eseguire lo script all'orario desiderato. Esempio per eseguire ogni giorno alle 3:00 AM:

0 3 * * * /bin/bash /path/completo/alla/tua/directory/SnapAudit/schedule.sh > /path/completo/alla/tua/directory/SnapAudit/cron.log 2>&1

Ricorda di sostituire /path/completo/alla/tua/directory/SnapAudit/ con il percorso effettivo.

Note sulla Sicurezza
Alcune scansioni, come il controllo dei permessi di /etc/shadow o /etc/sudoers, richiedono permessi di root. Esegui lo script con sudo python3 main.py per ottenere risultati completi per queste scansioni.

L'output dei report può contenere informazioni sensibili sul tuo sistema. Proteggi l'accesso alla directory reports/.

Contribuire
Sentiti libero di migliorare questo progetto! Puoi aggiungere nuove scansioni, migliorare il parsing dell'output, aggiungere formati di report, ecc.
