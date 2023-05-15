import openai

# OpenAI API 키 설정
openai.api_key = 'YOUR_API_KEY'

def interact_with_chat_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,  # 적절한 길이로 조정할 수 있습니다.
        temperature=0.7,  # 다양한 응답을 얻기 위해 조정할 수 있습니다.
        n=1,  # 생성할 응답의 개수를 지정합니다.
        stop=None,  # 대화를 정지할 텍스트를 지정합니다.
        timeout=15,  # 요청이 만료되기 전에 응답을 얻기 위한 시간 제한입니다.
    )

    if response.choices:
        return response.choices[0].text.strip()
    else:
        return "ChatGPT와의 상호 작용에 문제가 발생했습니다."

# ChatGPT와 상호 작용하는 예시
while True:
    user_input = input("사용자: ")

    if user_input.lower() == 'quit':
        break

    prompt = "사용자: " + user_input + "\nAI:"

    ai_response = interact_with_chat_gpt(prompt)
    print("AI:", ai_response)
