from app import *

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

    t = Worker()     # sub thread 생성
    t.daemon = True
    t.start()        # sub thread의 run 메서드를 호출

    app.run(port=8080)