import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolTip, QPushButton, QFileDialog
)

from pychromecast import get_chromecasts

from caster import Caster


class ControlWindow(QMainWindow):

    window_shown = pyqtSignal()
    _chromecast_loaded = pyqtSignal()
    _media_loaded = pyqtSignal()
    _media_stopped = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._playing = False
        self._stop_discovery = None
        self._caster = None
        self._setup_ui()

    def _load_chromecasts(self):

        self._stop_discovery = get_chromecasts(
            blocking=False,
            callback=self._handle_chromecast
        )
        self._set_status('Looking for chromecasts...')

    def _handle_chromecast(self, chromecast):
        self._stop_discovery()
        chromecast.socket_client.start()
        self._caster = Caster(chromecast)
        self._set_status("Found %s at %s" % (
            chromecast.name, chromecast.host))
        self._chromecast_loaded.emit()

    def showEvent(self, event):

        super().showEvent(event)
        self.window_shown.emit()

    def _setup_ui(self):

        # QToolTip.setFont(QFont('SansSerif', 10))

        # self.setToolTip('This is a <b>QWidget</b> widget')

        # button_open = QFileDialog(self)
        button_open = QPushButton("Open", self)
        button_open.setDisabled(True)
        button_open.clicked.connect(self._on_open)

        btn_playpause = QPushButton('Play / Pause', self)
        btn_playpause.move(100, 0)
        btn_playpause.clicked.connect(self._on_playpause)
        btn_playpause.setDisabled(True)

        button_stop = QPushButton("Stop", self)
        button_stop.clicked.connect(self._on_stop)
        button_stop.setDisabled(True)
        button_stop.move(200, 0)

        # btn3 = QPushButton('Pause', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())


        self.window_shown.connect(self._load_chromecasts)

        self._chromecast_loaded.connect(lambda: button_open.setDisabled(False))

        self._media_loaded.connect(lambda: button_open.setDisabled(True))
        self._media_loaded.connect(lambda: btn_playpause.setDisabled(False))
        self._media_loaded.connect(lambda: button_stop.setDisabled(False))

        self._media_stopped.connect(lambda: button_open.setDisabled(False))
        self._media_stopped.connect(lambda: btn_playpause.setDisabled(True))
        self._media_stopped.connect(lambda: button_stop.setDisabled(True))

        self.setGeometry(300, 300, 300, 50)
        self.setWindowTitle('Chromecast')
        self.show()

    def _set_status(self, message):
        self.statusBar().showMessage(message)

    def _on_open(self):

        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            self._caster.play_media(filename)
            self._media_loaded.emit()
            self._set_status("Now playing %s" % filename)
            self._playing = True

    def _on_playpause(self):
        if self._playing:
            print("Pause")
            self._caster.pause()
        else:
            print("Play")
            self._caster.play()

        self._playing = not self._playing

    def _on_stop(self):
        self._caster.stop()
        self._media_stopped.emit()
        self._set_status("Stopped.")


if __name__ == '__main__':

    app = QApplication(sys.argv)

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()

    control_window = ControlWindow()

    sys.exit(app.exec_())
