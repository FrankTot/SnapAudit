import subprocess

def get_open_ports():
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    return result.stdout
