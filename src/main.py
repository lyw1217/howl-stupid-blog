from app import *
    
from flask import Flask, render_template, request

def post_process(input_value) :

    post_subject = input_value
    prompt = f"'{post_subject}'에 대한 주제의 블로그 글, 자세하게, markdown"
    response = generate_text(prompt, max_token=MAX_TOKEN)
    root_logger.critical(response)

    prompt = make_prompt_for_image(post_subject)
    img_path = make_image_karlo(post_subject, prompt)
    #img_path = make_image_dall_e(post_subject, prompt)
    response = insert_image_into_markdown(response, img_path)

    post_path = drop_to_markdown(post_subject, response)

    #post_to_tistory(TISTORY_ACCESS_TOKEN, BLOG_NAME, title, response)
    post_to_tistory_markdown(post_path, post_subject, response)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        input_value = request.form['myInput']

        post_process(input_value)

        return f"'{input_value}'를 주제로 포스팅 완료!"
    else:
        return '잘못된 요청입니다.'

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

if __name__ == "__main__":

    print_initlog()

    app.run(debug=True, port=8080)