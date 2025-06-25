import sys
from uuid import uuid4
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QPushButton, QLabel, QApplication, QWidget, QTabWidget, QVBoxLayout, QFileDialog

from .Core.video_processing_handler import VideoProccessingHandler
from .Core.type_capture import TypeCapture
from .Utils.utilities import Utilities

class CameraView(QWidget):
    # Constructor
    def __init__(self, main_window=None):
        super(CameraView, self).__init__()

        # Properties
        self.main_window = main_window
        self.processing_instance  = None

        self.draw_components()
        self.manage_signals()
     
    def draw_components(self):
        # Load template
        uic.loadUi('Views/Templates/CameraView.ui', self)

        self.lbl_screen = self.findChild(QLabel, 'lbl_screen')
        self.btn_launch_camera = self.findChild(QPushButton, 'btn_launch_camera')
        self.btn_take_picture = self.findChild(QPushButton, 'btn_take_picture')

        self.tabContainer = self.findChild(QTabWidget, 'tabContainer')
        self.tabContainer.setTabsClosable(True)
        self.tabContainer.setMovable(True)
        self.btn_save_image = self.findChild(QPushButton, 'btn_save_image')

    def center_window(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_camera(self):
        
        self.processing_instance = VideoProccessingHandler(
            lbl_camera=self.lbl_screen,
            type_capture=TypeCapture.General
        )

        self.processing_instance.start_video_capture()        
        self.btn_launch_camera.setEnabled(False)

    def take_picture(self):

        if not isinstance(self.processing_instance, VideoProccessingHandler):
            # Show error message
            Utilities.show_message("Please launch the camera first.")
            return
        
        # Create a new tab
        generic_tab = QWidget()
        # Create a layout for the tab
        layout = QVBoxLayout(generic_tab)

        # Crear y agregar el label al layout
        lbl_image = QLabel()
        lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap_image = self.lbl_screen.pixmap()

        lbl_image.setPixmap(pixmap_image)
        lbl_image.setScaledContents(True)
        layout.addWidget(lbl_image)

        # Generar nombre único
        generic_name = str(uuid4())[0:8]
        # Create full name for the tab
        full_name = f"Image_{generic_name}.png"
        # Add the label to the tab
        self.tabContainer.addTab(generic_tab, full_name)
    

    def manage_signals(self):
        # Connect buttons to their respective functions
        self.btn_launch_camera.clicked.connect(self.start_camera)        
        self.btn_take_picture.clicked.connect(self.take_picture)
        self.btn_save_image.clicked.connect(self.save_image)

        # Connect tab events
        self.tabContainer.currentChanged.connect(self.tab_changed)
        self.tabContainer.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        # Remove the tab at the given index
        if index != 0:
            self.tabContainer.removeTab(index)

    def tab_changed(self):
        self.update_status()

    def update_status(self):
        # Get the current tab index and name
        index = self.tabContainer.currentIndex()
        # Get the name of the current tab
        self.name = self.tabContainer.tabText(index)

    def save_image(self):

        # Check if the tab is empty
        if self.tabContainer.currentIndex() == 0:
            # Show error message
            Utilities.show_message("Please take a picture first.")
            return
        
        # Get the current tab
        current_tab = self.tabContainer.currentWidget()
        # Get the label inside the current tab
        label = current_tab.findChild(QLabel)
        # Get the pixmap from the label
        pixmap = label.pixmap()
        # Save the pixmap to a file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", self.name, "Images (*.png *.jpg *.jpeg)")

        if file_path:
            # Save the image in the selected path
            pixmap.save(file_path)
            # Show success message
            Utilities.show_message(f"Image saved in {file_path}")
            # Remove the tab after saving
            self.tabContainer.removeTab(self.tabContainer.currentIndex())

    def closeEvent(self, event):
        if(isinstance(self.processing_instance, VideoProccessingHandler)):
            self.processing_instance.stop_video_capture()

        if self.main_window:
            self.main_window.show()
        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = CameraView()

    app.exec()