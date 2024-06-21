from PySide6.QtWidgets import QBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from .settings import set_path

class FileExplorer(QWidget):
  def __init__(self , parent=None):
    super().__init__(parent)

    # Layout
    layout = QVBoxLayout(self)
    layout.setObjectName("fileHolder")
    
    self.setFixedSize(250 , 350)
    # Button
    self.button = QPushButton("Open File Explorer")
    self.button.setObjectName("fileButton")
    self.button.clicked.connect(self.open_file_dialog)

    # Info label
    self.info_label = QLabel("No file selected")
    self.info_label.setObjectName("fileLabel")
    self.info_label.setFixedSize(250,250)
    
    

    # Add to layout
    layout.addWidget(self.button , 2)
    layout.addWidget(self.info_label , 2)
        

  def open_file_dialog(self):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
    if file_path:
      pixmap = QPixmap(file_path)
      self.info_label.setPixmap(pixmap.scaled(self.info_label.size() ,  Qt.KeepAspectRatio))
      set_path(file_path)
      