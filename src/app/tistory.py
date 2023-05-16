from app.config import *
import requests
import subprocess
import markdown

def post_to_tistory(title, path):

    with open(path, 'r') as f:
        content = f.read()

    content = markdown.markdown(content)

    url = f"https://www.tistory.com/apis/post/write"
    
    data = {
        'access_token': TISTORY_ACCESS_TOKEN,
        'output': 'json',
        'blogName': BLOG_NAME,
        'visibility':3,
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


def upload_to_tistory(path):
    requests_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    files = {'uploadedfile': open(path, 'rb')}

    url = f'https://www.tistory.com/apis/post/attach?access_token={TISTORY_ACCESS_TOKEN}&blogName={BLOG_NAME}&output=json'

    response = requests.post(url, files=files,headers=requests_headers)
    result = response.json()

    if 'tistory' in result and 'status' in result['tistory']:
        status = result['tistory']['status']
        if status == '200':
            root_logger.critical("이미지가 성공적으로 업로드되었습니다.")
            return result['tistory']['replacer']
        else:
            root_logger.critical(f"이미지 업로드에 실패하였습니다. 오류 코드: {status}")
            root_logger.critical(result)
            return ""
    else:
        root_logger.critical("API 응답 형식이 잘못되었습니다.")
        return ""

'''
path : markdown 파일의 경로
title : 포스팅 제목
content : 포스팅 내용
https://github.com/jojoldu/markdown-tistory
'''
def post_to_tistory_markdown(title, path):
    out = subprocess.run(['/usr/local/bin/markdown-tistory', 'write' , path], capture_output=True)
    root_logger.critical(f"{out.stdout}")

'''
markdown 맨 뒤에 이미지를 추가하는 함수
'''
def insert_image_into_markdown(md_content, img_path):
    return f"{md_content} \n\n\n ![image]({img_path})"

'''
tistory image 추가
'''
def insert_tistory_image_into_markdown(md_content, replacer):
    return f"{md_content} \n\n\n <p>{replacer}</p>"
