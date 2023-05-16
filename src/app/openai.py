from app.config import *
import openai

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

model = GPT_MODEL

def generate_text(prompt, max_token=100):
    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You're trying to write a post for your blog."},
            {"role": "user", "content": prompt}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    root_logger.critical(answer)
    
    return f"{answer}"

def drop_to_markdown(title, content):
    if SYS_PLATFORM == 'Windows':
        path = os.path.join(ROOT_DIR, f"posts\{title}.md")
    else :
        path = os.path.join(ROOT_DIR, f"posts/{title}.md")

    with open(path, 'w') as f:
        f.write(content)

    root_logger.critical(f"drop to markdown > path : {path}")

    return path