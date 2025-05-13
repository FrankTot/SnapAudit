# SnapAudit

SnapAudit è uno strumento Python che esegue una scansione di sicurezza su sistemi Linux. Genera snapshot dello stato attuale del sistema.

## Funzionalità

- Servizi attivi
- Porte di rete aperte
- Utenti loggati
- Modifiche recenti ai file in /etc
- Report automatico

## Utilizzo

```bash
python3 main.py
```

## Automazione (cron)

```bash
crontab -e
# Esecuzione giornaliera alle 7:00
0 7 * * * /percorso/assoluto/schedule.sh
```
