from importlib import import_module
import datetime
import json
from media_down import down
import url_
#할일: girlschannel 추가하기
try:
    thread_url, list_ = url_.thread_url, url_.list_
except AttributeError:
    try:
        url = url_.url
    except AttributeError:
        raise
    thread_url, list_ = import_module('fetch').execute(url)
    continue_ = input("fetch.py 실행완료. 계속 진행하시겠습니까?: ")
    if continue_ in ["n", "N"]:
        raise SystemExit(0)

for i in ['open2ch', '2ch.sc', '5ch.net']:
    if thread_url.find(i) != -1:
        if i in ['5ch.net', '2ch.sc']:
            import_module('2ch').execute(thread_url, list_) #import를 쓰지 않은 이유: 2ch가 처음에 숫자가 와서 그냥 import로는 못함
        if i in ['open2ch.net']:
            import_module('open2ch').execute(thread_url, list_)

with open('./jsons/' + datetime.datetime.today().strftime("%Y%m%d") + '.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for i in data['comments']:
        for j in i['comment_media']:
            down(j)