# 基于GPT-3.5的邮件摘要生成器 (GPT-3.5-email_summarizer)

GPT-3.5-email_summarizer会对指定数量的邮件进行读取并分析，使用GPT-3.5分析邮件并返回总结邮件，使用Python实现。该项目利用了GPT-3.5-turbo (OpenAI) API，以及自定义的排序和筛选规则来生成邮件摘要。

## 功能

- 通过Outlook API读取用户收到的邮件
- 提取邮件的主题、正文和发件人信息
- 利用GPT-3.5生成邮件摘要
- 根据重要度和可信度对邮件摘要进行排序
- 生成HTML表格格式的邮件摘要报告
- 将邮件摘要报告发送给用户

## 安装与配置

确保您已安装以下依赖：

- Python 3.x
- [openai](https://github.com/openai/openai) (安装：`pip install openai`)
- [requests](https://docs.python-requests.org/en/master/) (安装：`pip install requests`)
- configparser
- re
- html2text
- imapclient
- smtplib
- bs4

在开始使用之前，请确保已获取OpenAI API的访问密钥。请修改文件中的config.ini，填入自己的用户名和密码，以及openAI key。
默认发送和接收邮箱为Outlook。可以通过修改imap和smtp来切换成不同的邮箱。请确保在邮箱设置里允许使用imap和smtp。
默认的设置将会读取最新的十五封邮件，并发送重要度前十的邮件给用户。您可以修改config里的参数来改变读取和发送的邮件数量。

## 使用方法

1. 配置好所有依赖和API密钥后，在项目根目录下运行`main.py`文件：
2. 程序将自动读取用户收到的邮件，并生成邮件摘要报告。
3. 报告将以HTML表格的形式发送至用户的邮箱。

## 许可

本项目采用[MIT许可证](LICENSE)。
