#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:59
#!Author: Renjie Chen
#!Function: 基础界面框架

import sys
import os
from binascii import hexlify
from PyQt5.QtCore import Qt,QSettings
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction, qApp, QInputDialog, QFileDialog, QMenu, QActionGroup, QLabel
import webbrowser
from feedback import feedbackDialog
from aboutme import aboutDialog
from mainwindow import mainWindow


def viptest(p):
    if len(p)!=20:return False
    pubKey="010001"
    modulus="00e0b509f6259df8"
    text=p[:5]
    text=text[::-1].encode()
    rsa=int(hexlify(text),16)**int(pubKey,16)%int(modulus,16)
    return format(rsa,'x').zfill(15)==p[5:]

class rootWindow(QMainWindow):
    #windowList=[]
    def __init__(self):
        super().__init__()
        self.createSettings()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.setGeometry(100,100,1000,900)
        self.setWindowTitle('APP')
        self.setWindowIcon(QIcon('icon/download.ico'))
        self.mainwindow=mainWindow()
        self.mainwindow.statusbarSignal[str].connect(self.createStatusBar)
        self.setCentralWidget(self.mainwindow)

    def createSettings(self):
        self.setting=QSettings('MySoft','Beautyleg Downloader')
        self.isvip=self.setting.value('isVip',0)

    def createActions(self):
        self.openAct=QAction(QIcon('icon/open.ico'),'打开...',self,shortcut="Ctrl+O",triggered=self.openfile,statusTip='打开文件')
        self.exitAct=QAction("退出",self,shortcut="Ctrl+Q",triggered=self.close)
        self.debug=QAction('开发者模式',self,statusTip='本功能为开发者调试功能，用户请勿使用！',checkable=True,enabled=False)
        self.user=QAction('用户模式',self,statusTip='目前为用户模式！',checkable=True)
        self.activation=QAction(QIcon('icon/greyvip.png'),'激活VIP',self,shortcut="Ctrl+V",triggered=self.showDialog_VIP,statusTip='激活VIP功能')
        self.aboutappAct = QAction("关于应用",self,triggered=self.aboutapp)
        self.aboutmeAct = QAction("关于作者", self, triggered=self.aboutme)
        self.aboutQtAct = QAction("关于Qt", self, triggered=QApplication.instance().aboutQt)
        self.feedbackAct = QAction(QIcon('icon/feedback.ico'), '反馈', self, triggered=self.feedback)

        self.alignmentGroup = QActionGroup(self)
        self.alignmentGroup.addAction(self.user)
        self.alignmentGroup.addAction(self.debug)
        self.user.setChecked(True)

        if self.isvip==1:
            self.activation.setIcon(QIcon("icon/vip.ico"))
            self.activation.blockSignals(True)
            self.activation.setStatusTip('VIP已激活')
            self.activation.setToolTip("VIP用户：\n    — 快速下载\n    — 并发下载\n    — 丝足便当")


    def createMenus(self):
        modemenu = QMenu('模式切换',self)
        modemenu.addAction(self.user)
        modemenu.addAction((self.debug))

        settingMenu = self.menuBar().addMenu('设置(&S)')
        settingMenu.addMenu(modemenu)

        feedbackMenu = self.menuBar().addMenu('反馈(&B)')
        feedbackMenu.addAction(self.feedbackAct)

        aboutMenu=self.menuBar().addMenu("关于(&A)")
        aboutMenu.addAction(self.aboutappAct)
        aboutMenu.addAction(self.aboutmeAct)
        aboutMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(settingMenu)
        self.menuBar().addMenu(feedbackMenu)
        self.menuBar().addMenu(aboutMenu)

    def createToolBars(self):
        self.toolbar=self.addToolBar('Activate')
        self.toolbar.addAction(self.activation)

    def createStatusBar(self,words='待命中'):
        self.statusBar().showMessage(words)

    def openfile(self):
        fname=QFileDialog.getOpenFileName(self,'Open file',os.getcwd())


    def showDialog_VIP(self):
        webbrowser.open("https://www.fageka.com/sell/Xx0yDHM4301")
        text,ok=QInputDialog.getText(self,'激活VIP',"输入激活码:")
        if ok:
            if viptest(text):
                self.activation.setIcon(QIcon("icon/vip.ico"))
                self.activation.blockSignals(True)
                self.setting.setValue('isVip',1)
                self.activation.setStatusTip('VIP已激活')
                self.activation.setToolTip("VIP用户：\n    — 快速下载\n    — 并发下载\n    — 丝足便当")
            else:
                self.createStatusBar("激活失败")

    def aboutapp(self):
        QMessageBox.about(self, "About Beautyleg Downloader","<p>应用 <b>Beautyleg Downloader</b> 可以用于下载 <style>a:link {text-decoration: none;}a:visited {text-decoration: none;}a:active {text-decoration: none;}a:hover {text-decoration: none;}</style><a href='http://www.beautyleg.com'> <b>Beautyleg</b></a> 套图，支持在线预览，图包下载，VIP用户可以多图包快速下载。</p>" 
                          "<p>本应用仅作为交流学习使用，请勿用于商业用途，否则后果自负。</p>" 
                          "<p>图片版权所有- Copyright© BEAUTYLEG , All Rights Reserved</p>"
                          "<p>当前版本 V0.2 Beta <style>a:link {text-decoration: none;}a:visited {text-decoration: none;}a:active {text-decoration: none;}a:hover {text-decoration: none;}</style><a href='https://rb16719799.icoc.bz/'> <b>了解更新</b></a> </p>")

    def aboutme(self):
        abm=aboutDialog()
        r=abm.exec_()

    def feedback(self):
        fbd=feedbackDialog()
        r=fbd.exec_()

    #右键菜单
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        refreshAct = cmenu.addAction("刷新")
        quitAct = cmenu.addAction("退出")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    entry=rootWindow()
    entry.show()
    sys.exit(app.exec_())




