import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QPixmap

from . device_camera_startup import DeviceCamera

class VideoProccessingHandler(DeviceCamera):
    # Constructor
    def __init__(self,
        lbl_camera=None,
        type_capture=None,
        path_to_save=None,
        capture_duration=None,
        total_images=None):
        super(VideoProccessingHandler, self).__init__()

        # Properties
        self.lbl_camera = lbl_camera

        self.path_to_save = path_to_save
        self.type_capture = type_capture
        self.capture_duration = capture_duration
        self.total_images = total_images

    def start_video_capture(self):
        self.video_capture_instance = DeviceCamera(
            type_capture=self.type_capture,
            path_to_save=self.path_to_save,
            capture_duration=self.capture_duration,
            total_images=self.total_images
        )
        self.video_capture_instance.change_pixmap_signal.connect(self.update_image)
        self.video_capture_instance.start()

    @pyqtSlot(QPixmap)
    def update_image(self, pixmap_image):
        self.lbl_camera.setScaledContents(True)
        self.lbl_camera.setPixmap(pixmap_image)

    def stop_video_capture(self):
        self.video_capture_instance.stop()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    instance = VideoProccessingHandler()

    app.exec()