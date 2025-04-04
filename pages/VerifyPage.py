import os
import time
import tracemalloc

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.analytics import get_resource_usage
from helpers.verify import verify_file_signature

class VerifyPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack

        pageLabel = QLabel("Verify Documents")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        #  Create and configure labels
        self.shift_label = QLabel("Key:")
        self.plaintext_label = QLabel("Plaintext:")
        self.ciphertext_label = QLabel("Ciphertext:")

        # # Create and configure input fields
        # self.shift_input = QTextEdit()        
        # self.shift_input.setPlaceholderText("Key must be one of 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23 and 25")
        # self.shift_input.setStyleSheet("font-size: 18px; padding: 5px; height: 20px; ")

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

        self.sigfile_button = QPushButton("Select signature file")
        self.sigfile_button.setFixedWidth(150)  # Set fixed width
        self.sigfile_button.setFixedHeight(25)  # Set fixed height
        self.sigfile_button.clicked.connect(lambda: self.pick_sig_file())
        self.sigfile_label = QLabel("No signature selected")

        # Layout for file picker 2
        sigfile_layout = QHBoxLayout()
        sigfile_layout.addStretch()
        sigfile_layout.addWidget(self.sigfile_button)
        sigfile_layout.addWidget(self.sigfile_label)
        sigfile_layout.addStretch()

        self.publickeyfile_button = QPushButton("Select public key file")
        self.publickeyfile_button.setFixedWidth(150)  # Set fixed width
        self.publickeyfile_button.setFixedHeight(25)  # Set fixed height
        self.publickeyfile_button.clicked.connect(lambda: self.pick_publickey_file())
        self.publickeyfile_label = QLabel("No public key selected")

        # Layout for file picker 1
        publickeyfile_layout = QHBoxLayout()
        publickeyfile_layout.addStretch()
        publickeyfile_layout.addWidget(self.publickeyfile_button)
        publickeyfile_layout.addWidget(self.publickeyfile_label)
        publickeyfile_layout.addStretch()

        self.analysis_output_label = QLabel("Calculation Time:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setStyleSheet("font-size: 13px; padding: 5px; height: 10px;")

        # Layout for inputs
        input_layout = QVBoxLayout()
        input_layout.addLayout(docfile_layout)
        input_layout.addLayout(sigfile_layout)
        input_layout.addLayout(publickeyfile_layout)

        # Create and configure the "Sign" button
        verify_button = QPushButton("Verify Document")
        verify_button.setStyleSheet("font-size: 18px; padding: 10px;")
        verify_button.clicked.connect(self.verify_btn_clicked)

        # Layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(verify_button)
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
        self.publickey_file_path = None
        self.signaturefile_path = None

    def go_back(self):
        self.docfile_path = None
        self.publickey_file_path = None
        self.signaturefile_path = None
        # self.plaintext_input.setPlainText("")
        # self.ciphertext_output.setPlainText("")
        # self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.publickeyfile_label.setText("No public key selected")
        self.stack.setCurrentIndex(0)

    def clear(self):
        self.docfile_path = None
        self.publickey_file_path = None
        self.signaturefile_path = None
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.publickeyfile_label.setText("No public key selected")
        self.sigfile_label.setText("No signature selected")
    
    def pick_doc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            file_size = os.stat(file_path).st_size/1024
            self.docfile_path = file_path
            self.docfile_label.setText(f"Document file selected, {file_size:.2f} KB in file size")

    def pick_sig_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Signature File", "", "Sig Files (*.sig)")
        if file_path:
            self.signaturefile_path = file_path
            self.sigfile_label.setText(f"Signature selected")

    def pick_publickey_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Public Key", "", "Pem Files (*.pem)")
        if file_path:
            self.publickey_file_path = file_path
            self.publickeyfile_label.setText(f"Public Key selected")

    def verify_btn_clicked(self):
        if not self.docfile_path:
            QMessageBox.warning(self, "Warning", "No document file selected")
            return
        
        if not self.signaturefile_path:
            QMessageBox.warning(self, "Warning", "No signature selected")
            return
        
        if not self.publickey_file_path:
            QMessageBox.warning(self, "Warning", "No public key selected")
            return

        self.analysis_output.setPlainText("")
        
        try:
            tracemalloc.start()
            start_time = time.time()        
            if verify_file_signature(self.publickey_file_path, self.docfile_path, self.signaturefile_path):
                QMessageBox.information(self, "Success", "Document is valid")
            else:
                QMessageBox.warning(self, "Warning", "Document is invalid")
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
        except Exception as e:
            QMessageBox.critical(self, "Error", repr(e))
            return
        
    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return cpu_usage, memory_usage