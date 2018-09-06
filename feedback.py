#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:57
#!Author: Renjie Chen
#!Function: 反馈界面

from PyQt5.QtWidgets import QPushButton,QApplication,QTextEdit,QLabel,QLineEdit,QGridLayout,QComboBox,QMessageBox,QDialog, QCompleter
from PyQt5.QtGui import QStandardItemModel, QRegExpValidator, QIcon
from PyQt5.QtCore import QRegExp, Qt
from sendEmail import sEmail

class feedbackDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createGridLayout()
        self.setGeometry(300,300,450,500)
        self.setWindowIcon(QIcon("icon/feedback.ico"))
        self.setWindowTitle("用户反馈")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
    def emailSubmit(self):
        if "@" not in self.contactEdit.text():
            QMessageBox.information(self,"注意","<p>联系邮箱为空或者不合法。</p><p>请重新填写。</p>")
        elif self.contentEdit.toPlainText()=="":
            QMessageBox.information(self,"注意","<p>具体内容为空。</p><p>请重新填写。</p>")
        elif sEmail(self.combo.currentText(),self.contactEdit.text()+'\n'+self.contentEdit.toPlainText(),["config.ini"]):
            self.successMessage()
        else:
            self.failureMessage()
    def createWidgets(self):
        self.title=QLabel("反馈类型：")
        self.contact=QLabel("邮箱地址：")
        self.content=QLabel("具体内容：")
        self.combo=QComboBox()
        self.combo.addItem("意见反馈")
        self.combo.addItem("问题反馈")
        self.combo.addItem("联系作者")
        self.contactEdit=QLineEdit()
        self.contactEdit.setPlaceholderText("请输入您的联系邮箱")
        self.contentEdit=QTextEdit()
        self.contentEdit.setPlaceholderText("具体描述需要反馈的内容")
        self.submit=QPushButton("提交")
        self.submit.clicked.connect(self.emailSubmit)

        self.model = QStandardItemModel(0, 1, self)
        completer = QCompleter(self.model, self)
        self.contactEdit.setCompleter(completer)
        completer.activated[str].connect(self.contactEdit.setText)
        self.contactEdit.textEdited[str].connect(self.autocomplete)

        regx = QRegExp("^[0-9A-Za-z_.-]{3,16}@[0-9A-Za-z-]{1,10}(\.[a-zA-Z0-9-]{0,10}){0,2}\.[a-zA-Z0-9]{2,6}$")
        validator = QRegExpValidator(regx, self.contactEdit)
        self.contactEdit.setValidator(validator)

    def createGridLayout(self):
        grid=QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.title,1,0)
        grid.addWidget(self.combo,1,1)
        grid.addWidget(self.contact,2,0)
        grid.addWidget(self.contactEdit,2,1)
        grid.addWidget(self.content,3,0)
        grid.addWidget(self.contentEdit,3,1,5,1)
        grid.addWidget(self.submit,9,0,1,2)
        self.setLayout(grid)

    def successMessage(self):
        MESSAGE="<p>你的反馈我们已经收到，我们会尽快给您回馈，感谢您的支持。</p><p>点击OK退出反馈界面。</p>"
        success=QMessageBox.information(self,"反馈成功",MESSAGE)
        self.close()

    def failureMessage(self):
        MESSAGE="<p>由于某些原因，您没有反馈成功。<p>是否重新尝试一次？"
        failure=QMessageBox(QMessageBox.Warning,"反馈失败",MESSAGE,QMessageBox.NoButton,self)
        failure.addButton("是",QMessageBox.AcceptRole)
        failure.addButton("否",QMessageBox.RejectRole)
        if failure.exec_()==QMessageBox.AcceptRole:
            pass
        else:
            self.close()

    def autocomplete(self, text):
        if "@" in self.contactEdit.text():
            return
        emaillist = ["@live.com", "@139.com", "@126.com", "@163.com", "@gmail.com", "@qq.com"]
        self.model.removeRows(0, self.model.rowCount())
        for i in range(0, len(emaillist)):
            self.model.insertRow(0)
            self.model.setData(self.model.index(0, 0), text + emaillist[i])


if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    interface=feedbackDialog()
    interface.show()
    sys.exit(app.exec_())