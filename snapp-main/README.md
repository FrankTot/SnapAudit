
# Snapp - System Snapshot Audit Tool

Snapp è un'applicazione Python per effettuare snapshot del sistema GNU/Linux, raccogliendo informazioni sui servizi attivi, utenti configurati e loggati, porte aperte e ultime modifiche ai file di sistema.  
Genera report PDF chiari e completi e offre una GUI moderna per gestire e visualizzare i report.

---

## Funzionalità

- Scansione e snapshot dei servizi attivi  
- Rilevazione degli utenti configurati e attivi al momento dell'audit  
- Identificazione delle porte di rete aperte  
- Monitoraggio delle ultime modifiche ai file nella cartella `/etc`  
- Generazione di report PDF con nome automatico che include data e ora del report  
- Interfaccia grafica intuitiva per generare, salvare e visualizzare i report  
- Possibilità di aprire i report precedenti direttamente dalla GUI

---

## Requisiti

### Dipendenze Python

Il progetto usa Python 3 e richiede:

- `PyQt6==6.6.1` (per la GUI)  
- `fpdf2==2.6.0` (per la generazione PDF)

Questi pacchetti sono indicati in `requirements.txt`. Per installarli esegui:

```bash
pip3 install -r requirements.txt
```

---

### Dipendenze di sistema

Per aprire i file PDF dalla GUI, è necessario che sul sistema siano presenti uno o più programmi in grado di visualizzare PDF e un gestore di apertura file.  
Su sistemi Debian/Ubuntu (o derivati) installa:

```bash
sudo apt update
sudo apt install evince xdg-utils links2
```

- `evince`: visualizzatore PDF grafico consigliato  
- `xdg-utils`: per aprire file con il programma predefinito  
- `links2`: browser testuale di fallback nel caso non siano disponibili altri programmi grafici

Se non hai questi programmi o se aprendo i PDF ricevi errori simili a:

```
No applications found for mimetype: application/pdf
xdg-open: no method available for opening 'file.pdf'
```

devi installarli tramite il gestore pacchetti della tua distribuzione.

---

## Installazione e avvio

1. Clona la repository:

```bash
git clone https://github.com/tuo-username/snapp.git
cd snapp
```

2. Installa le dipendenze Python:

```bash
pip3 install -r requirements.txt
```

3. Installa le dipendenze di sistema (vedi sopra)

4. Avvia il programma:

```bash
python3 main.py
```

---

## Come usare il programma

- Avvia `main.py` per aprire la GUI  
- Clicca su "Genera Report" per effettuare l’audit e creare un nuovo PDF  
- Il report sarà salvato automaticamente in `reports/` con nome del tipo:

  ```
  report_YYYYMMDD_HHMMSS.pdf
  ```

- Puoi visualizzare subito il report appena creato o aprire qualsiasi report precedente dalla lista  
- Se mancano programmi per aprire PDF, segui la sezione "Dipendenze di sistema" per risolvere

---

## Struttura del progetto

```
snapp/
├── assets/               # Risorse statiche: logo, fonts (se presenti)
├── core/                 # Logica principale: snapshot e generazione report
│   ├── __init__.py
│   ├── report_generator.py
│   └── system_snapshot.py
├── gui/                  # GUI e visualizzatore PDF
│   ├── __init__.py
│   ├── main_gui.py
│   └── pdf_viewer.py
├── reports/              # Dove vengono salvati i report PDF
├── main.py               # Script principale di avvio GUI
├── requirements.txt      # Dipendenze Python
└── README.md             # Questo file
```

---

## Note importanti

- Il programma deve essere eseguito con permessi sufficienti per leggere i dati di sistema necessari (ad esempio `/etc`)  
- I report sono generati usando il font di default di `fpdf2` per evitare problemi di compatibilità e download font  
- Se si vuole cambiare il visualizzatore PDF di default, basta installarne uno differente e assicurarsi che `xdg-open` lo riconosca correttamente  
- In caso di problemi, controlla che tutti i pacchetti Python siano aggiornati e che le dipendenze di sistema siano installate

---

## Contatti e supporto

Per domande, problemi o suggerimenti apri una issue su GitHub o contattami direttamente.

---

Buon audit e buon lavoro con Snapp! 🚀
