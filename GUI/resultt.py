from PySide6.QtWidgets import (
    QGroupBox, QHBoxLayout, QVBoxLayout, QWidget,
    QLabel, QStackedWidget, QPushButton ,
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from .charts import BarChartSVM, CNN_CHART
from .settings import clear_layout


class Result(QWidget):
    AnalysisSignal = Signal(type(BarChartSVM))
    showAnalysis = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        
        self.setFixedSize(self.screen().size().width() * 0.6, 350)
          
        self.label = QLabel("Accuracy and other info will show here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #333; padding: 10px;")
        self.label.setObjectName("anaLabel")

        self.layout.addWidget(self.label)

        self.stackedWidget = None  # Initialize as None
        self.navLayout = None  # Initialize as None

    def update_label_text(self, text):
        """Update label text with proper error handling."""
        try:
            self.label.setText(text)
        except Exception as e:
            print(f"Error updating label: {e}")
            clear_layout(self.layout)
            self.layout.update()
            label = QLabel(text)
            label.setObjectName("resultLabel")
            self.layout.addWidget(label)

    def update_Result_label_content(self, content):
        """Clear layout and update it with new content."""
        self.loader = content
        self.showAnalysis = []
        clear_layout(self.layout)

        # Ensure navigation layout and stacked widget are reset
        self.navLayout = None
        self.stackedWidget = None

        print("The layout is cleared")
        self.layout.addWidget(self.loader)

    def show_out_come(self, result):
        """Display the outcome with navigation and stacked widget."""
        clear_layout(self.layout)
        print("=========> The layout is cleared")

        # Create stacked widget and navigation layout
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

        # Populate the stacked widget
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

        # Emit appropriate signal based on analysis
        if len(self.showAnalysis) > 0:
            self.AnalysisSignal.emit(BarChartSVM(data=self.showAnalysis))
        else:
            self.AnalysisSignal.emit(CNN_CHART(data=result))

    def show_previous(self):
        """Navigate to the previous page in the stacked widget."""
        if self.stackedWidget is not None:
            current_index = self.stackedWidget.currentIndex()
            if current_index > 0:
                self.stackedWidget.setCurrentIndex(current_index - 1)

    def show_next(self):
        """Navigate to the next page in the stacked widget."""
        if self.stackedWidget is not None:
            current_index = self.stackedWidget.currentIndex()
            if current_index < self.stackedWidget.count() - 1:
                self.stackedWidget.setCurrentIndex(current_index + 1)
