
import subprocess

def get_active_services():
    result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'],
                            capture_output=True, text=True)
    return result.stdout
