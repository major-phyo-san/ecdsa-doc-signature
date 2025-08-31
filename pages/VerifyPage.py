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

        self.docfile_button = QPushButton("Select document file")
        self.docfile_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.docfile_button.clicked.connect(lambda: self.pick_doc_file())
        self.docfile_label = QLabel("No file selected")
        self.docfile_label.setStyleSheet("font-size: 12px; padding: 10px;")

        self.sigfile_button = QPushButton("Select signature file")        
        self.sigfile_button.clicked.connect(lambda: self.pick_sig_file())
        self.sigfile_label = QLabel("No signature selected")
        self.sigfile_label.setStyleSheet("font-size: 12px; padding: 10px;")

        self.publickeyfile_button = QPushButton("Select public key file")        
        self.publickeyfile_button.clicked.connect(lambda: self.pick_publickey_file())
        self.publickeyfile_label = QLabel("No public key selected")
        self.publickeyfile_label.setStyleSheet("font-size: 12px; padding: 10px;")

        self.analysis_output_label = QLabel("Calculation Time:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setStyleSheet("font-size: 13px; padding: 5px; height: 10px;")

        # Create and configure the "Sign" button
        verify_button = QPushButton("Verify Document")
        verify_button.setStyleSheet("font-size: 18px; padding: 10px;")
        verify_button.clicked.connect(self.verify_btn_clicked)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.go_back)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("font-size: 18px; padding: 10px;")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout()

        pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pageLabel.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(pageLabel)

        # Input fields
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)

        # docfile col        
        docfile_col = QVBoxLayout()
        docfile_col.addWidget(self.docfile_button, alignment=Qt.AlignmentFlag.AlignCenter)
        docfile_col.addWidget(self.docfile_label, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addLayout(docfile_col)

        # sigfile col
        sigfile_col = QVBoxLayout()
        sigfile_col.addWidget(self.sigfile_button, alignment=Qt.AlignmentFlag.AlignCenter)
        sigfile_col.addWidget(self.sigfile_label, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addLayout(sigfile_col)

        # public key col
        publickey_col = QVBoxLayout()
        publickey_col.addWidget(self.publickeyfile_button, alignment=Qt.AlignmentFlag.AlignCenter)
        publickey_col.addWidget(self.publickeyfile_label, alignment=Qt.AlignmentFlag.AlignCenter)
        input_layout.addLayout(publickey_col)

        layout.addLayout(input_layout)

        # Verify button
        verify_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addSpacing(10)
        layout.addWidget(verify_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Analysis
        # layout.addSpacing(20)
        # layout.addWidget(self.analysis_output_label)
        # layout.addWidget(self.analysis_output)

        # Footer
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