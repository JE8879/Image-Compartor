import cv2
import time
import platform
from uuid import uuid4
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from . type_capture import TypeCapture, TypePlatform

class DeviceCamera(QThread):
    # Signals
    change_pixmap_signal = pyqtSignal(QPixmap)
    complete_signal = pyqtSignal(str)

    # Constructor 
    def __init__(self, 
        parent=None,
        type_capture=None,
        path_to_save=None,
        capture_duration=None,
        total_images=None):
        super(DeviceCamera, self).__init__(parent)

        # Properties
        self._run_flag = True
        self._cap = None
        self.list_images = []

        self.path_to_save = path_to_save
        self.type_capture = type_capture
        self.capture_duration = capture_duration
        self.total_images = total_images

    @pyqtSlot()
    def stop(self):
        self._run_flag = False
        self.wait()

    def run(self):
        os = platform.system()

        if os == TypePlatform.Windows.value:
            self._cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        else:
            self._cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
        self._cap.set(cv2.CAP_PROP_FPS, 60)

        
        # Diccionario de funciones de captura
        self.capture_options = {
            TypeCapture.General : self.capture_general,
            TypeCapture.Time    : self.capture_by_time,
            TypeCapture.Quantity: self.capture_by_quantity
        }

        if self.type_capture in self.capture_options:
            self.capture_options[self.type_capture]()
        self._cap.release()

    def capture_general(self):

        while(self._run_flag):
            ret, cv_img = self._cap.read()
            if(ret):
                pixmap_image = self.convert_cv2_image_to_q_pixmap(cv_img)
                self.change_pixmap_signal.emit(pixmap_image)

    def capture_by_time(self):
        start_time = time.time()
        self.list_images = []

        while int(time.time() - start_time) < self.capture_duration:
            ret, cv_img = self._cap.read()
            if ret:
                pixmap_image = self.convert_cv2_image_to_q_pixmap(cv_img)
                self.change_pixmap_signal.emit(pixmap_image)
                self.list_images.append(pixmap_image)
    
        for image in self.list_images:
            self.save_image(image, self.path_to_save)

        self.list_images = []
        self.complete_signal.emit("Capture completed")

    def capture_by_quantity(self):
        image_counter = 0

        while image_counter < self.total_images:
            ret , cv_img = self._cap.read()
            if ret:
                pixmap_image = self.convert_cv2_image_to_q_pixmap(cv_img)
                self.change_pixmap_signal.emit(pixmap_image)
                self.list_images.append(pixmap_image)

                image_counter += 1
        
        for image in self.list_images:
            self.save_image(image, self.path_to_save)
        
        self.list_images = []
        self.complete_signal.emit("Capture completed")

    def save_image(self, pixmap_image, path):
        full_path = f"{path}{self.generate_image_name()}.png"
        pixmap_image.save(full_path, "PNG")
    
    def generate_image_name(self):
        return str(uuid4())[0:7]
        
    def convert_cv2_image_to_q_pixmap(self, MatLike):
        rgb_image = cv2.cvtColor(MatLike, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w

        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap_image = QPixmap.fromImage(q_image)
        return pixmap_image
