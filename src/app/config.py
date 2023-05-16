import os
import json
import platform
import logging
import logging.config
import sys

''' 경로 설정 '''
if getattr(sys, 'frozen', False):
    # 임시 파일 경로로 지정됨
    #BASE_DIR = os.path.join(sys._MEIPASS, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #ROOT_DIR = os.path.join(sys._MEIPASS, os.path.dirname(BASE_DIR))
    # 실행파일이 위치한 경로를 BASE로 잡음
    BASE_DIR = os.path.abspath("")
    ROOT_DIR = BASE_DIR
else:
    # main.py가 위치한 경로를 BASE로 잡음
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.path.dirname(BASE_DIR)

SYS_PLATFORM = platform.system()

''' Logging Configuration '''
if SYS_PLATFORM == 'Windows':
    LOG_CFG_PATH = os.path.join(ROOT_DIR, 'config\logging.json')
else:
    LOG_CFG_PATH = os.path.join(ROOT_DIR, 'config/logging.json')

with open(LOG_CFG_PATH) as json_file:
    log_configs = json.load(json_file)
    LOGGING_PATH = os.path.abspath(os.path.join(
        log_configs['handlers']['file']['filename'], os.pardir))
    if os.path.isdir(LOGGING_PATH) != True:
        os.makedirs(LOGGING_PATH)
    logging.config.dictConfig(log_configs)

root_logger = logging.getLogger()
'''
# USAGE
root_logger.debug("디버그")
root_logger.info("정보")
root_logger.error("오류")
'''
parent_logger = logging.getLogger("parent")
'''
# USAGE
parent_logger.debug("디버그")
parent_logger.info("정보")
parent_logger.error("오류")
'''
child_logger = logging.getLogger("parent.child")
'''
# USAGE
child_logger.debug("디버그")
child_logger.info("정보")
child_logger.error("오류")
'''

''' Main Configuration '''
if SYS_PLATFORM == 'Windows':
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config\config.json')
else:
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config/config.json')

with open(CONFIG_PATH) as json_file:
    configs = json.load(json_file)

    INTERVAL = int(configs['interval'])
    GPT_MODEL = configs['gpt-model']
    MAX_TOKEN = int(configs['max_token'])


if SYS_PLATFORM == 'Windows':
    SECRETS_PATH = os.path.join(ROOT_DIR, 'config\secrets.json')
else:
    SECRETS_PATH = os.path.join(ROOT_DIR, 'config/secrets.json')
if os.path.isfile(SECRETS_PATH):
    with open(SECRETS_PATH) as json_file:
        sec = json.load(json_file)
        try :
            TISTORY_APP_ID = sec['TISTORY_APP_ID']
            root_logger.critical(f'Loaded TISTORY_APP_ID')
        except KeyError :
            root_logger.critical(f"No TISTORY_APP_ID.")
        try :
            TISTORY_KEY = sec['TISTORY_KEY']
            root_logger.critical(f'Loaded TISTORY_KEY')
        except KeyError :
            root_logger.critical(f"No TISTORY_KEY.")
        try :
            TISTORY_ACCESS_TOKEN = sec['TISTORY_ACCESS_TOKEN']
            root_logger.critical(f'Loaded TISTORY_ACCESS_TOKEN')
        except KeyError :
            root_logger.critical(f"No TISTORY_ACCESS_TOKEN.")
        try :
            OPENAI_API_KEY = sec['OPENAI_API_KEY']
            root_logger.critical(f'Loaded OPENAI_API_KEY')
        except KeyError :
            root_logger.critical(f"No OPENAI_API_KEY.")
        try :
            KAKAO_REST_KEY = sec['KAKAO_REST_KEY']
            root_logger.critical(f'Loaded KAKAO_REST_KEY')
        except KeyError :
            root_logger.critical(f"No KAKAO_REST_KEY.")
        root_logger.critical('=== PRIVATE LOADED ===')