from app import *

if __name__ == "__main__":
    #
    #
    #
    #
    #
    #
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



    # 사용 예시
    post_subject = "지구온난화와 분리수거의 정도"
    prompt = f"'{post_subject}'에 대한 주제의 블로그 글, 자세하게, markdown"
    response = generate_text(prompt, max_token=MAX_TOKEN)
    root_logger.critical(response)

    #response = response.replace("\n", "</p><br></p>")

    post_path = drop_to_markdown(post_subject, response)

    #access_token = TISTORY_ACCESS_TOKEN
    #blog_name = 'nextdoorfire'
    #title = 'TEST'
    #content = response

    #post_to_tistory(access_token, blog_name, title, content)
    post_to_tistory_markdown(post_path, post_subject, response)