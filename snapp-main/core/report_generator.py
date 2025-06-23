import datetime
from fpdf import FPDF
from .system_snapshot import (
    get_active_services,
    get_logged_users,
    get_open_ports,
    get_recent_etc_modifications
)

class PDFReport:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)

        # Nome file con data e ora
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"reports/report_{now_str}.pdf"

        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=12)
        self._add_header()
        self.generate_full_report()
        self.pdf.output(self.filename)
        print(f"Report salvato in {self.filename}")

    def _add_header(self):
        self.pdf.set_font("Helvetica", "B", 16)
        self.pdf.cell(0, 10, "SnapAudit Report", ln=True, align="C")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pdf.set_font("Helvetica", "", 12)
        self.pdf.cell(0, 10, f"Data report: {now}", ln=True, align="C")
        self.pdf.ln(10)

    def add_section(self, title, content):
        self.pdf.set_font("Helvetica", "B", 14)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font("Helvetica", "", 12)
        safe_content = content.encode('ascii', errors='ignore').decode('ascii')
        self.pdf.multi_cell(0, 8, safe_content)
        self.pdf.ln(5)

    def generate_full_report(self):
        self.add_section("Servizi Attivi", get_active_services())
        self.add_section("Utenti Loggati", get_logged_users())
        self.add_section("Porte Aperte", get_open_ports())
        self.add_section("Modifiche Recenti in /etc", get_recent_etc_modifications())
