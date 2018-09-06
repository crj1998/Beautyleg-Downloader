import random
from binascii import hexlify
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QLabel,QLineEdit,QGridLayout


def genpw(text):
    pubKey='010001'
    modulus='00e0b509f6259df8'
    text=text[::-1].encode()
    rsa=int(hexlify(text),16)**int(pubKey,16)%int(modulus,16)
    return format(rsa,'x').zfill(15)

class genpwWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createGridLayout()
        self.move(300,300)
        self.setFixedSize(450,100)
        self.setWindowTitle('激活码生成器')
    def setRandomIndex(self):
        result=''
        words='abcdefghijklmnopqrstuvwxyz'
        for i in range(random.randint(1,4)):
            result+=random.choice(words)
        while len(result)<5:
            result+=str(random.randint(0,9))
        result=list(result)
        random.shuffle(result)
        result=''.join(result)
        self.line1.setText(result)
        self.line2.setText(result+genpw(result))
    def genPW(self):
        get=self.line1.text()
        self.line2.setText(get+genpw(get))
    def createWidgets(self):
        self.lb1=QLabel('序列码：')
        self.lb2=QLabel('激活码：')
        self.rand=QPushButton(icon=QIcon('icon/rand.ico'))
        self.rand.setToolTip("随机")
        self.gen=QPushButton('产生')
        self.rand.minimumSizeHint()
        self.rand.clicked.connect(self.setRandomIndex)
        self.gen.clicked.connect(self.genPW)
        self.line1=QLineEdit()
        self.line2=QLineEdit()
        self.line1.setEchoMode(QLineEdit.Password)
        

    def createGridLayout(self):
        #新建表格排列对象，并设置间距为10
        grid=QGridLayout()
        grid.setSpacing(10)
        #表格布局
        grid.addWidget(self.lb1,1,0)
        grid.addWidget(self.line1,1,1)
        grid.addWidget(self.lb2,2,0)
        grid.addWidget(self.line2,2,1)
        grid.addWidget(self.rand,1,2)
        grid.addWidget(self.gen,2,2,1,3)
        #使能表格布局
        self.setLayout(grid)

def genpwText(number):
    words='abcdefghijklmnopqrstuvwxyz'
    for i in range(number):
        result=''
        for j in range(random.randint(1,4)):
            result+=random.choice(words)
        while len(result)<5:
            result+=str(random.randint(0,9))
        result=list(result)
        random.shuffle(result)
        result=''.join(result)
        print(result+genpw(result))
if __name__ == '__main__':
    import sys
    #app=QApplication(sys.argv)
    #interface=genpwWindow()
    #interface.show()
    #sys.exit(app.exec_())
    genpwText(50)