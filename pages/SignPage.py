import os
import time
import tracemalloc

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.sign import sign_file, save_signature_to_file

class SignPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack

        pageLabel = QLabel("Sign Documents")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        self.docfile_button = QPushButton("Select document file")        
        self.docfile_button.clicked.connect(lambda: self.pick_doc_file())
        self.docfile_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.docfile_label = QLabel("No file selected")
        self.docfile_label.setStyleSheet("font-size: 12px; padding: 10px;")

        self.privatekeyfile_button = QPushButton("Select private key file")        
        self.privatekeyfile_button.clicked.connect(lambda: self.pick_privatekey_file())
        self.privatekeyfile_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.privatekeyfile_label = QLabel("No private key selected")
        self.privatekeyfile_label.setStyleSheet("font-size: 12px; padding: 10px;")

        self.analysis_output_label = QLabel("Calculation Time:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setStyleSheet("font-size: 13px; padding: 5px; height: 10px;")

        # Create and configure the "Sign" button
        sign_button = QPushButton("Sign Document")
        sign_button.setStyleSheet("font-size: 18px; padding: 10px;")
        sign_button.clicked.connect(self.sign_btn_clicked)

        # Create and configure the "Save" button
        save_button = QPushButton("Save Signature")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_sigfile_btn_clicked)

        # back_button = QPushButton("Back")
        # back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        # back_button.clicked.connect(self.go_back)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("font-size: 18px; padding: 10px;")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout()

        pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pageLabel.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(pageLabel)

        # Input area
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)        

        # Re-create docfile layout
        docfile_col = QVBoxLayout()
        docfile_col.addWidget(self.docfile_button, alignment=Qt.AlignmentFlag.AlignCenter)
        docfile_col.addWidget(self.docfile_label, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addLayout(docfile_col)

        # Re-create private key layout
        privatekey_col = QVBoxLayout()
        privatekey_col.addWidget(self.privatekeyfile_button, alignment=Qt.AlignmentFlag.AlignCenter)
        privatekey_col.addWidget(self.privatekeyfile_label, alignment=Qt.AlignmentFlag.AlignCenter)        
        input_layout.addLayout(privatekey_col)

        layout.addLayout(input_layout)

        # Action buttons
        action_layout = QVBoxLayout()
        sign_button.setStyleSheet("font-size: 16px; padding: 10px;")
        save_button.setStyleSheet("font-size: 16px; padding: 10px;")
        action_layout.addWidget(sign_button)
        action_layout.addWidget(save_button)
        action_layout.setSpacing(15)
        action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(action_layout)

        # Analysis output
        # layout.addSpacing(20)
        # layout.addWidget(self.analysis_output_label)
        # layout.addWidget(self.analysis_output)

        # Footer buttons
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(clear_button)
        # footer_layout.addWidget(back_button)
        footer_layout.addStretch()
        footer_layout.setSpacing(20)
        layout.addSpacing(30)
        layout.addLayout(footer_layout)

        layout.addStretch()
        self.setLayout(layout)

        self.docfile_path = None
        self.privatekey_file_path = None
        self.signature = None

    def go_back(self):
        self.docfile_path = None
        self.privatekey_file_path = None
        self.signature = None
        # self.plaintext_input.setPlainText("")
        # self.ciphertext_output.setPlainText("")
        # self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.privatekeyfile_label.setText("No private key selected")
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
            # cpu_usage, memory_usage = self.monitor_resources()

            # timeTakenAnalysis = f"Time taken: {time_taken_ms:.2f} ms"
            # cpuUsageAnalysis = f"CPU usage: {cpu_usage}%"        
            # memoryUsageAnalysis = f"Memory usage: {peak / 10**3} KB"        
            # combinedAnalysis = f"{timeTakenAnalysis}"
            # combinedAnalysis = f"{timeTakenAnalysis}\n{cpuUsageAnalysis}\n{memoryUsageAnalysis}"

            # self.analysis_output.setPlainText(combinedAnalysis)
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
        
    # def monitor_resources(self, interval=1):
    #     cpu_usage, memory_usage = get_resource_usage(interval)
    #     return cpu_usage, memory_usage