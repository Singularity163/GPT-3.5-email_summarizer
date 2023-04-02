import re
import html2text
from OpenAI_API import generate_response

def preprocess_email_body(body: str) -> str:
    # 将HTML内容转换为纯文本
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True
    plain_text = text_maker.handle(body)

    # 删除不是中文、英文、数字和常用标点的字符
    clean_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9,.，。？！“”‘’：:;；<>《》【】『』「」()（）]', '', plain_text)

    return clean_text
def process_email(subject, sender, body):
    prompt = create_prompt(subject, sender, body)
    gpt_response = generate_response(prompt)
    email_summary = truncate_prompt(gpt_response)
    return email_summary

def create_prompt(subject, sender, body):
    body = preprocess_email_body(body)
    body = truncate_prompt(body)

    prompt = f"""
    你是一名助理，请严格根据邮件主题，正文和发件人提供的信息，在模板中填写重要度 (1-10)，内容概括，回复建议和可信度 (1-10)。
    不要给促销邮件，优惠邮件，折扣邮件，广告邮件高重要度评分。
    如果邮件主题是英文，请翻译为中文，并在英文标题前用括号包含中文标题。
    请确保不要给出任何额外的响应、解释、说明或原因。严格按照给出的模板格式输出。

    邮件主题: {subject}
    正文: {body}
    发件人: {sender}
    
    模板：
    邮件主题: {{你需要在这里复述邮件主题}}
    正文: {{你需要在这里复述正文}}
    发件人: {{你需要在这里复述发件人}}
    重要度: {{你需要在这里输入重要度}}
    内容概括: {{你需要在这里输入内容概括}}
    回复建议: {{你需要在这里输入回复建议}}
    可信度: {{你需要在这里输入可信度}}
|
    """

    return prompt

def truncate_prompt(prompt, max_tokens=4000):
    if len(prompt) > max_tokens:
        prompt = prompt[:max_tokens]
    return prompt


