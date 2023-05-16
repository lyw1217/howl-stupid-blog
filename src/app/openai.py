from app.config import *
import openai
import requests
from PIL import Image
from io import BytesIO

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

model = GPT_MODEL

'''
chatgpt에게 질문하는 함수
'''
def generate_text(prompt, max_token=200):
    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant who excels at blogging posts."},
            {"role": "user", "content": prompt}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        #max_tokens=max_token,
        n=1,
        #temperature=0.7
    )
    answer = response['choices'][0]['message']['content']
    root_logger.critical(answer)
    
    return f"{answer}"

'''
메시지를 영어로 번역시키는 함수
'''
def translate_to_en(prompt, max_token=200):
    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant who excels at blogging posts."},
            {"role": "user", "content": f"Translate to English. {prompt}"}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        #max_tokens=max_token,
        n=1,
        #temperature=0.7
    )
    answer = response['choices'][0]['message']['content']
    root_logger.critical(answer)
    
    return f"{answer}"

'''
제목, 내용을 입력받아 .md 파일로 떨구는 함수
'''
def drop_to_markdown(title, content):
    if SYS_PLATFORM == 'Windows':
        path = os.path.join(ROOT_DIR, f"posts\{title}.md")
    else :
        path = os.path.join(ROOT_DIR, f"posts/{title}.md")

    with open(path, 'w') as f:
        f.write(content)

    root_logger.critical(f"drop to markdown > path : {path}")

    return path

'''
주제를 입력받아 이미지 생성을 위한 프롬프트 작성을 요청하는 함수
https://wooiljeong.github.io/python/chatgpt-api/
'''
def make_prompt_for_image(subject, max_token=200):
    query = f"'{subject}'는 어떤 모습일지 외형적인 모습을 자유롭게 상상해서 자세히 영어로 묘사해주세요."
    # 새 메시지 구성
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who is good at detailing."
        },
        {
            "role": "user",
            "content": query
        }
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    answer = response['choices'][0]['message']['content']
    root_logger.critical(f"외형 묘사 = {answer}")


    # 새 메시지 구성
    messages = [
        {"role": "system", "content": "You are an assistant who is good at creating prompts for image creation." },
        {"role": "assistant", "content": answer }
    ]

    # 사용자 메시지 추가
    messages.append(
        {"role": "user", "content": "Condense up to 4 outward description to focus on nouns and adjectives separated by ','" }
    )

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    prompt = f"{response['choices'][0]['message']['content']}, realistic lighting, ultra-detailed, 8K, photorealism"
    root_logger.critical(f"이미지 프롬프트 = {prompt}")
        
    return prompt

def make_image_dall_e(subject, prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    res = requests.get(image_url)
    img = Image.open(BytesIO(res.content))

    if SYS_PLATFORM == 'Windows':
        path = os.path.join(ROOT_DIR, f"img\{subject}.png")
    else :
        path = os.path.join(ROOT_DIR, f"img/{subject}.png")
        
    img.save(path)

    root_logger.critical(f"dall-e 이미지 저장 성공, path = {path}")

    return path