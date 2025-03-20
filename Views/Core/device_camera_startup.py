
import numpy as np
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

class DeviceCamera(QThread):

    # Signals
    change_pixmap_signal = pyqtSignal(QPixmap)

    # Constructor 
    def __init__(self):
        super(DeviceCamera, self).__init__()

        # Properties
        self._cap = None
