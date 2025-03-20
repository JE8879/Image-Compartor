import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QPushButton, QLabel, QApplication, QWidget, QTabWidget

class CameraView(QWidget):
    # Constructor
    def __init__(self, main_window=None):
        super(CameraView, self).__init__()

        # Properties
        self.main_window = main_window

        self.draw_components()
        # self.manage_signals()

    def draw_components(self):
        # Load template
        uic.loadUi('Views/Templates/CameraView.ui', self)

    def closeEvent(self, event):
        if self.main_window:
            self.main_window.show()
        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = CameraView()

    app.exec()