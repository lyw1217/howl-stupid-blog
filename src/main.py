from app import *

from threading import Thread
import time
import random
import datetime

def print_initlog():
    root_logger.critical(r"██   ██  ██████  ██     ██ ██                ")
    root_logger.critical(r"██   ██ ██    ██ ██     ██ ██                ")
    root_logger.critical(r"███████ ██    ██ ██  █  ██ ██                ")
    root_logger.critical(r"██   ██ ██    ██ ██ ███ ██ ██                ")
    root_logger.critical(r"██   ██  ██████   ███ ███  ███████           ")
    root_logger.critical(r"                                             ")
    root_logger.critical(r"                                             ")
    root_logger.critical(r"███████ ████████ ██    ██ ██████  ██ ██████  ")
    root_logger.critical(r"██         ██    ██    ██ ██   ██ ██ ██   ██ ")
    root_logger.critical(r"███████    ██    ██    ██ ██████  ██ ██   ██ ")
    root_logger.critical(r"     ██    ██    ██    ██ ██      ██ ██   ██ ")
    root_logger.critical(r"███████    ██     ██████  ██      ██ ██████  ")
    root_logger.critical(r"                                             ")
    root_logger.critical(r"                                             ")
    root_logger.critical(r"██████  ██       ██████   ██████             ")
    root_logger.critical(r"██   ██ ██      ██    ██ ██                  ")
    root_logger.critical(r"██████  ██      ██    ██ ██   ███            ")
    root_logger.critical(r"██   ██ ██      ██    ██ ██    ██            ")
    root_logger.critical(r"██████  ███████  ██████   ██████             ")
    root_logger.critical(r"                                by YOUNGWOO  ")
    root_logger.critical(f"  ROOT DIR     = {ROOT_DIR}")
    root_logger.critical(f"  BASE DIR     = {BASE_DIR}")
    root_logger.critical(f"  CONFIG  PATH = {CONFIG_PATH}")
    root_logger.critical(f"  LOG CFG PATH = {LOG_CFG_PATH}")
    root_logger.critical(f"  LOGGING PATH = {LOGGING_PATH}")
    root_logger.critical(f"")
    root_logger.critical(f"  INTERVAL     = {INTERVAL} min")
    root_logger.critical(r"======================================")

'''
쓰레드
'''
def th_subject_upload():
    root_logger.critical(f"subject upload thread 시작, interval = {INTERVAL}")
    while True:
        if SYS_PLATFORM == 'Windows':
            SUBJECT_PATH = os.path.join(ROOT_DIR, 'config\subject.json')
        else:
            SUBJECT_PATH = os.path.join(ROOT_DIR, 'config/subject.json')
        if os.path.isfile(SUBJECT_PATH):
            with open(SUBJECT_PATH) as json_file:
                subjects = json.load(json_file)
        else :
            root_logger.critical("subject.json 파일 읽기 실패")
            return None
        
        if len(subjects['subjects']) > 0 :
            s = subjects['subjects'][0]
            
            del subjects['subjects'][0]
            with open(SUBJECT_PATH, 'w') as json_file:
                json.dump(subjects, json_file, ensure_ascii=False)

            if len(s) > 0:
                post_process(s)
        
        next_interval = INTERVAL * random.randint(40, 60)

        root_logger.critical(f"남은 subject 개수    : {len(subjects['subjects'])}")
        root_logger.critical(f"다음 포스팅 예상 시간 : {datetime.datetime.now() + datetime.timedelta(seconds=next_interval)}")

        # 주기가 너무 일정하지 않게끔
        time.sleep(next_interval)

'''
일말의 양심
'''
def conscience(content, flag):
    if flag :
        return f"{content} \n\n\n\n 이 글은 ChatGPT, DALL-E, Karlo API를 이용하여 자동으로 작성된 글입니다."
    else :
        return f"{content} \n\n\n\n This post was automatically generated using the ChatGPT, DALL-E, and Karlo APIs."


'''
포스트 업로드를 위한 메인 프로세스
'''
def post_process(input_value) :
    root_logger.critical(f"{input_value}에 대한 글 작성 시작...")
    
    post_subject = input_value
    
    # 주제에 맞는 컨텐츠 생성
    prompt = f"'{post_subject}'에 대한 주제의 블로그 글, 자세하게, markdown"
    response = generate_text(prompt, max_token=MAX_TOKEN)
    root_logger.critical(response)

    # 영어로 번역
    en_contents = translate_to_en(response)

    # 이미지를 위한 프롬프트 생성
    prompt = make_prompt_for_image(post_subject)
    
    # 생성한 프롬프트로 이미지 생성
    img_path = make_image_karlo(post_subject, prompt)
    
    # 티스토리 이미지 삽입을 위해 이미지 업로드, replacer 컨텐츠 하단에 추가
    replacer = upload_to_tistory(img_path)
    en_contents = insert_tistory_image_into_markdown(en_contents, replacer)
    kr_contents = insert_tistory_image_into_markdown(response, replacer)

    # 일말의 양심 추가
    kr_contents = conscience(kr_contents, True)
    en_contents = conscience(en_contents, False)

    # 포스팅 제목 생성
    kr_post_subject = f"{post_subject}"
    en_post_subject = f"{translate_to_en(post_subject)}"

    # 마크다운 파일로 떨구기
    kr_post_path = drop_to_markdown(kr_post_subject, kr_contents)
    en_post_path = drop_to_markdown(en_post_subject, en_contents)

    # 티스토리에 업로드
    post_to_tistory(kr_post_subject, kr_post_path)
    
    # 약 1~5분 뒤 영어 포스팅 업로드
    time.sleep(random.randint(60, 300))
    
    post_to_tistory(en_post_subject, en_post_path)

if __name__ == "__main__":

    print_initlog()

    t = Thread(target=th_subject_upload)
    t.start()

    flask_app.run(debug=True, port=8080)