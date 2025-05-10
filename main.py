import sys
from ui.window import NetworkManagerGUI
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkManagerGUI()
    window.show()
    sys.exit(app.exec())
