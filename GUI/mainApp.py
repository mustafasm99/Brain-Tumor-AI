from PySide6 import QtWidgets 
from PySide6.QtWidgets import  QPushButton , QVBoxLayout ,QHBoxLayout 
from .fileExplorer import FileExplorer
from .resultt import Result
from .Analysis import Analysis
from .menu import menu

class widget(QtWidgets.QWidget):
     def __init__(self, *args, **kwargs):
          super(widget , self).__init__()
           
          content = QVBoxLayout()
          imageSection = QHBoxLayout()
          
          # get the fileExplorer and unpack the file path from it 
          self.result_widget = Result()
          
          imageSection.addWidget(self.result_widget , 1)
          imageSection.addWidget(FileExplorer() , 1)
          
          
          self.Analysis = Analysis()
          
          content.addLayout(imageSection)
          content.addWidget(self.Analysis)
         
          main = QtWidgets.QWidget()
          main.setLayout(content)
          # create the menu and its connections 
          self.menu_widget = menu()
          self.menu_widget.ResultLabelConnection.connect(self.result_widget.update_label_text)
          self.menu_widget.ResultSetContent.connect(self.result_widget.update_Result_label_content)
          self.menu_widget.ResultShowOutCome.connect(self.result_widget.show_out_come)
          self.menu_widget.StartWorker.connect(self.menu_widget.start_processing)
          self.result_widget.AnalysisSignal.connect(self.Analysis.show_content)
          
          
          layout = QHBoxLayout()
          layout.addWidget(self.menu_widget , 1)
          layout.addWidget(main , 4)
          self.setLayout(layout)
     
     