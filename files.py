
import subprocess

def get_recent_file_changes(path='/etc', days=1):
    result = subprocess.run(['find', path, '-type', 'f', '-mtime', f'-{days}'],
                            capture_output=True, text=True)
    return result.stdout
