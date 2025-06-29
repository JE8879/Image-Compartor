import sys
# from screeninfo import get_monitors
from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication, QLabel

from Views.camera_view import CameraView
from Views.model_view import ModelView

class MainView(QWidget):
    # Constructor
    def __init__(self):
        super(MainView, self).__init__()

        self.draw_components()
        self.manage_signals()
        #self.get_screen_info()

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
        self.btn_create_model = self.findChild(QPushButton, 'btn_create_model')
    
    def OpenCameraView(self):
        self.camera_view_instance = CameraView(main_window=self)
        self.camera_view_instance.show()
        self.hide()

    def OpenModelView(self):
        self.model_view_instance = ModelView(main_window=self)
        self.model_view_instance.show()
        self.hide()

    def manage_signals(self):
        self.btn_create_images.clicked.connect(self.OpenCameraView)
        self.btn_create_model.clicked.connect(self.OpenModelView)

    # def get_screen_info(self):
    #     monitors = get_monitors()
    #     # Mostrar información de cada monitor
    #     for i, monitor in enumerate(monitors, 1):
    #         print(f"\nMonitor {i}:")
    #         print(f"Resolución: {monitor.width}x{monitor.height} píxeles")
    #         print(f"Posición: x={monitor.x}, y={monitor.y}")
    #         if hasattr(monitor, 'name'):
    #             print(f"Nombre: {monitor.name}")
    #         print(f"Principal: {'Sí' if monitor.is_primary else 'No'}")

    
    
if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainView()

    window.show()

    app.exec()
