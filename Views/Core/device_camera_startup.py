import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

class DeviceCamera(QThread):
    # Signals
    change_pixmap_signal = pyqtSignal(QPixmap)

    # Constructor 
    def __init__(self, parent=None):
        super(DeviceCamera, self).__init__(parent)

        # Properties
        self._run_flag = True
        self._cap = None

    @pyqtSlot()
    def stop(self):
        self._run_flag = False
        self.wait()

    def run(self):
        self._cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
        # self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self._cap.set(cv2.CAP_PROP_FPS, 60)
        
        while(self._run_flag):
            ret, cv_img = self._cap.read()
            if(ret):
                pixmap_image = self.convert_cv2_image_to_q_pixmap(cv_img)
                self.change_pixmap_signal.emit(pixmap_image)
        self._cap.release()
        
    def convert_cv2_image_to_q_pixmap(self, MatLike):
        rgb_image = cv2.cvtColor(MatLike, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap_image = QPixmap.fromImage(q_image)
        return pixmap_image