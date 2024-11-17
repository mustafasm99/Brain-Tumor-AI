# worker.py
# code for working the queue for the SVM and more other tasks


from PySide6.QtCore import QObject, QRunnable, Signal
from result.svm import SVM_LINER , SVM_LINER_DWT , RPF , RPF_DWT , POLY , POLY_DWT
from result.cnn import CNN
from result.knn import KNN , KNN_DWT


class WorkerSignals(QObject):
    finished = Signal()
    result_ready = Signal(list)
    error = Signal(str)

class Worker(QRunnable):
     def __init__(self, path , name=None):
          super().__init__()
          self.path = path
          self.signals = WorkerSignals()
          self.name    = name
          print("---- worker starting ----")
     
     def run(self):
          try:
               if self.name == "SVM-liner":
                    r = SVM_LINER(path=self.path)
                    result = r.run()
                    self.signals.result_ready.emit(result)
                    
               
               elif self.name == "SVM-liner-Dwt":
                    print("DWT is working")
                    r = SVM_LINER_DWT(path=self.path)
                    result = r.run()
                    self.signals.result_ready.emit(result) 
                    
                        
               elif self.name == "SVM-RPF":
                    print("RPF is working")
                    r = RPF(path=self.path)
                    result = r.run()
                    self.signals.result_ready.emit(result)
                    
                    
               elif self.name == "SVM-RPF-Dwt":
                    print("RPF-DWT is working")
                    r = RPF_DWT(path=self.path)
                    result = r.run()
                    self.signals.result_ready.emit(result)
                    
                    
               elif self.name == "SVM-Poly":
                    print("RPF-DWT is working")
                    r = POLY(path=self.path)
                    result = r.run()
                    self.signals.result_ready.emit(result)
                    
                    
               elif self.name == "SVM-Poly-Dwt":
                    print("SVM-POLY-DWT is working")
                    r = POLY_DWT(path=self.path)
                    result = r.run()
                    print(result)
                    self.signals.result_ready.emit(result)
               
               elif self.name == "CNN":
                    model     = CNN(image_path=self.path)
                    result    = model.run()
                    self.signals.result_ready.emit([result])
               
               elif self.name == "KNN":
                    model = KNN(image_path=self.path)
                    result = model.run()
                    self.signals.result_ready.emit([result])
               
               elif self.name == "KNN-Dwt":
                    model = KNN_DWT(image_path=self.path)
                    result = model.run()
                    self.signals.result_ready.emit([result])
               else:
                    print(self.name)
          
          except Exception as e:
               print("Error ===========>")
               self.signals.error.emit(str(e))
          finally:
               self.signals.finished.emit()
