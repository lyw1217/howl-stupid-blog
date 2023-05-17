from PyKakao import Karlo
from app.config import *
from app.openai import *

'''
kako karlo에게 이미지 생성 요청하는 함수
'''
def make_image_karlo(subject, prompt) :

    api = Karlo(service_key = KAKAO_REST_KEY)

    # 이미지 생성하기 REST API 호출
    img_dict = api.text_to_image(prompt, 1)

    # 생성된 이미지 정보
    if img_dict.get("images") is not None :
        img_str = img_dict.get("images")[0].get('image')

        # base64 string을 이미지로 변환
        img = api.string_to_image(base64_string = img_str, mode = 'RGBA')

        # 이미지 저장하기
        if SYS_PLATFORM == 'Windows':
            path = os.path.join(ROOT_DIR, f"img\{subject}.png")
        else :
            path = os.path.join(ROOT_DIR, f"img/{subject}.png")

        img.save(path)

        root_logger.critical(f"karlo 이미지 저장 성공, path = {path}")
    else :
        '''
        실패 시 dall-e 사용
        '''
        root_logger.critical(f"Fail. karlo 이미지 저장 실패, Dall-E 사용")
        path = make_image_dall_e(subject, prompt)

    return path

