import openai
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

openai.api_key = config.get("OpenAI", "api_key")

def generate_response(prompt, max_tokens=4000):

    model_engine = "gpt-3.5-turbo"

    input_text = prompt

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": prompt}],
        temperature = 0
)
    # 从响应中提取生成的文本
    generated_text = response.choices[0].message.content
    return generated_text
