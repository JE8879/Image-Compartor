import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QPixmap

from . device_camera_startup import DeviceCamera

class VideoProccessingHandler(DeviceCamera):
    # Constructor
    def __init__(self,lbl_camera=None):
        super(VideoProccessingHandler, self).__init__()

        # Properties
        self.lbl_camera = lbl_camera

    def start_video_capture(self):
        self.video_capture_instance = DeviceCamera()
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