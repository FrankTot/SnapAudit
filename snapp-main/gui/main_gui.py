import os
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QMessageBox, QApplication, QLabel
)
from core.report_generator import PDFReport

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SnapAudit - GUI")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.generate_btn = QPushButton("Genera nuovo report")
        self.generate_btn.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_btn)

        layout.addWidget(QLabel("Report generati:"))
        self.report_list = QListWidget()
        layout.addWidget(self.report_list)

        self.open_btn = QPushButton("Apri report selezionato")
        self.open_btn.clicked.connect(self.open_report)
        layout.addWidget(self.open_btn)

        self.setLayout(layout)
        self.refresh_report_list()

    def refresh_report_list(self):
        self.report_list.clear()
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        reports = sorted(
            [f for f in os.listdir(reports_dir) if f.endswith(".pdf")],
            reverse=True
        )
        self.report_list.addItems(reports)

    def generate_report(self):
        try:
            report = PDFReport()
            QMessageBox.information(self, "Successo", f"Report generato:\n{report.filename}")
            self.refresh_report_list()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la generazione del report:\n{e}")

    def open_report(self):
        selected = self.report_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Attenzione", "Seleziona un report dalla lista.")
            return

        filename = os.path.join("reports", selected.text())
        try:
            # Su GNU/Linux usa xdg-open per aprire PDF col visualizzatore di default
            subprocess.Popen(["xdg-open", filename])
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'apertura del file:\n{e}")
