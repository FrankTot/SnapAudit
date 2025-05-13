import subprocess

def get_logged_users():
    result = subprocess.run(['who'], capture_output=True, text=True)
    return result.stdout
