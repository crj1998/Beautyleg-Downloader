from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

def sEmail(theme='TEST',content='IGNORE ME',files=[]):
    sendAddr="2088737914@qq.com"
    password="oitecwcidermeiid"
    recipientAddr="3257575985@qq.com"
    msg=MIMEMultipart()
    msg["From"]=formataddr(["BltFeedback",sendAddr])
    msg["To"]=formataddr(['User',recipientAddr])
    msg["Subject"]=theme
    txt=MIMEText(content,"plain","utf-8")
    msg.attach(txt)
    if files!=[]:
        try:
            for f in files:
                part = MIMEApplication(open(f,"rb").read())
                part.add_header("Content-Disposition", "attachment", filename=f)
                msg.attach(part)
        except:
            pass
    try:
        smtp="smtp."+sendAddr.split("@")[-1]
        server=smtplib.SMTP_SSL(smtp,465)
        server.login(sendAddr,password)
        server.sendmail(sendAddr,[recipientAddr,],msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    if sEmail():
        print("邮件发送成功")
    else:
        print("邮件发送失败")