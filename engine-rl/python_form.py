import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class PythonDynamicForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engine-RL Python Dynamic Form")
        self.resize(450, 320)
        self.setStyleSheet("background-color: #0b0e14; color: #f0f5ff;")
        
        layout = QVBoxLayout()
        
        lbl = QLabel("Engine-RL Python GUI Form (PyQt6)")
        lbl.setStyleSheet("color: #00d2ff; font-size: 13pt; font-weight: bold;")
        
        btn = QPushButton("Click Python Action")
        btn.setStyleSheet("background-color: #00b478; color: white; padding: 10px; font-weight: bold; border-radius: 4px;")
        btn.clicked.connect(self.on_click)
        
        layout.addWidget(lbl)
        layout.addWidget(btn)
        self.setLayout(layout)

    def on_click(self):
        print("Action triggered from Python Form!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = PythonDynamicForm()
    form.show()
    sys.exit(app.exec())