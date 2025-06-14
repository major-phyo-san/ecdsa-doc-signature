import os
import psutil
import time
import tracemalloc

from datetime import datetime

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.analytics import get_resource_usage
from helpers.keygen import generate_keypair

class KeygenPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack
        self.keypair = {}

        pageLabel = QLabel("Key Pair Generation")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        # Create and configure select box
        self.options = {
            "ed25519",  # default
            "secp224r1",
            "secp256k1",  # Used in Bitcoin & Ethereum
            "secp256r1",  # General-Purpose (Web, TLS, Digital Signatures, Blockchain), (NIST P-256), Same as prime256v1
            "secp384r1",  # Higher Security (Government, Long-Term Security)
            "secp521r1",  # Ultra-Secure (Rare Use Cases, High Computational Power)
            "prime192v1",  # Same as secp192r1
            "prime256v1",  # Same as secp256r1
        }
        self.select_box = QComboBox()
        self.select_box.addItems(self.options)
        self.select_box.setStyleSheet("font-size: 18px; padding: 5px; width: 120px; height: 30px;")

        #  Create and configure buttons
        keygen_button = QPushButton("Generate Public/Private Key Pair")
        keygen_button.setStyleSheet("font-size: 18px; padding: 10px;")
        keygen_button.clicked.connect(self.keygen_btn_clicked)

        # Create and configure the "Save As" button
        save_button = QPushButton("Save Key Pair")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_keys)

        # Layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.select_box)
        button_layout.addWidget(keygen_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch(1)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.go_back)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("font-size: 18px; padding: 10px;")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout()
        layout.addWidget(pageLabel)
        layout.addLayout(button_layout)
        layout.addWidget(clear_button)     
        layout.addWidget(back_button)       
        layout.setAlignment(pageLabel, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(back_button, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(clear_button, Qt.AlignmentFlag.AlignCenter)

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
        cpu_usage, memory_usage = self.monitor_resources()
        print(f"Time taken {round(time_taken_ms, 4)} ms")
        print(f"CPU usage {cpu_usage} %")
        print(f"Memory usage {memory_usage} %")
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

    def save_to_file_btn_clicked(self):
        if not self.is_encryption and not self.is_decryption:
            QMessageBox.warning(self, "Warning", "No data to be saved")
            return
        
        text = None
        if self.is_encryption:
            cipherText = self.ciphertext_output.toPlainText()
            if not cipherText:
                QMessageBox.warning(self, "Warning", "No cipher text to save. Check the decryption first.")
                return
            text = cipherText
        
        if self.is_decryption:
            plainText = self.plaintext_input.toPlainText()
            if not plainText:
                QMessageBox.warning(self, "Warning", "No plain text to save. Check the encryption first.")
                return
            text = plainText

        # Open file dialog to save the combined content
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_path and text:
            self.save_to_file(file_path, text)

    def save_to_file(self, file_path, text):
        try:
            with open(file_path, 'w') as file:
                file.write(text)
            QMessageBox.information(self, "Success", "File saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save plain text file: {e}")

    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return cpu_usage, memory_usage