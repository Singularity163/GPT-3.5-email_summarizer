import time
import imapclient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from email import message_from_bytes
import base64
from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# 获取配置文件中的值
username = config.get("General", "username")
password = config.get("General", "password")
to_email = config.get("General", "to_email")
imap_server = config.get("Outlook", "imap_server")
imap_port = config.getint("Outlook", "imap_port")
smtp_server = config.get("Outlook", "smtp_server")
smtp_port = config.getint("Outlook", "smtp_port")
email_limit = config.getint("Emails", "email_limit")


def get_text_email_body(msg):
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            return part.get_payload()
        elif part.get_content_type() == "text/html":
            try:
                soup = BeautifulSoup(part.get_payload(), 'html.parser')
                return soup.get_text()
            except:
                return ""
    return ""


def get_outlook_emails(username, password, limit = email_limit):
    with imapclient.IMAPClient(imap_server, port=imap_port, ssl=True) as client:
        client.login(username, password)
        client.select_folder("INBOX")

        messages = client.search(["ALL"])
        messages = messages[-limit:]

        email_data = []
        for msg_id in messages:
            msg_data = client.fetch(msg_id, ["ENVELOPE", "BODY[]"])
            envelope = msg_data[msg_id][b"ENVELOPE"]
            body = msg_data[msg_id][b"BODY[]"].decode("utf-8")

            msg = message_from_bytes(msg_data[msg_id][b"BODY[]"])
            body = get_text_email_body(msg)

            email_data.append({
                "subject": envelope.subject.decode(),
                "from": envelope.from_[0].mailbox.decode() + "@" + envelope.from_[0].host.decode(),
                "date": envelope.date,
                "body": body
            })

        return email_data


def send_email_summary(username, password, to_email, email_summary):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = to_email
        msg["Subject"] = "您的邮件总结 (Email Summary)"

        msg.attach(MIMEText(email_summary, "html"))  # 将 "plain" 更改为 "html"

        server.sendmail(username, to_email, msg.as_string())