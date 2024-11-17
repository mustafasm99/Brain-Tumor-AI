from PySide6.QtCharts import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                              QChartView, QValueAxis )
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter , QCursor
from PySide6.QtWidgets import QLabel , QWidget , QHBoxLayout , QToolTip

class BarChartSVM(QWidget):
     def __init__(self,parent=None, data:list = []):
          super().__init__(parent)
          
          self.layout = QHBoxLayout()
          
          
          self.names               = []
          self.accuracys           = []
          self.losses              = []
          self.predicted_classes   = []
          
          for i in data:
               self.names.append(i['title'])
               self.accuracys.append(i['Accuracy'])
               self.losses.append(i['loss'])
               self.predicted_classes.append(i['predicted_class'])
          
          
          self.series  = QBarSeries()
          
          self.set_0 = QBarSet("accuracy")
          self.set_1 = QBarSet("loss")
          
          self.set_0.append([float(i) for i in self.accuracys])
          self.set_1.append([float(i) for i in self.losses])
          
          self.series.append(self.set_0)
          self.series.append(self.set_1)
          
          self.series.hovered.connect(self.tooltip)
          
          self.chart = QChart()
          self.chart.addSeries(self.series)
          self.chart.setTitle("Loss/Accuracy")
          self.chart.setAnimationOptions(QChart.SeriesAnimations)
          
          self.axis_x = QBarCategoryAxis()
          self.axis_x.append(self.names)
          self.chart.addAxis(self.axis_x, Qt.AlignBottom)
          self.series.attachAxis(self.axis_x)
          
          self.axis_y = QValueAxis()
          self.axis_y.setRange(0, 100)
          self.chart.addAxis(self.axis_y, Qt.AlignLeft)
          self.series.attachAxis(self.axis_y)

          self.chart.legend().setVisible(True)
          self.chart.legend().setAlignment(Qt.AlignBottom)

          self._chart_view = QChartView(self.chart)
          self._chart_view.setRenderHint(QPainter.Antialiasing)
          
          self.layout = QHBoxLayout()
          self.layout.addWidget(self._chart_view)
          text = ""
          for index,data in enumerate(self.names):
               print(data)
               text += f"""
                    {data} : {self.predicted_classes[index]}
                    """
          self.label  = QLabel(text)
          self.label.setObjectName("anaLabelR")
          text = ""
          self.layout.addWidget(self.label)
          self.setLayout(self.layout)
          
     def tooltip(self , status , index , barset):
          if status:
               values = barset.at(index)
               cat    = self.names[index]
               tool   = f"{barset.label()} : {values} ({cat})"
               QToolTip.showText(QCursor.pos() , tool)
          else:
               QToolTip.hideText()


class CNN_CHART(QWidget):
     def __init__(self, parent=None , data : dict = {}):
          super().__init__(parent)
          
          self.layout = QHBoxLayout()
          self.names  =['Accuracy' , 'Loss']
          self.chart = QChart()
          
          self.series  = QBarSeries()
          
          self.set_0 = QBarSet(self.names[0])
          self.set_1 = QBarSet(self.names[1])
          
          self.set_0.append(data[0]['accuracy']*100)
          self.set_1.append(data[0]['loss']*100)
          
          self.series.append(self.set_0)
          self.series.append(self.set_1)
          
          self.series.hovered.connect(self.tooltip)
          
          self.chart = QChart()
          self.chart.addSeries(self.series)
          self.chart.setTitle("Loss/Accuracy")
          self.chart.setAnimationOptions(QChart.SeriesAnimations)
          
          
          
          self.axis_y = QValueAxis()
          self.axis_y.setRange(0, 100)
          self.chart.addAxis(self.axis_y, Qt.AlignLeft)
          self.series.attachAxis(self.axis_y)

          self.chart.legend().setVisible(True)
          self.chart.legend().setAlignment(Qt.AlignBottom)

          self._chart_view = QChartView(self.chart)
          self._chart_view.setRenderHint(QPainter.Antialiasing)
          
          self.layout = QHBoxLayout()
          self.layout.addWidget(self._chart_view)
          
          self.setLayout(self.layout)
     
     
     def tooltip(self , status , index , barset):
          if status:
               values = barset.at(index)
               cat    = self.names[index]
               tool   = f"{barset.label()} : {values} ({cat})"
               QToolTip.showText(QCursor.pos() , tool)
          else:
               QToolTip.hideText()