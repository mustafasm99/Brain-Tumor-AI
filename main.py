from GUI.mainApp import widget
from PySide6 import QtWidgets
import sys


if __name__ == "__main__":
     app = QtWidgets.QApplication([])

     widget = widget()
     widget.resize(1800, 970)
     widget.show()
     with open("style/style.qss" , 'r') as f :
          _style = f.read()
          app.setStyleSheet(_style)
     sys.exit(app.exec())