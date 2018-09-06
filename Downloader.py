import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from myGUI import rootWindow
from PyQt5 import sip
def checkFile():
    rootpath=os.getcwd()
    files={"root":["config.ini","scrapy.cfg","cover.jpg"],"icon":['alipay.ico', 'alipay.loc', 'avatar.ico', 'bank.ico', 'bili.gif', 'download.ico', 'Error.ico', 'fastforward.ico', 'fastrewind.ico', 'feedback.ico', 'greyvip.png', 'help.ico', 'Info.ico', 'loading.gif', 'loadinga.gif', 'loadingb.gif', 'new.ico', 'open.ico', 'rand.ico', 'register.ico', 'skipnext.ico', 'skipprev.ico', 'thumbdown.ico', 'thumbup.ico', 'user.ico', 'Valid.ico', 'vip.ico', 'wechat.ico', 'wechatpay.loc'],"res":["0.data","1.data"]}
    for f in files["root"]:
        path=os.path.join(rootpath,f)
        if not os.path.exists(path):
            return False
    subpath=os.path.join(rootpath,"icon")
    for f in files["icon"]:
        path=os.path.join(subpath,f)
        if not os.path.exists(path):
            return False
    subpath=os.path.join(rootpath,"res")
    for f in files["res"]:
        path=os.path.join(subpath,f)
        if not os.path.exists(path):
            return False
    return True

if __name__ == '__main__':
    #for root, dirs, files in os.walk(os.getcwd()):
    try:
        app=QApplication(sys.argv)
        if not checkFile():
            QMessageBox.critical(None,"错误","缺少必须的资源文件\n请勿随意修改除Picture文件夹外的文件")
        else:
            blt=rootWindow()
            blt.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
    x=input()
