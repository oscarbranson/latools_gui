
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QApplication
## Basic Widgets are located in PyQt5.Widgets
from PyQt5.QtGui import *


class Button(QWidget):
    def __init__(self): ##Initialisation
        super().__init__()
        self.initUI() ##Runs the gui creation below

    def initUI(self):
        
        btn = QPushButton('Button_Test',self) ##Creates button object
        btn.resize(btn.sizeHint())
        btn.move(50,50)

        btn.clicked.connect(QApplication.instance().quit) ##Supposed to kill app????

        self.setGeometry(300,300,300,200)
        self.show()
        self.setWindowTitle("Basic")


if __name__ == '__main__':
    
    app = QApplication(sys.argv)## Sys.argv is a list of commands from command line.
    test = Button()
    ## w = QWidget()
    ##w.resize(250, 150)
    ##w.move(300, 300)
    ##w.setWindowTitle('Simple')
    ##w.show()
    
    sys.exit(app.exec_())
