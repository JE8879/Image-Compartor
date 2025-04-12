from PyQt6.QtWidgets import QMessageBox

class Utilities:

    @staticmethod
    def show_message(message):
        """
        Show a message in a new Window.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        