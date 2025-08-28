import sys

from PyQt6.QtWidgets import QApplication, QTabWidget

from pages.KeygenPage import KeygenPage
from pages.SignPage import SignPage
from pages.VerifyPage import VerifyPage

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Document Digital Signature")
        self.setGeometry(0, 0, 800, 700)
        self.setFixedSize(800, 700)

        # Create pages
        self.page1 = KeygenPage(self)
        self.page2 = SignPage(self)
        self.page3 = VerifyPage(self)

        # Add tabs
        self.addTab(self.page1, "Key Pair Generation")
        self.addTab(self.page2, "Sign Documents")
        # self.addTab(self.page3, "Verify Documents")

def apply_stylesheet(app):
    app.setStyleSheet("""
        QWidget {
            background: #F1F8F4;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }

        QLabel {
            color: #2E7D32;
            font-size: 18px;
            font-weight: 500;
        }

        QPushButton {
            background-color: #2E7D32;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 17px;
            font-weight: 600;
            min-width: 180px;
            max-width: 240px;
        }

        QPushButton:hover {
            background-color: #43A047;
            color: #ffffff;
        }

        QPushButton:pressed {
            background-color: #1B5E20;
        }

        QLineEdit, QTextEdit {
            background: #ffffff;
            border: 1.5px solid #A5D6A7;
            border-radius: 6px;
            padding: 6px;
            font-size: 16px;
        }

        QTabWidget::pane {
            border: 2px solid #A5D6A7;
            border-radius: 10px;
            margin: 16px 8px 8px 8px;
            padding: 12px;
        }

        QTabBar::tab {
            background: #F1F8F4;
            color: #2E7D32;
            border: 1px solid #A5D6A7;
            border-radius: 8px 8px 0 0;
            min-width: 40px;
            min-height: 18px;
            margin-right: 3px;
            margin-top: 18px;
            margin-left: 8px;
            padding: 4px 12px 4px 12px;
            font-size: 15px;
            font-weight: 600;
        }

        QTabBar::tab:first {
            margin-left: 18px;
        }

        QTabBar::tab:selected {
            background: #2E7D32;
            color: #ffffff;
        }

        QTabBar::tab:hover {
            background: #43A047;
            color: #ffffff;
        }
    """)

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
