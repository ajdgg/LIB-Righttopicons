from dotenv import load_dotenv
from log import XJ_Log
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


XJ_Log = XJ_Log()

load_dotenv('.env.bot')


EMAIL = os.getenv('EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
AC = os.getenv('AC')
SMTP_PORT = os.getenv('SMTP_PORT')
SYSOP_EMAIL = os.getenv('SYSOP_EMAIL')


def self_inspection():
    required_vars = ['EMAIL', 'SMTP_SERVER', 'AC', 'SMTP_PORT', 'SYSOP_EMAIL']
    for var in required_vars:
        if os.getenv(var) is None:
            print(f"缺少环境变量: {var}")
            XJ_Log.w_log(f"缺少环境变量: {var}", 'error')
            return False
    return True


def mail(data):
    sender_email = EMAIL
    password = AC
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = SYSOP_EMAIL
    message["Subject"] = "运行报告"
    message.attach(MIMEText(data, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, SYSOP_EMAIL, message.as_string())
    except Exception as e:
        print(f"邮件发送失败: {e}")
        XJ_Log.w_log(f"邮件发送失败: {e}", 'error')


def f_email(data):
    if self_inspection():
        mail(data)
        return True
    else:
        return False
