#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/23 9:25
#!Author: Renjie Chen
#!Function: 关于作者的界面

from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QGridLayout, QDialog, QToolButton, QAction, QMenu
from PyQt5.QtGui import QMovie, QPixmap, QIcon
from PyQt5.QtCore import Qt

class aboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createGridLayout()
        self.setFixedSize(600, 450)
        self.setWindowTitle("关于作者")
        self.setWindowIcon(QIcon("icon/avatar.ico"))
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def createWidgets(self):
        self.introduce=QLabel("<p>学生党一枚，</p>"
                "<p>就读于<b>东川路男子职业技术学校</b>，</p>"
                "<p>初学<b>Python<b>，请多指教。</p>"
                "<p>交流学习可联系QQ：<i>3257575985</i>\n</p>"
                "<p><a href='https://github.com/crj1998'> <i>打开github</i></a></p>")
        self.introduce.setOpenExternalLinks(True)
        self.introduce.resize(100,300)
        self.gifpic=QLabel()
        self.gifpic.setScaledContents(True)
        self.gifpic.setFixedSize(280,350)
        self.movie=QMovie("icon/bili.gif")
        self.gifpic.setMovie(self.movie)
        self.movie.start()

        self.bt=QPushButton("打赏作者")
        self.bt.clicked.connect(self.reward)
        self.pix1=QPixmap("icon/alipay.loc")
        self.pix2=QPixmap("icon/wechatpay.loc")

        menu = QMenu(self)
        self.alipayAct = QAction(QIcon("icon/alipay.ico"), "支付宝打赏", self, triggered=self.topay)
        self.wechatAct = QAction(QIcon("icon/wechat.ico"), "微信打赏", self, triggered=self.topay)
        menu.addAction(self.alipayAct)
        menu.addAction(self.wechatAct)

        self.payway=QToolButton(self)
        self.payway.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.payway.setPopupMode(QToolButton.InstantPopup)
        self.payway.setText("打赏方式")
        self.payway.setIcon(QIcon("icon/bank.ico"))
        self.payway.setAutoRaise(True)
        self.payway.setEnabled(False)
        self.payway.setMenu(menu)

    def createGridLayout(self):
        grid=QGridLayout()
        grid.setSpacing(1)
        grid.addWidget(self.gifpic,1,1)
        grid.addWidget(self.introduce,1,2,1,2)
        grid.addWidget(self.bt, 2, 3)
        grid.addWidget(self.payway,2,1)
        grid.setAlignment(self.payway, Qt.AlignCenter)
        self.setLayout(grid)

    def reward(self):
        if self.bt.text()=="打赏作者":
            self.bt.setText("还是算了")
            self.movie.stop()
            self.gifpic.setPixmap(self.pix1)
            self.payway.setEnabled(True)
        else:
            self.bt.setText("打赏作者")
            self.gifpic.setMovie(self.movie)
            self.movie.start()
            self.payway.setEnabled(False)

    def topay(self):
        if self.sender() == self.alipayAct:
            self.gifpic.setPixmap(self.pix1)
        elif self.sender() == self.wechatAct:
            self.gifpic.setPixmap(self.pix2)



if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    interface=aboutDialog()
    interface.show()
    sys.exit(app.exec_())