import webbrowser

#webbrowser.open('https://www.baidu.com')

from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lb=QLabel(self)
        self.lb.setOpenExternalLinks(True)
        self.lb.setText("<style>a:link {text-decoration: none;}a:visited {text-decoration: none;}a:active {text-decoration: none;}a:hover {text-decoration: none;}</style> <a href='https://github.com/crj1998' a>打开github")
        self.move(10,10)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = mainWindow()
    ex.show()
    sys.exit(app.exec_())