import os
import psutil
import time
import tracemalloc

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from time import sleep

class SignPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack

        pageLabel = QLabel("Multiplicative Encryption")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        #  Create and configure labels
        self.shift_label = QLabel("Key:")
        self.plaintext_label = QLabel("Plaintext:")
        self.ciphertext_label = QLabel("Ciphertext:")

        # Create and configure input fields
        self.shift_input = QTextEdit()        
        self.shift_input.setPlaceholderText("Key must be one of 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23 and 25")
        self.shift_input.setStyleSheet("font-size: 18px; padding: 5px; height: 20px; ")

        self.textfile_button = QPushButton("Select plain text file")
        self.textfile_button.setFixedWidth(150)  # Set fixed width
        self.textfile_button.setFixedHeight(25)  # Set fixed height
        self.textfile_button.clicked.connect(lambda: self.pick_text_file())
        self.textfile_label = QLabel("No file selected")

        # Layout for file picker 1
        textfile_layout = QHBoxLayout()
        textfile_layout.addStretch()
        textfile_layout.addWidget(self.textfile_button)
        textfile_layout.addWidget(self.textfile_label)
        textfile_layout.addStretch()

        self.plaintext_input = QTextEdit()
        self.plaintext_input.setReadOnly(True)
        self.plaintext_input.setFixedHeight(90)
        self.plaintext_input.setStyleSheet("font-size: 12px; margin-bottom: 25px;")

        self.ciphertextfile_button = QPushButton("Select cipher text file")
        self.ciphertextfile_button.setFixedWidth(150)  # Set fixed width
        self.ciphertextfile_button.setFixedHeight(25)  # Set fixed height
        self.ciphertextfile_button.clicked.connect(lambda: self.pick_ciphertext_file())
        self.ciphertextfile_label = QLabel("No file selected")

        # Layout for file picker 1
        ciphertextfile_layout = QHBoxLayout()
        ciphertextfile_layout.addStretch()
        ciphertextfile_layout.addWidget(self.ciphertextfile_button)
        ciphertextfile_layout.addWidget(self.ciphertextfile_label)
        ciphertextfile_layout.addStretch()

        self.ciphertext_output = QTextEdit()
        self.ciphertext_output.setReadOnly(True)
        self.ciphertext_output.setFixedHeight(90)
        self.ciphertext_output.setStyleSheet("font-size: 12px; margin-bottom: 25px;")

        self.key_result_label = QLabel("Brute force result:")
        self.key_result_output = QTextEdit()
        self.key_result_output.setReadOnly(True)
        self.key_result_output.setStyleSheet("font-size: 13px; padding: 5px; height: 60px;")

        self.analysis_output_label = QLabel("Calculation Time:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setStyleSheet("font-size: 13px; padding: 5px; height: 10px;")

        # Layout for inputs
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.shift_label)
        input_layout.addWidget(self.shift_input)

        input_layout.addWidget(self.plaintext_label)
        input_layout.addWidget(self.plaintext_input)
        input_layout.addLayout(textfile_layout)

        input_layout.addWidget(self.ciphertext_label)
        input_layout.addWidget(self.ciphertext_output)
        input_layout.addLayout(ciphertextfile_layout)

        input_layout.addWidget(self.key_result_label)
        input_layout.addWidget(self.key_result_output)

        input_layout.addWidget(self.analysis_output_label)
        input_layout.addWidget(self.analysis_output)

        # Create and configure the "Encrypt, Decrypt" buttons
        encrypt_button = QPushButton("Encrypt")
        encrypt_button.setStyleSheet("font-size: 18px; padding: 10px;")
        encrypt_button.clicked.connect(self.encrypt_btn_clicked)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.setStyleSheet("font-size: 18px; padding: 10px;")
        decrypt_button.clicked.connect(self.decrypt_btn_clicked)

        attack_button = QPushButton("Attack")
        attack_button.setStyleSheet("font-size: 18px; padding: 10px;")
        attack_button.clicked.connect(self.attack_btn_clicked)

        # Create and configure the "Save As" button
        save_button = QPushButton("Save File")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_to_file_btn_clicked)

        # Layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(encrypt_button)
        button_layout.addWidget(decrypt_button)
        button_layout.addWidget(attack_button)
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

        self.is_decryption = False
        self.is_encryption = False

        self.textfile_path = None
        self.cipherfile_path = None
        self.validKeys = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    def go_back(self):
        self.plaintext_input.setPlainText("")
        self.ciphertext_output.setPlainText("")
        self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.shift_input.setPlainText(None)
        self.textfile_path = None
        self.cipherfile_path = None
        self.is_decryption = False
        self.is_encryption = False
        self.stack.setCurrentIndex(0)

    def clear(self):
        self.plaintext_input.setPlainText("")
        self.ciphertext_output.setPlainText("")
        self.key_result_output.setPlainText("")
        self.analysis_output.setPlainText("")
        self.textfile_label.setText("No file selected")
        self.ciphertextfile_label.setText("No file selected")
        self.shift_input.setPlainText(None)
        self.textfile_path = None
        self.cipherfile_path = None
        self.is_decryption = False
        self.is_encryption = False

    def attack_btn_clicked(self):
        self.is_decryption = False
        self.is_encryption = False   
        cipherText = self.ciphertext_output.toPlainText()
        if not cipherText:
            QMessageBox.critical(self, "Error", "Cipher text must be provided")
            return
        
        tracemalloc.start()

        start_time = time.time()        
        brute_text = self.brute_attack(cipherText)
        end_time = time.time()
        
        current, peak = tracemalloc.get_traced_memory()
        time_taken_ms = (end_time - start_time) * 1000
        cpu_usage, memory_usage = self.monitor_resources()

        timeTakenAnalysis = f"Time taken: {time_taken_ms:.2f} ms"
        combinedAnalysis = f"{timeTakenAnalysis}"

        if brute_text:
            self.key_result_output.setPlainText(brute_text)
            self.analysis_output.setPlainText(combinedAnalysis)  

            dialog = QDialog(self)
            dialog.setWindowTitle("Brute force attack result")
            dialog.setMinimumSize(500, 400)

            # Create a QTextEdit for displaying the long text
            text_edit = QTextEdit(dialog)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("font-size: 14px; padding: 10px;")

            # Set the long text to the text edit
            text_edit.setPlainText(brute_text)

            # Create and configure the "Close" button
            close_button = QPushButton("Close")
            close_button.setStyleSheet("font-size: 16px; padding: 5px;")
            close_button.clicked.connect(dialog.accept)

            # Layout for the dialog
            dialog_layout = QVBoxLayout()
            dialog_layout.addWidget(text_edit)

            # Layout for the close button
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(close_button)
            button_layout.addStretch()
            
            dialog_layout.addLayout(button_layout)

            # Set layout for the dialog
            dialog.setLayout(dialog_layout)

            # Show the dialog
            dialog.exec()
            
        else:
            QMessageBox.warning(self, "Not OK", "Unable to perform brute force attacking")

    def brute_attack(self, cipherText):    
        shiftKeys = self.validKeys
        brute_text = ""
        for key in shiftKeys:
            result = f"Plain text at key {key}: \n"            
            inv_key = self.mod_inverse(key, 26)        
            for char in cipherText:
                if char.isupper():
                    result += chr((ord(char) - 65) * inv_key % 26 + 65)
                elif char.islower():
                    result += chr((ord(char) - 97) * inv_key % 26 + 97)
                else:
                    result += char
            result += "\n\n\n"
            brute_text += result
        return brute_text

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
            
    def pick_text_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            file_size = os.stat(file_path).st_size/1024
            self.textfile_path = file_path
            self.textfile_label.setText(f"Text file selected, {file_size:.2f} KB in file size")
            try:
                with open(self.textfile_path, 'r') as plainTextFile:
                    plainText = plainTextFile.read()
                    if plainText:
                        self.plaintext_input.setPlainText(plainText)
            except Exception as e:
                errMsg = "Opening plaintext file failed: %s " %e
                QMessageBox.critical(self, "Error", errMsg)

    def pick_ciphertext_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cipher Text File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            file_size = os.stat(file_path).st_size/1024
            self.cipherfile_path = file_path
            self.ciphertextfile_label.setText(f"Cipher text file selected, {file_size:.2f} KB in file size")
            try:
                with open(self.cipherfile_path, 'r') as cipherTextFile:
                    cipherText = cipherTextFile.read()
                    if cipherText:
                        self.ciphertext_output.setPlainText(cipherText)
            except Exception as e:
                errMsg = "Opening cipher text file failed: %s " %e
                QMessageBox.critical(self, "Error", errMsg)

    def encrypt_btn_clicked(self):
        self.is_encryption = True
        self.is_decryption = False
        self.analysis_output.setPlainText("")
        shiftKey = self.shift_input.toPlainText()
        shiftKey = int(shiftKey)
        plainText = self.plaintext_input.toPlainText()
        if not shiftKey in self.validKeys:
            QMessageBox.critical(self, "Error", "Key is incorrect")
            return 1
        if not plainText:
            QMessageBox.critical(self, "Error", "Plain text is empty")
            return 1
        
        tracemalloc.start()
        start_time = time.time()        
        self.encrypt(plainText, shiftKey)
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
    
    def decrypt_btn_clicked(self):
        self.is_encryption = False
        self.is_decryption = True
        self.analysis_output.setPlainText("")
        shiftKey = self.shift_input.toPlainText()
        shiftKey = int(shiftKey)
        cipherText = self.ciphertext_output.toPlainText()
        if not shiftKey in self.validKeys:
            QMessageBox.critical(self, "Error", "Key must be between 0 and 25")
            return 1
        if not cipherText:
            QMessageBox.critical(self, "Error", "Cipher text is empty")
            return 1
        
        tracemalloc.start()
        start_time = time.time()              
        self.decrypt(cipherText, shiftKey)        
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()       
        cpu_usage, memory_usage = self.monitor_resources()
        
        time_taken_ms = (end_time - start_time) * 10**3

        timeTakenAnalysis = f"Time taken: {time_taken_ms:.2f} ms"
        cpuUsageAnalysis = f"CPU usage: {cpu_usage}%"        
        memoryUsageAnalysis = f"Memory usage: {peak / 10**3} KB"        
        combinedAnalysis = f"{timeTakenAnalysis}"
        # combinedAnalysis = f"{timeTakenAnalysis}\n{cpuUsageAnalysis}\n{memoryUsageAnalysis}"

        self.analysis_output.setPlainText(combinedAnalysis)

    def mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1
    
    def encrypt(self, text, key):
        result = ""
        for char in text:
            if char.isupper():
                result += chr((ord(char) - 65) * key % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - 97) * key % 26 + 97)
            else:
                result += char
        
        self.ciphertext_output.setPlainText(result)
        return 0
    
    def decrypt(self, cipher_text, key):        
        result = ""
        # Calculate the modular multiplicative inverse of the key
        inv_key = self.mod_inverse(key, 26)
        try:
            for char in cipher_text:
                if char.isupper():
                    result += chr((ord(char) - 65) * inv_key % 26 + 65)
                elif char.islower():
                    result += chr((ord(char) - 97) * inv_key % 26 + 97)
                else:
                    result += char

        except ValueError:
            QMessageBox.critical(self, "Error", "Key is not valid")
            return 1
        
        self.plaintext_input.setPlainText(result)
        return 0

    def monitor_resources(self, interval=1):
        cpu_usage = psutil.cpu_percent(interval=interval)
        memory_info = psutil.virtual_memory()
        return cpu_usage, memory_info.percent