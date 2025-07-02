from watchdog.events import FileSystemEventHandler
from PyQt6.QtCore import pyqtSignal, QObject

class ChangeHandler(QObject, FileSystemEventHandler):
    # Signals
    progress_signal = pyqtSignal(int)

    # Constructor
    def __init__(self, 
        lbl_progress = None):
        super(ChangeHandler, self).__init__()

        # Properties
        self.items_in_folder = 0
        self.lbl_progress = lbl_progress

        # Conecta la señal a la función de actualización
        self.progress_signal.connect(self.update_progress)

    def on_created(self, event):
        if(event.src_path):
            self.items_in_folder += 1
            self.progress_signal.emit(self.items_in_folder)

    def update_progress(self, value):
       if self.lbl_progress is not None:
            self.lbl_progress.setText(f"Total images created: {value}")