#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/9/3 10:41
#!Author: Renjie Chen
#!Function:

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QBrush
from PyQt5.QtWidgets import QListWidget, QMenu, QAction, QAbstractItemView, QListWidgetItem
import csv


class listItem(QListWidgetItem):
    def __init__(self, line):
        super().__init__()
        self.year = line[0]
        self.no = line[1]
        self.model = line[2]
        self.pages = line[3]
        self.tag = line[4]
        self.date = line[5]
        self.style_init()

    def style_init(self):
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setText("No.%s %s [%sP] %s.%s" % (self.no, self.model, self.pages, self.year, self.date))

    def style_new(self):
        self.setForeground(QBrush(Qt.red))
        self.setToolTip('新发布')
        self.setIcon(QIcon('icon/new.ico'))

    def getName(self):
        return "No.%s %s [%sP] %s.%s" % (self.no, self.model, self.pages, self.year, self.date)

    def writecsv(self):
        with open('res/0.data', 'a', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile, delimiter='-')
            writer.writerow([self.year, self.no, self.model, self.pages, self.tag, self.date])


class ListWidget(QListWidget):
    addGroupSignal = pyqtSignal(str)
    delGroupSignal = pyqtSignal(str)

    def __init__(self,newlist=[]):
        super().__init__()
        self.new = newlist
        self.map_list = [{'groupname': "BeautyLeg", 'datasource': '1'}, {'groupname': "我的收藏", 'datasource': '0'}]
        self.current = '1'
        self.Dataload()
        self.Ui_init()

    def Dataload(self, name='BeautyLeg'):
        self.clear()
        filename = "res/%s.data" % self.nametono(name)
        with open(filename, 'r', encoding='utf-8') as csvFile:
            lines = csv.reader(csvFile, delimiter='-')
            lines = [l for l in lines]
            lines.reverse()
            for line in lines:
                newitem = listItem(line)
                if newitem.no in self.new:
                    newitem.style_new()
                self.addItem(newitem)

    def Ui_init(self):
        self.setCurrentRow(0)
        self.setIconSize(QSize(20, 30))
        self.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                           "QListWidget::Item{padding-top:2px; padding-bottom:2px; }"
                           "QListWidget::Item:hover{background:skyblue; }")
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def nametono(self, name):
        if name == 'BeautyLeg':
            return '1'
        elif name == '我的收藏':
            return '0'
        else:
            return None

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            menu = QMenu(self)
            colAct = QAction("收藏", menu)
            delAct = QAction('删除', menu)
            if self.current == '1':
                delAct.setEnabled(False)
            if self.current == '0' or len(self.selectedItems()) > 1:
                colAct.setEnabled(False)
            colAct.triggered.connect(self.colItem)
            delAct.triggered.connect(self.delItem)
            menu.addAction(colAct)
            menu.addAction(delAct)
            menu.popup(self.mapToGlobal(event.pos()))

    def colItem(self):
        item = self.selectedItems()[0]
        with open('res/0.data', 'r', newline='', encoding='utf-8') as csvFile:
            lines = csv.reader(csvFile, delimiter='-')
            for l in lines:
                if l[1] == item.no:
                    return
        item.writecsv()

    def delItem(self):
        dellist = self.selectedItems()
        dl = []
        for delitem in dellist:
            dl.append(delitem.no)
            del_item = self.takeItem(self.row(delitem))
            del del_item
        with open('res/0.data', 'r', newline='', encoding='utf-8') as csvFile:
            lines = [i for i in csv.reader(csvFile, delimiter='-')]
        with open('res/0.data', 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile, delimiter='-')
            for line in lines:
                if line[1] not in dl:
                    writer.writerow(line)