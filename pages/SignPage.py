import os
import psutil
import time
import tracemalloc

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.analytics import get_resource_usage
from helpers.sign import sign_file, save_signature_to_file

class SignPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack

        pageLabel = QLabel("Sign Documents")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        #  Create and configure labels
        self.shift_label = QLabel("Key:")
        self.plaintext_label = QLabel("Plaintext:")
        self.ciphertext_label = QLabel("Ciphertext:")

        # Create and configure input fields
        self.shift_input = QTextEdit()        
        self.shift_input.setPlaceholderText("Key must be one of 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23 and 25")
        self.shift_input.setStyleSheet("font-size: 18px; padding: 5px; height: 20px; ")

        self.docfile_button = QPushButton("Select document file")
        self.docfile_button.setFixedWidth(150)  # Set fixed width
        self.docfile_button.setFixedHeight(25)  # Set fixed height
        self.docfile_button.clicked.connect(lambda: self.pick_doc_file())
        self.docfile_label = QLabel("No file selected")

        # Layout for file picker 1
        docfile_layout = QHBoxLayout()
        docfile_layout.addStretch()
        docfile_layout.addWidget(self.docfile_button)
        docfile_layout.addWidget(self.docfile_label)
        docfile_layout.addStretch()

        # self.plaintext_input = QTextEdit()
        # self.plaintext_input.setReadOnly(True)
        # self.plaintext_input.setFixedHeight(90)
        # self.plaintext_input.setStyleSheet("font-size: 12px; margin-bottom: 25px;")

        self.privatekeyfile_button = QPushButton("Select private key file")
        self.privatekeyfile_button.setFixedWidth(150)  # Set fixed width
        self.privatekeyfile_button.setFixedHeight(25)  # Set fixed height
        self.privatekeyfile_button.clicked.connect(lambda: self.pick_privatekey_file())
        self.privatekeyfile_label = QLabel("No private key selected")

        # Layout for file picker 1
        privatekeyfile_layout = QHBoxLayout()
        privatekeyfile_layout.addStretch()
        privatekeyfile_layout.addWidget(self.privatekeyfile_button)
        privatekeyfile_layout.addWidget(self.privatekeyfile_label)
        privatekeyfile_layout.addStretch()

        self.analysis_output_label = QLabel("Calculation Time:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setStyleSheet("font-size: 13px; padding: 5px; height: 10px;")

        # Layout for inputs
        input_layout = QVBoxLayout()
        input_layout.addLayout(docfile_layout)
        input_layout.addLayout(privatekeyfile_layout)

        # Create and configure the "Sign" button
        sign_button = QPushButton("Sign Document")
        sign_button.setStyleSheet("font-size: 18px; padding: 10px;")
        sign_button.clicked.connect(self.sign_btn_clicked)

        # Create and configure the "Save" button
        save_button = QPushButton("Save Signature")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_sigfile_btn_clicked)

        # Layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(sign_button)
        # button_layout.addWidget(decrypt_button)
        # button_layout.addWidget(attack_button)
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
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(clear_button)
        layout.addWidget(back_button)
        layout.setAlignment(pageLabel, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(back_button, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(clear_button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.docfile_path = None
        self.privatekey_file_path = None
        self.signature = None
        self.validKeys = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    def go_back(self):
        self.docfile_path = None
        self.privatekey_file_path = None
        self.signature = None
        # self.plaintext_input.setPlainText("")
        # self.ciphertext_output.setPlainText("")
        # self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.shift_input.setPlainText(None)
        self.docfile_path = None
        self.privatekey_file_path = None
        self.stack.setCurrentIndex(0)

    def clear(self):
        self.docfile_path = None
        self.privatekey_file_path = None
        self.signature = None
        # self.plaintext_input.setPlainText("")
        # self.ciphertext_output.setPlainText("")
        # self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.privatekeyfile_label.setText("No private key selected")
        self.shift_input.setPlainText(None)
        self.docfile_path = None
        self.privatekey_file_path = None
            
    def pick_doc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            file_size = os.stat(file_path).st_size/1024
            self.docfile_path = file_path
            self.docfile_label.setText(f"Document file selected, {file_size:.2f} KB in file size")

    def pick_privatekey_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Private Key", "", "Pem Files (*.pem)")
        if file_path:
            self.privatekey_file_path = file_path
            self.privatekeyfile_label.setText(f"Private Key selected")

    def sign_btn_clicked(self):
        if not self.docfile_path:
            QMessageBox.warning(self, "Warning", "No document file selected")
            return
        
        if not self.privatekey_file_path:
            QMessageBox.warning(self, "Warning", "No private key selected")
            return

        self.analysis_output.setPlainText("")
        
        try:
            tracemalloc.start()
            start_time = time.time()        
            self.signature = sign_file(self.privatekey_file_path, self.docfile_path)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            time_taken_ms = (end_time - start_time) * 10**3
            cpu_usage, memory_usage = self.monitor_resources()

            timeTakenAnalysis = f"Time taken: {time_taken_ms:.2f} ms"
            cpuUsageAnalysis = f"CPU usage: {cpu_usage}%"        
            memoryUsageAnalysis = f"Memory usage: {peak / 10**3} KB"        
            combinedAnalysis = f"{timeTakenAnalysis}"
            # combinedAnalysis = f"{timeTakenAnalysis}\n{cpuUsageAnalysis}\n{memoryUsageAnalysis}"

            self.analysis_output.setPlainText(combinedAnalysis)
            QMessageBox.information(self, "Success", "Document signed successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", repr(e))
            return

    def save_sigfile_btn_clicked(self):        
        if not self.signature:
            QMessageBox.warning(self, "Warning", "No signature to be saved")
            return        
        try:
            info = save_signature_to_file(self.signature, self.docfile_path)
            QMessageBox.information(self, "Success", info)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Signature file failed to save")
            return
        
    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return cpu_usage, memory_usage