import email_processor
import email_module
from email_module import get_outlook_emails
from email_processor import process_email, create_prompt, truncate_prompt
import email_formatter
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# 获取配置文件中的值
username = config.get("General", "username")
password = config.get("General", "password")
to_email = config.get("General", "to_email")

def main():

    #读取邮件
    received_email = get_outlook_emails(username, password)

    email_summaries = []
    # 处理每封邮件，获取邮件摘要
    for email in received_email:
        subject = email['subject']
        sender = email['from']
        body = email['body']
        summary = process_email(subject, sender, body)
        email_summaries.append(summary)

    # 对评估结果根据重要度数值排序
    sorted_summaries = email_formatter.sort_summaries_by_importance(email_summaries)

    # 创建一个适合发送给用户的邮件格式
    summary_email = email_formatter.generate_summary_email(sorted_summaries)

    email_module.send_email_summary(username, password, to_email, summary_email)

if __name__ == "__main__":
    main()