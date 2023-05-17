from flask import Flask, render_template, request
from app import *

import threading
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

'''
@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        input_value = request.form['myInput']

        post_process(input_value)

        return f"'{input_value}'를 주제로 포스팅 완료!"
    else:
        return '잘못된 요청입니다.'
'''
@app.route('/process', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        if SYS_PLATFORM == 'Windows':
            SUBJECT_PATH = os.path.join(ROOT_DIR, 'config\subject.json')
        else:
            SUBJECT_PATH = os.path.join(ROOT_DIR, 'config/subject.json')
        if os.path.isfile(SUBJECT_PATH):
            with open(SUBJECT_PATH) as json_file:
                subjects = json.load(json_file)
        else :
            root_logger.critical("subject.json 파일 읽기 실패")
            return f"주제 : '{input_value}', 포스팅 대기열 추가 실패.. 다시 시도해주세요."

        input_value = request.form['myInput']
        if len(input_value) > 0:
            subjects['subject'].append(input_value)

        with open(SUBJECT_PATH, 'w') as json_file:
            json.dump(subjects, json_file)

        return f"주제 : '{input_value}', 포스팅 대기열 추가 완료! ({len(subjects['subject'])}개 남음)"
    else:
        return '잘못된 요청입니다.'


@app.route('/uploadpost', methods=['GET', 'POST'])
def uploadpost():
    if request.method == 'GET' or request.method == 'POST' :
        input_value = request.args.get('input')
        
        if input_value is not None :
            post_process(input_value)
            return f"'{input_value}'를 주제로 포스팅 완료!"

        else :
            return f"wrong input value"
            
    else:
        return '잘못된 요청입니다.'

class Worker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        root_logger.critical(f"subject upload daemon 시작, interval = {INTERVAL}")
        time.sleep(5)
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
            
            if len(subjects['subject']) > 0 :
                s = subjects['subject'][0]
                
                del subjects['subject'][0]
                with open(SUBJECT_PATH, 'w') as json_file:
                    json.dump(subjects, json_file)

                if len(s) > 0:
                    post_process(s)
                
            root_logger.critical(f"남은 subject 개수 : {len(subjects['subject'])}")

            # 주기가 너무 일정하지 않게끔
            time.sleep(INTERVAL * random.randint(40, 60) + random.randint(0, 100))

def conscience(content):
    return f"{content} \n\n\n\n 이 글은 ChatGPT API를 이용하여 자동으로 작성된 글입니다."

def post_process(input_value) :
    root_logger.critical(f"{input_value}에 대한 글 작성 시작...")
    post_subject = input_value
    prompt = f"'{post_subject}'에 대한 주제의 블로그 글, 자세하게, markdown"
    response = generate_text(prompt, max_token=MAX_TOKEN)
    root_logger.critical(response)

    prompt = make_prompt_for_image(post_subject)
    
    img_path = make_image_karlo(post_subject, prompt)
    #img_path = make_image_dall_e(post_subject, prompt)
    
    #response = insert_image_into_markdown(response, img_path)
    response = insert_tistory_image_into_markdown(response, upload_to_tistory(img_path))

    response = conscience(response)

    post_path = drop_to_markdown(f"{post_subject}", response)

    #post_to_tistory_markdown(post_subject, post_path)
    post_to_tistory(post_subject, post_path)
