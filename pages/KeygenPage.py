import os
import psutil
import time
import tracemalloc

from datetime import datetime

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.keygen import generate_keypair

class KeygenPage(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack = stack
        self.keypair = {}

        pageLabel = QLabel("Key Pair Generation")
        pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pageLabel.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        self.select_box = QComboBox()
        self.select_box.addItems({"secp384r1"})
        self.select_box.setStyleSheet("font-size: 16px; padding: 6px;")

        keygen_button = QPushButton("Generate Key Pair")
        save_button = QPushButton("Save Key Pair")
        clear_button = QPushButton("Clear")
        back_button = QPushButton("Back")

        for btn in (keygen_button, save_button, clear_button, back_button):
            btn.setStyleSheet("font-size: 16px; padding: 10px;")
        keygen_button.clicked.connect(self.keygen_btn_clicked)
        save_button.clicked.connect(self.save_keys)
        clear_button.clicked.connect(self.clear)
        back_button.clicked.connect(self.go_back)

        # Group main action buttons
        action_layout = QVBoxLayout()
        # action_layout.addWidget(self.select_box)
        action_layout.addWidget(keygen_button)
        action_layout.addWidget(save_button)
        action_layout.setSpacing(15)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Footer layout
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(clear_button)
        # footer_layout.addWidget(back_button)
        footer_layout.addStretch()
        footer_layout.setSpacing(20)

        layout = QVBoxLayout()
        layout.addWidget(pageLabel)
        layout.addSpacing(10)
        layout.addLayout(action_layout)
        layout.addSpacing(30)
        layout.addLayout(footer_layout)
        layout.addStretch()

        self.setLayout(layout)

    def go_back(self):
        self.keypair = {}
        self.stack.setCurrentIndex(0)     

    def clear(self):
        self.keypair = {}
    
    def keygen_btn_clicked(self):
        selected_label = self.select_box.currentText();
        print(f"Keygen btn clicked with option {selected_label}")
        tracemalloc.start()
        start_time = time.time()
        self.keypair = generate_keypair(selected_label)
        if not self.keypair:
            QMessageBox.warning(self, "Warning", "Key pair generation failed")
            return
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        time_taken_ms = (end_time - start_time) * 1000
        # cpu_usage, memory_usage = self.monitor_resources()
        # print(f"Time taken {round(time_taken_ms, 4)} ms")
        # print(f"CPU usage {cpu_usage} %")
        # print(f"Memory usage {memory_usage} %")
        QMessageBox.information(self, "Success", f"Key pair for {self.select_box.currentText()} generated successfully.")
        # print(self.keypair["private_pem"])
    
    def save_keys(self):
        """Generate a key pair and save them to the selected directory."""
        # Get a directory from the user
        if not self.keypair:
            QMessageBox.critical(self, "Error", "No key pair to save.")
            return
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")

        if directory:  # Ensure the user selected a valid directory
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            public_key = self.keypair["public_pem"]
            private_key = self.keypair["private_pem"]
            # Define fixed file names
            private_key_name = f"{timestamp}_{self.select_box.currentText()}_private.pem"
            public_key_name = f"{timestamp}_{self.select_box.currentText()}_public.pem"
            public_key_path = os.path.join(directory, public_key_name)
            private_key_path = os.path.join(directory, private_key_name)

            try:
                # Save the public key
                with open(public_key_path, "wb") as pub_file:
                    pub_file.write(public_key)

                # Save the private key
                with open(private_key_path, "wb") as priv_file:
                    priv_file.write(private_key)

                # Show success message
                QMessageBox.information(self, "Success", f"Keys saved to:\n{directory}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save keys:\n{str(e)}")

    # def monitor_resources(self, interval=1):
    #     cpu_usage, memory_usage = get_resource_usage(interval)
    #     return cpu_usage, memory_usage