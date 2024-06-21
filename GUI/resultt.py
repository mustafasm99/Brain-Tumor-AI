from PySide6.QtWidgets   import  QGroupBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QStackedWidget, QPushButton, QFrame
from PySide6.QtCore      import Signal
from .charts             import BarChartSVM , CNN_CHART
from .settings           import clear_layout


class Result(QWidget):
     
     AnalysisSignal = Signal(type(BarChartSVM))
     showAnalysis   = []
     
     def __init__(self, parent=None):
          super().__init__(parent)

          self.layout = QVBoxLayout(self)
          self.label = QLabel("Accuracy and other info will show here")
          self.label.setObjectName("anaLabel")

          self.layout.addWidget(self.label)

        

     def update_label_text(self, text):
          try:
               self.label.setText(text)
          except:
               clear_layout(self.layout)
               label = QLabel(text)
               label.setObjectName("resultLabel")
               self.layout.addWidget(label)

     def update_Result_label_content(self, content):
          self.loader = content
          clear_layout(self.layout)
          print("The layout is cleard")
          self.layout.addWidget(self.loader)

     def show_out_come(self, result):
          clear_layout(self.layout)

          self.stackedWidget = QStackedWidget()
          self.layout.addWidget(self.stackedWidget)

          self.navLayout = QHBoxLayout()
          self.prevButton = QPushButton("Previous")
          self.nextButton = QPushButton("Next")
          self.prevButton.clicked.connect(self.show_previous)
          self.nextButton.clicked.connect(self.show_next)
          self.navLayout.addWidget(self.prevButton)
          self.navLayout.addWidget(self.nextButton)

          self.layout.addLayout(self.navLayout)
          
          
          for i in result:
               newHolder = QVBoxLayout()
               name = ""
               for j in i.keys():
                    if j != "prediction":
                         dataHolder = QHBoxLayout()
                         
                         nameLabel = QLabel(str(j))
                         valueLabel = QLabel(str(i[j]))

                         nameLabel.setObjectName("resultLabel")
                         nameLabel.setFixedHeight(30)
                         
                         valueLabel.setObjectName("resultLabel")
                         valueLabel.setFixedHeight(30)
                         
                         
                         dataHolder.addWidget(nameLabel)
                         dataHolder.addWidget(valueLabel)
                         newHolder.addLayout(dataHolder)
                    else:
                         self.showAnalysis.append(i[j])
                         name = i[j]['title']

               group = QGroupBox(f"result {name}")
               group.setLayout(newHolder)
               group.setObjectName("ResultGroup")
               self.stackedWidget.addWidget(group)
               
          if len(self.showAnalysis) > 0:
               self.AnalysisSignal.emit(BarChartSVM(data=self.showAnalysis))
          else:
               self.AnalysisSignal.emit(CNN_CHART(data=result))

     def show_previous(self):
          current_index = self.stackedWidget.currentIndex()
          if current_index > 0:
               self.stackedWidget.setCurrentIndex(current_index - 1)

     def show_next(self):
          current_index = self.stackedWidget.currentIndex()
          if current_index < self.stackedWidget.count() - 1:
               self.stackedWidget.setCurrentIndex(current_index + 1)

     
