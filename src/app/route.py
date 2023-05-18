#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, jsonify, make_response
from app import *

flask_app = Flask(__name__)
flask_app.config['JSON_AS_ASCII'] = False

if SYS_PLATFORM == 'Windows':
    SUBJECT_PATH = os.path.join(ROOT_DIR, 'config\subject.json')
else:
    SUBJECT_PATH = os.path.join(ROOT_DIR, 'config/subject.json')
    
@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/process', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if os.path.isfile(SUBJECT_PATH):
            with open(SUBJECT_PATH) as json_file:
                subjects = json.load(json_file)
        else :
            root_logger.critical("subject.json 파일 읽기 실패")
            return f"주제 : '{input_value}', 포스팅 대기열 추가 실패.. 다시 시도해주세요."
        
        input_value = request.form['myInput']
        if len(input_value) > 0:
            subjects['subjects'].append(input_value)
        else :
            return f"주제가 잘못되었습니다. 다시 시도해주세요."

        with open(SUBJECT_PATH, 'w') as json_file:
            json.dump(subjects, json_file, ensure_ascii=False)

        return f"주제 : '{input_value}', 포스팅 대기열 추가 완료! ({len(subjects['subjects'])}개 남음)"
    else:
        return '잘못된 요청입니다.'


@flask_app.route('/uploadpost', methods=['GET', 'POST'])
def uploadpost():
    if request.method == 'POST' :
        input_value = request.args.get('input')
        
        if input_value is not None :
            post_process(input_value)
            return f"'{input_value}'를 주제로 포스팅 완료!"

        else :
            return f"wrong input value"
    elif request.method == 'GET' :
        if os.path.isfile(SUBJECT_PATH):
            with open(SUBJECT_PATH) as json_file:
                subjects = json.load(json_file)
        else :
            root_logger.critical("subject.json 파일 읽기 실패")
            return f"포스팅 대기열 조회 실패.. 다시 시도해주세요."
        
        return make_response(json.dumps(subjects, ensure_ascii=False, indent=4))
    else:
        return '잘못된 요청입니다.'

