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
        self.addTab(self.page3, "Verify Documents")

def apply_stylesheet(app):
    app.setStyleSheet("""
        QWidget {
            background: #f5f7fa;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }
        QLabel {
            color: #23198c;
            font-size: 18px;
            font-weight: 500;
        }
        QPushButton {
            background-color: #b3d8e3;
            color: #23198c;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 17px;
            font-weight: 600;
            min-width: 180px;
            max-width: 240px;
        }
        QPushButton:hover {
            background-color: #7fc7e3;
            color: #fff;
        }
        QPushButton:pressed {
            background-color: #5ba7c5;
        }
        QLineEdit, QTextEdit {
            background: #fff;
            border: 1.5px solid #b3d8e3;
            border-radius: 6px;
            padding: 6px;
            font-size: 16px;
        }
        QTabWidget::pane {
            border: 2px solid #b3d8e3;
            border-radius: 10px;
            margin: 16px 8px 8px 8px;
            padding: 12px;
        }
        QTabBar::tab {
            background: #eaf6fb;
            color: #23198c;
            border: 1px solid #b3d8e3;
            border-radius: 8px 8px 0 0;
            min-width: 40px;
            min-height: 18px;
            margin-right: 3px;
            margin-top: 18px;
            margin-left: 8px; /* Add margin at the start of tabs */
            padding: 4px 12px 4px 12px;
            font-size: 15px;
            font-weight: 600;
        }
        QTabBar::tab:first {
            margin-left: 18px; /* Extra margin for the very first tab */
        }
        QTabBar::tab:selected {
            background: #b3d8e3;
            color: #23198c;
        }
        QTabBar::tab:hover {
            background: #7fc7e3;
            color: #fff;
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
