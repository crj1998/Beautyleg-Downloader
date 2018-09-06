#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:58
#!Author: Renjie Chen
#!Function: 主界面

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QComboBox, QPushButton, QProgressBar
from MyListWidget import ListWidget
from multiprocessing import Process
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import requests
import time
import os

from beautylegcore import Update

class mainWindow(QWidget):
    statusbarSignal = pyqtSignal(str)
    def __init__(self,isvip=0):
        super().__init__()
        self.vip=isvip
        self.page = 0
        self.sharpness = False
        self.nowlist = []
        self.savedpages= 0
        self.createItems()
        self.createGridLayout()
        self.setFixedSize(1000,850)
        self.setWindowTitle('main')

    def createItems(self):
        pixmap = QPixmap("cover.jpg")
        self.preview = QLabel(self)
        self.preview.setFixedSize(430, 646)
        self.preview.setPixmap(pixmap)
        self.preview.setScaledContents(True)

        self.info = QLabel("Picture Information!")
        self.info.setAlignment(Qt.AlignCenter)

        self.nextpic = QPushButton(icon=QIcon('icon/skipnext.ico'))
        self.nextpack = QPushButton(icon=QIcon('icon/fastforward.ico'))
        self.prevpic = QPushButton(icon=QIcon('icon/skipprev.ico'))
        self.prevpack = QPushButton(icon=QIcon('icon/fastrewind.ico'))
        self.thumbup = QPushButton(icon=QIcon('icon/thumbup.ico'))
        self.thumbdown = QPushButton(icon=QIcon('icon/thumbdown.ico'))
        self.download = QPushButton("下载",self)
        self.TSHD = QPushButton("TS",self)
        self.TSHD.setCheckable(True)
        self.nextpack.setFixedSize(50, 35)
        self.prevpack.setFixedSize(50, 35)
        self.nextpic.setFixedSize(60, 35)
        self.prevpic.setFixedSize(60, 35)
        self.thumbup.setFixedSize(60, 35)
        self.thumbdown.setFixedSize(60, 35)
        self.nextpic.setEnabled(False)
        self.prevpic.setEnabled(False)

        self.nextpack.clicked.connect(self.nextpackage)
        self.prevpack.clicked.connect(self.prevpackage)
        self.nextpic.clicked.connect(self.picchange)
        self.prevpic.clicked.connect(self.picchange)
        self.download.clicked.connect(self.downloadAct)
        if self.vip==1:
            self.TSHD.toggled[bool].connect(self.changesharpness)
        else:
            self.TSHD.setEnabled(False)

        update = Update()
        newlist=update.newnolist
        self.listwidget = ListWidget(newlist)
        self.listwidget.itemSelectionChanged.connect(self.vipdownload)
        self.listwidget.itemDoubleClicked.connect(self.do)

        font = QFont()
        font.setPointSize(15)
        self.combo = QComboBox(self)
        for i in self.listwidget.map_list:
            self.combo.addItem(i['groupname'])
        self.combo.setFont(font)
        self.combo.activated[str].connect(self.onActivated)

        self.listwidget.addGroupSignal[str].connect(self._add)
        self.listwidget.delGroupSignal[str].connect(self._del)

        self.progressbar=QProgressBar(self)
        self.progressbar.setMinimum(0)
        self.progressbar.setOrientation(Qt.Horizontal)
        self.progressbar.setFormat("%p%")

        self.time_1s=QTimer(self)
        self.time_1s.setInterval(1000)
        self.time_1s.timeout.connect(self.checkProcess)

    def createGridLayout(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.prevpack, 1, 1, 1, 1)
        grid.addWidget(self.info, 1, 2, 1, 4)
        grid.addWidget(self.nextpack, 1, 6, 1, 1)
        grid.addWidget(self.preview, 2, 1, 7, 6)
        grid.addWidget(self.prevpic, 9, 2, 1, 1)
        grid.addWidget(self.thumbdown, 9, 3, 1, 1)
        grid.addWidget(self.TSHD, 9, 4, 1, 1)
        grid.addWidget(self.thumbup, 9, 5, 1, 1)
        grid.addWidget(self.nextpic, 9, 6, 1, 1)
        grid.addWidget(self.combo, 1, 7, 1, 1)
        grid.addWidget(self.listwidget, 2, 7, 7, 1)
        grid.addWidget(self.download,9,7,1,1)
        grid.addWidget(self.progressbar,10,1,1,7)
        self.setLayout(grid)

    def onActivated(self, text):
        groupname = self.combo.currentText()
        self.listwidget.Dataload(groupname)
        self.listwidget.current = self.listwidget.nametono(groupname)
        self.listwidget.setCurrentRow(0)

    def _add(self, groupname):
        self.combo.addItem(groupname)

    def _del(self, groupname):
        index = self.combo.findText(groupname)
        self.combo.removeItem(index)

    def vipdownload(self):
        if self.vip==0 and len(self.listwidget.selectedItems())>1:
            self.download.setEnabled(False)
            self.download.setToolTip("你不是VIP，暂时不能多个图包同时下载")
            self.statusbarSignal.emit("你不是VIP，暂时不能多个图包同时下载。开通VIP享受更多功能")
        else:
            self.download.setEnabled(True)

    def nextpackage(self):
        row = self.listwidget.currentRow()
        if row == self.listwidget.count() - 1:
            self.listwidget.setCurrentRow(0)
        else:
            self.listwidget.setCurrentRow(row + 1)
        item = self.listwidget.currentItem()
        self.page=0
        self.loadWebPic(item,self.page,self.sharpness)

    def prevpackage(self):
        row = self.listwidget.currentRow()
        if row == 0:
            self.listwidget.setCurrentRow(self.listwidget.count() - 1)
        else:
            self.listwidget.setCurrentRow(row - 1)
        self.page=0
        self.loadWebPic(item,self.page,self.sharpness)

    def picchange(self):
        sender=self.sender()
        if sender==self.prevpic:
            if self.page == 0:
                self.page = (self.vip+1)*5
            else:
                self.page -= 1
        else:
            if self.page == (self.vip+1)*5:
                self.page = 0
            else:
                self.page += 1
        item = self.listwidget.currentItem()
        self.loadWebPic(item, self.page, self.sharpness)

    def loadWebPic(self, item, page=0,high = False):
        if high:
            p = {"src": "/photo/beautyleg/%s/%s/beautyleg-%s-%s.jpg" % (item.year, item.no, item.no, str(page).zfill(4)), "h": "646",
                      "w": "430", "zc": "1", "q": "100"}
        else:
            p = {"src": "/photo/beautyleg/%s/%s/beautyleg-%s-%s.jpg" % (item.year, item.no, item.no ,str(page).zfill(4)), "h": "323",
                      "w": "215", "zc": "1", "q": "100"}
        url = "http://www.beautylegmm.com/usr/themes/mm/timthumb.php"
        r = requests.get(url, params=p, timeout=5)
        cover = QPixmap()
        cover.loadFromData(r.content,"JPG")
        self.preview.setPixmap(cover)
        self.setEnabled(True)

    def do(self):
        currentitem = self.listwidget.currentItem()
        if currentitem:
            text = currentitem.text()
            self.info.setText(text)
            self.loadWebPic(currentitem,0,self.sharpness)
        self.nextpic.setEnabled(True)
        self.prevpic.setEnabled(True)

    def changesharpness(self,HD):
        if HD:
            self.TSHD.setText("HD")
            self.sharpness=True
        else:
            self.TSHD.setText("TS")
            self.sharpness=False

    def downloadAct(self):
        if self.download.text()=="下载":
            self.download.setText("取消")
            self.nowlist=[]
            allpages=0
            nolist=[]
            for item in self.listwidget.selectedItems():
                allpages+=int(item.pages)
                nolist.append(item.no)
                self.nowlist.append(item)
            self.progressbar.setMaximum(allpages)
            args = ['scrapy','crawl','Beautyleg','-a','indexlist=%s'%(",".join(nolist))]
            self.time_1s.start()
            self.p = Process(target=execute, args=(args,))
            self.p.start()
        else:
            self.time_1s.stop()
            self.p.terminate()
            self.p.join()
            self.download.setText("下载")

    def checkProcess(self):
        allpages=0
        path=os.path.abspath(os.getcwd())
        path=os.path.join(path,"Picture")
        for item in self.nowlist:
            pic_path=os.path.join(path,"No.%s %s"%(item.no,item.model))
            try:
                l=len(os.listdir(pic_path))
                if l==int(item.pages):
                    self.nowlist.pop(self.nowlist.index(item))
                    self.savedpages+=l
                    self.statusbarSignal.emit("No.%s %s 已下载!"%(item.no,item.model))
                else:
                    allpages+=l
            except FileNotFoundError:
                pass
        self.progressbar.setValue(self.savedpages+allpages)
        if not self.p.is_alive():
            self.statusbarSignal.emit("下载结束")
            self.savedpages=0
            self.time_1s.stop()
            self.download.setText("下载")
        else:
            self.statusbarSignal.emit("下载中...")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = mainWindow(1)
    ex.show()
    sys.exit(app.exec_())
