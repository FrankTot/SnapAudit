from modules import services, ports, users, files, report

def main():
    data = {
        'Servizi Attivi': services.get_active_services(),
        'Porte Aperte': ports.get_open_ports(),
        'Utenti Loggati': users.get_logged_users(),
        'Modifiche Recenti (/etc)': files.get_recent_file_changes('/etc'),
    }

    report_path = report.generate_report(data)
    print(f"✅ Report generato: {report_path}")

if __name__ == '__main__':
    main()
