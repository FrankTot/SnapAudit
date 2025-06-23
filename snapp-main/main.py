from PyQt6.QtWidgets import QApplication
import sys
from gui.main_gui import MainGUI

def main():
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
