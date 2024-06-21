from .settings import settings
from PySide6.QtWidgets import  QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt

class Loader(QWidget):
    def __init__(self):
        super().__init__()        
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(str(settings['BASE_DIR'])+"/style/loader.gif")
        self.label.setMovie(self.movie)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.movie.start()