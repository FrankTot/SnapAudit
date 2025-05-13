
from datetime import datetime
import os

def generate_report(data: dict, output_dir='reports'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(output_dir, f'snap_report_{timestamp}.txt')

    with open(filename, 'w') as f:
        f.write(f"SnapAudit Report - {timestamp}\n")
        f.write("="*60 + "\n")
        for section, content in data.items():
            f.write(f"\n[ {section.upper()} ]\n")
            f.write(content + "\n")
    return filename
