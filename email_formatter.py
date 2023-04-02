import re
from typing import List, Tuple
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

top_summaries = config.getint("MarkdownHandler", "top_summaries")

def extract_summary_data(summary: str) -> Tuple[str, str, int, str, str, int]:
    try:
        subject = re.search(r'邮件主题:\s*(.*?)\n', summary, re.DOTALL).group(1).strip()
    except AttributeError:
        subject = '数据缺失'

    try:
        sender = re.search(r'发件人:\s*(.*?)\n', summary, re.DOTALL).group(1).strip()
    except AttributeError:
        sender = '数据缺失'

    try:
        importance = int(re.search(r'重要度:\s*(\d)', summary).group(1))
    except AttributeError:
        importance = -1

    try:
        summary_text = re.search(r'内容概括:\s*(.*?)\n', summary, re.DOTALL).group(1).strip()
    except AttributeError:
        summary_text = '数据缺失'

    try:
        reply_suggestion = re.search(r'回复建议:\s*(.*?)\n', summary, re.DOTALL).group(1).strip()
    except AttributeError:
        reply_suggestion = '数据缺失'

    try:
        credibility = int(re.search(r'可信度:\s*(\d)', summary).group(1))
    except AttributeError:
        credibility = -1

    return subject, sender, importance, summary_text, reply_suggestion, credibility


def sort_summaries_by_importance(email_summaries: List[str]) -> List[str]:
    extracted_data = [extract_summary_data(summary) for summary in email_summaries]
    sorted_summaries = sorted(extracted_data, key=lambda x: x[2], reverse=True)
    return sorted_summaries[:top_summaries]

def generate_summary_email(sorted_summaries: List[Tuple[str, str, int, str, str, int]]) -> str:
    table_header = '''<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
                      <tr>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">邮件主题</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">发件人</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">重要度</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">内容概括</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">回复建议</th>
                        <th style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2;">可信度</th>
                      </tr>'''

    table_rows = ''
    for index, summary in enumerate(sorted_summaries):
        background_color = '#f2f2f2' if index % 2 == 0 else '#ffffff'
        table_rows += f'''<tr style="background-color: {background_color};">
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[0]}</td>
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[1]}</td>
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[2]}</td>
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[3]}</td>
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[4]}</td>
                           <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">{summary[5]}</td>
                         </tr>'''

    table_footer = '</table>'
    summary_email = table_header + table_rows + table_footer
    return summary_email



