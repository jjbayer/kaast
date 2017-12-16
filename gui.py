from PyQt5.QtWidgets import QApplication, QWidget


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QFileDialog
from PyQt5.QtGui import QFont    


class ControlWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self._playing = False
        self.setup_ui()
            
    def setup_ui(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        # btn1 = QFileDialog(self)
        btn1 = QPushButton("Open", self)
        btn2 = QPushButton('Play / Pause', self)

        btn1.clicked.connect(self.handle_open)
        # btn3 = QPushButton('Pause', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        btn2.move(50, 50)       
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Chromecast')    
        self.show()

    def on_open(self):

        filename = QFileDialog.getOpenFileName()
        self.caster.play(filename)

    def on_playpause(self): 
        if self._playing:
            self.caster.pause()
        else:
            self.caster.play()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()
    
    control_window = ControlWindow()

    sys.exit(app.exec_())