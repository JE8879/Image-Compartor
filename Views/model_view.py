import os
import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QFileSystemModel
from PyQt6.QtWidgets import QPushButton, QLabel, QApplication, QWidget, QProgressBar, QRadioButton, QSpinBox, QLineEdit, QTreeView

from .Utils.utilities import Utilities

class ModelView(QWidget):
    # Constructor
    def __init__(self, main_window=None):
        super(ModelView, self).__init__()
        # Properties
        self.main_window = main_window
        self.processing_instance = None

        # Load Settings
        json_settins = Utilities.load_json_settings()
        self.models_path = json_settins['directories']['models']

        self.draw_components()
        self.load_directories()
        self.manage_signals()
    
    def draw_components(self):
        # Load Template
        uic.loadUi('Views/Templates/ModelView.ui', self)

        self.lbl_main_screen = self.findChild(QLabel, 'lbl_main_screen')

        self.model_name = self.findChild(QLineEdit, 'model_name')
        self.btn_generate_model = self.findChild(QPushButton, 'btn_generate_model')
        self.btn_undo_changes = self.findChild(QPushButton, 'btn_undo_changes')
        self.btn_begin_image_capture = self.findChild(QPushButton, 'btn_begin_image_capture')

        self.rdb_quantity_based = self.findChild(QRadioButton, 'rdb_quantity_based')
        self.rdb_time_based = self.findChild(QRadioButton, 'rdb_time_based')

        self.spin_quantity_based = self.findChild(QSpinBox, 'spin_quantity_based')
        self.spin_time_based = self.findChild(QSpinBox, 'spin_time_based')

        self.image_progressBar = self.findChild(QProgressBar, 'image_progressBar')
        self.image_progressBar.setValue(0)
        self.image_progressBar.setVisible(False)

        self.images_root = self.findChild(QTreeView, 'images_root')
    

    def center_window(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        # if(isinstance(self.processing_instance, VideoProccessingHandler)):
        #     self.processing_instance.stop_video_capture()
        if self.main_window:
            self.main_window.show()
        event.accept()

    def manage_signals(self):
        self.btn_generate_model.clicked.connect(self.generate_model)

    def load_directories(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(self.models_path)
        self.images_root.setModel(self.model)
        self.images_root.setRootIndex(self.model.index(self.models_path))

    def generate_model(self):
        if(len(self.model_name.text()) != 0):
            # Create model name
            self.models_path += self.model_name.text()
            # Create the directory with the same name
            os.mkdir(self.models_path)
            # Show message 
            Utilities.show_message(message=f"Model {self.model_name.text()} created successfully")
            self.models_path += "/"
        else:
            Utilities.show_message(message="The Model name is required")


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = ModelView()

    app.exec()