# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 00:22:54 2024

@author: NASUS
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from rembg import remove
import cv2
import os

class BackgroundRemoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Background Remover |N.T.")
        self.resize(350, 200)
        self.initUI()

    def initUI(self):
        self.select_button = QPushButton("Select Image", self)
        self.select_button.clicked.connect(self.select_image)

        self.clear_button = QPushButton("Clear Result", self)
        self.clear_button.clicked.connect(self.clear_result)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.processing_label = QLabel("Processing...", self)
        self.processing_label.setAlignment(Qt.AlignCenter)
        self.processing_label.setStyleSheet("font-weight: bold; color: blue")
        self.processing_label.hide()

        self.welcome_label = QLabel("Select the image from which the background will be removed\nSupported formats: PNG, JPG, JPEG", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.processing_label)

        self.setLayout(layout)

    def select_image(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
            file_dialog.setViewMode(QFileDialog.Detail)
            file_dialog.fileSelected.connect(self.remove_background)
            file_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}", QMessageBox.Ok)

    def remove_background(self, file_path):
        try:
            self.processing_label.show()  # Show "Processing..." label when processing starts
            QApplication.processEvents()  # Update the interface to make "Processing..." label visible

            with open(file_path, "rb") as f:
                img = f.read()
            output_img = remove(img)
            
            # Create the output file name
            temp_path, file_name = os.path.split(file_path)
            file_name, extension = os.path.splitext(file_name)
            output_image = os.path.join(temp_path, file_name + "_output" + extension)
            
            with open(output_image, "wb") as f:
                f.write(output_img)

            # Display the result
            img = cv2.imread(output_image)
            if img is not None:
                QMessageBox.information(self, "Success", "The visual is saved to the location of the photo.", QMessageBox.Ok)
                height, width, _ = img.shape
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                q_img = QImage(img.data, width, height, QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(q_img))
            else:
                QMessageBox.warning(self, "Error", "An error occurred while displaying the image.", QMessageBox.Ok)

            self.processing_label.hide()  # Hide "Processing..." label when processing is finished

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}", QMessageBox.Ok)

    def clear_result(self):
        self.image_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundRemoverApp()
    window.show()
    sys.exit(app.exec_())
