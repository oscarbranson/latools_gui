
import sys
from PyQt5.QtWidgets import *
## Basic Widgets are located in PyQt5.Widgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow():
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        app = QApplication(sys.argv)
        win = QWidget()
        box = QVBoxLayout()

        win.setLayout(box)
        win.setGeometry(300, 300, 300, 200)
        win.setWindowTitle("Example")
        
        
        box.addWidget(ControlPanel())
        box.addWidget(Disp())
        
        win.show()
        sys.exit(app.exec_())

class Disp(QWidget):
    def __init__(self):
        super().__init__()
        self.plh = QLabel("graph goeth here")
        self.pan1 = QFrame()
        self.pan1.setFrameShape(QFrame.StyledPanel)
        self.pan2 = QFrame()
        self.pan2.setFrameShape(QFrame.StyledPanel)

        self.pan1.resize(100,200)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.pan1)
        self.layout.addWidget(self.plh)
        self.layout.addWidget(self.pan2)
        self.setLayout(self.layout)
        
        
    
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

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.i = 1
        
        self.bn = QPushButton(self)
        self.bp = QPushButton(self)


        self.bn.setText("->")
        self.bp.setText("<-")

        #placeholder names
        #Changing this
        self.mlkth = QWidget()
        self.ysd = QWidget()
        self.bnh = QWidget()
        self.hod = QWidget()

        self.mlkthui()
        self.ysdui()
        self.bnhui()
        self.hodui()

        nextMove = self.nextcontrol()
        
        self.bn.clicked.connect(nextMove)
        self.bp.clicked.connect(self.prevcontrol())

        self.stack = QStackedWidget(self) ## Where stack is defined
        self.stack.addWidget (self.mlkth)
        self.stack.addWidget (self.ysd)
        self.stack.addWidget (self.bnh)
        self.stack.addWidget (self.hod)

        self.setLayout(layout)
        layout.addWidget(self.bp)
        layout.addWidget(self.stack)
        layout.addWidget(self.bn)

    def nextcontrol(self):
        self.i = self.i + 1
        self.stack.setCurrentIndex(i) 
        ## Stack is never defined here

    def prevcontrol(self):
        self.i = self.i - 1
        self.stack.setCurrentIndex(i)
        
    def mlkthui(self):
        layout = QFormLayout()
        layout.addRow("Placeholder 11", QLineEdit())
        layout.addRow("Placeholder 12", QLineEdit())
        self.mlkth.setLayout(layout) ## This is never defined here but THIS works?
        
    def ysdui(self):
        layout = QFormLayout()
        layout.addRow("Placeholder 21", QLineEdit())
        layout.addRow("Placeholder 22", QLineEdit())
        self.ysd.setLayout(layout)

    def bnhui(self):
        layout = QFormLayout()
        layout.addRow("Placeholder 31", QLineEdit())
        layout.addRow("Placeholder 32", QLineEdit())
        self.bnh.setLayout(layout)

    def hodui(self):
        layout = QFormLayout()
        layout.addRow("Placeholder 41", QLineEdit())
        layout.addRow("Placeholder 42", QLineEdit())
        self.hod.setLayout(layout)

if __name__ == '__main__':
    
    MainWindow()
