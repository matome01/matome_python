from importlib import import_module
import datetime
import json

from media_down import down
from fetch import site

#할일: girlschannel 추가하기

if site in ['5ch.net', '2ch.sc']:
    import_module('2ch')
if site in ['open2ch.net']:
    import_module('open2ch')

##위에서 fetch하고 import_module안에서 한번 더 fetch를 import하는데 한번만 실행되네...즉 같은모듈을 import 두번해도 한번만 실행하는듯..?

with open('./jsons/' + datetime.datetime.today().strftime("%Y%m%d") + '.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for i in data['comments']:
        for j in i['comment_media']:
            down(j)