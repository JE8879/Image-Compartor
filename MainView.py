import sys
from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLabel

from Views.CameraView import CameraView

class MainView(QWidget):
    # Constructor
    def __init__(self):
        super(MainView, self).__init__()

        self.draw_components()
        self.manage_signals()

    def draw_components(self):
        # Load template
        uic.loadUi('Views/Templates/MainView.ui', self)

        # Create font for title
        font = QFont("Century Gothic", 24)
        font.setWeight(QFont.Weight.Bold)

        # Title Label
        self.lbl_title = self.findChild(QLabel, 'lbl_title')
        self.lbl_title.setFont(font)

        self.btn_create_images = self.findChild(QPushButton, 'btn_create_images')
    
    def OpenCameraView(self):
        self.camera_view_instance = CameraView(main_window=self)
        self.camera_view_instance.show()
        self.hide()

    def manage_signals(self):
        self.btn_create_images.clicked.connect(self.OpenCameraView)
    
    
if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainView()

    window.show()

    app.exec()
