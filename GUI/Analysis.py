from PySide6.QtCore import Qt , Signal , Slot
from PySide6.QtWidgets import QVBoxLayout , QHBoxLayout , QWidget , QLabel
from .settings import clear_layout

class Analysis(QWidget):
     AnalysisSignal = Signal(list)
     def __init__(self, parent =  None ) :
          super().__init__(parent)
          
          self.layout = QHBoxLayout(self)
          self.label = QLabel("figures and orthe data will show here")
          self.label.setObjectName("anaLabel")
          self.setFixedHeight(450)
          self.layout.addWidget(self.label)
     
     @Slot( QWidget )  
     def show_content(self ,content):
          clear_layout(self.layout)
          self.chart = content
          self.layout.addWidget(self.chart)
          
          