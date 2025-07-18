import os
import sys
import platform
from watchdog.observers import Observer
from PyQt6 import uic
from PyQt6.QtGui import QGuiApplication, QFileSystemModel
from PyQt6.QtWidgets import QPushButton, QLabel, QApplication, QWidget, QRadioButton, QSpinBox, QLineEdit, QTreeView

from .Utils.utilities import Utilities
from .Utils.change_handler import ChangeHandler
from .Core.type_capture import TypeCapture, TypePlatform
from .Core.video_processing_handler import VideoProccessingHandler

class ModelView(QWidget):
    # Constructor
    def __init__(self, main_window=None):
        super(ModelView, self).__init__()
        # Properties
        self.main_window = main_window
        self.processing_instance = None

        self.main_sys_path = self.get_sys_path()
        
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

        self.lbl_images_created = self.findChild(QLabel, 'lbl_images_created')

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
        self.btn_begin_image_capture.clicked.connect(self.start_camera)

    def load_directories(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(self.main_sys_path)
        self.images_root.setModel(self.model)
        self.images_root.setRootIndex(self.model.index(self.main_sys_path))

    def generate_model(self):
        if(len(self.model_name.text()) != 0):
            # Create model name
            self.main_sys_path += self.model_name.text()
            # Create the directory with the same name
            os.mkdir(self.main_sys_path)
            # Show message 
            Utilities.show_message(message=f"Model {self.model_name.text()} created successfully")
            # Set the model name
            self.main_sys_path += "/"
            # Start observer
            self.start_change_handler()
            # Disable Button
            self.btn_generate_model.setDisabled(True)
        else:
            Utilities.show_message(message="The Model name is required")

    def start_camera(self):
        if self.btn_generate_model.isEnabled():
            Utilities.show_message("Please, first create a model")
            return

        if self.rdb_time_based.isChecked() and self.spin_time_based.value() != 0:
            
            self.image_processing_instance = VideoProccessingHandler(
                lbl_camera=self.lbl_main_screen,
                type_capture=TypeCapture.Time,
                path_to_save=self.main_sys_path,

                lbl_images_created=self.lbl_images_created,
                model_name=self.model_name,
                btn_generate_model=self.btn_generate_model,
                capture_duration=self.spin_time_based.value()
            )
            self.image_processing_instance.start_video_capture()
         
        if self.rdb_quantity_based.isChecked() and self.spin_quantity_based.value() != 0:

            self.image_processing_instance = VideoProccessingHandler(
                lbl_camera=self.lbl_main_screen,
                type_capture=TypeCapture.Quantity,
                path_to_save=self.main_sys_path,

                lbl_images_created=self.lbl_images_created,
                model_name=self.model_name,
                btn_generate_model=self.btn_generate_model,
                total_images=self.spin_quantity_based.value()
            )
            self.image_processing_instance.start_video_capture()


    def start_change_handler(self):
        self.event_handler = ChangeHandler(self.lbl_images_created)
        self.observer = Observer()

        self.observer.schedule(self.event_handler, path=self.main_sys_path, recursive=False)
        self.observer.start()

    def get_sys_path(self) -> str:
        # Get current platform
        currentPlatform = platform.system()
        # Load Settings
        json_settings = Utilities.load_json_settings()

        if currentPlatform == TypePlatform.Linux.value:
            system_path = json_settings['directories']['ubuntu-models']
        else:
            system_path = json_settings['directories']['windows-models']
        return system_path


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = ModelView()

    app.exec()