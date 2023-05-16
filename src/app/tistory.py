from app.config import *
import requests
import subprocess

def post_to_tistory(access_token, blog_name, title, content):
    url = f"https://www.tistory.com/apis/post/write"
    
    data = {
        'access_token': access_token,
        'output': 'json',
        'blogName': blog_name,
        'title': title,
        'content': content
    }

    response = requests.post(url, data=data)
    result = response.json()

    if 'tistory' in result and 'status' in result['tistory']:
        status = result['tistory']['status']
        if status == '200':
            root_logger.critical("글이 성공적으로 작성되었습니다.")
        else:
            root_logger.critical(f"글 작성에 실패하였습니다. 오류 코드: {status}")
            root_logger.critical(result)
    else:
        root_logger.critical("API 응답 형식이 잘못되었습니다.")

'''
path : markdown 파일의 경로
title : 포스팅 제목
content : 포스팅 내용
https://github.com/jojoldu/markdown-tistory
'''
def post_to_tistory_markdown(path, title, content):
    out = subprocess.run(['/usr/local/bin/markdown-tistory', 'write' , path], capture_output=True)
    root_logger.critical(f"{out.stdout}")

'''
markdown 맨 뒤에 이미지를 추가하는 함수
'''
def insert_image_into_markdown(md_content, img_path):
    return f"{md_content} \n\n\n ![image]({img_path})"
