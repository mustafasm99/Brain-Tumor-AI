from PySide6 import  QtWidgets , QtCore 
from PySide6.QtWidgets import  QListWidget , QListWidgetItem , QVBoxLayout 
from .settings import get_path 
from .worker import Worker
from .loader import Loader

class menu(QtWidgets.QWidget):
     # create in connections bettwen widgets
     ResultLabelConnection = QtCore.Signal(str)
     ResultSetContent      = QtCore.Signal(type(Loader))
     ResultShowOutCome     = QtCore.Signal(list)
     StartWorker           = QtCore.Signal()
     loading_mode          = False
     SelectedItem          = None
     
     def __init__(self , parent = None):
          super().__init__(parent)
          layout = QVBoxLayout(self)
          methods = [
               'SVM-Poly-Dwt',
               'SVM-liner-Dwt',
               'SVM-RPF-Dwt',
               'SVM-Poly',
               'SVM-liner',
               'SVM-RPF',
               
               'KNN-Dwt',
               'KNN',
               
               'CNN'
          ]
          menu = QListWidget()
          for i in methods:
               item = QListWidgetItem(i)
               item.setTextAlignment(QtCore.Qt.AlignCenter)
               menu.addItem(item)
          
          menu.itemClicked.connect(self.select_from_menu)
          layout.addWidget(menu)
          
          
     
     def select_from_menu(self , item):
          self.path = get_path()
          self.SelectedItem = item.text()
          
          if self.path is not None:
               if not self.loading_mode:
                    self.ResultSetContent.emit(Loader())
                    self.loading_mode = True
               self.StartWorker.emit()
          else:
               self.ResultLabelConnection.emit("path is not set correct")
     
     def on_worker_finished(self):
        self.loading_mode = False 
     
     def showError(self , error):
          self.ResultLabelConnection.emit(error)
     
     def start_processing(self):
        if self.path:
            worker = Worker(self.path , name=self.SelectedItem)
            worker.signals.result_ready.connect(self.ResultShowOutCome.emit)
            worker.signals.error.connect(self.showError)
            worker.signals.finished.connect(self.on_worker_finished)
            
            QtCore.QThreadPool.globalInstance().start(worker)