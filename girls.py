import requests
import re
from bs4 import BeautifulSoup
from papago_translation import papago
import math
#url_.py, fetch.py 필요없어서 빼버림. 내가 직접 수동으로 입력해야함 아래 thread_url과 list_를.
thread_url = "https://girlschannel.net/topics/2001112/"
list_ = ['1','3','6','8','200','400','600','800','1000','1001','1040','1400','1499','1500','1501','1999','2000', '2', '5400', '5500']
list_.sort(key=int)
list__ = [ [i for i in list_ if int(i) <= 500*n and int(i) > 500*(n-1)] for n in range(1, math.ceil(int(list_[-1])/500) + 1) ]
#list__ = [ [i for i in list_ if int(i) <= 500*n and int(i) > 500*(n-1)] for n in range(1, int(int(list_[-1])/500) + 2) ] #이건 위에것보다 부정확함. 이걸로해도 상관없긴함. 단지 케이스에따라 마지막에 []빈 list가 생길수있음. 근데 생겨도 상관없음.
print(list__)
res = [ requests.get(f'{thread_url}{i}') for i, j in enumerate(list__, 1) if j ]
soup = [ BeautifulSoup(i.text, 'lxml') for i in res ]
thread_title = soup[0].select(".head-area h1")[0].get_text(strip=True)

thread_opId = set() #걸찬에는 이거 필요없음 어차피 싹다 익명이라 <---다시조사해보니 틀렸음. 익명아니게할수도있음. 근데 모두 익명만 사용하는듯?
def comment_extract(num, soup):
    box = soup.find(id=f'comment{num}')
    datetime = box.p.a.get_text()
    contentbox = box.find("div", class_="body")
    text_jp = contentbox.get_text("\n", strip=True)
    text_kr = papago(text_jp)
    #anchor = contentbox.find("span", class_="res-anchor").get_text() 이걸로할까?아래껄로할까? 상관없을듯...이건 근데 앵커 하나만잡음
    anchor = re.findall(r'>>\d+', text_jp)
    #추천비추천
    updownbox = box.find("div", id=f'vbox{num}')
    plus = updownbox.find("div", class_="icon-rate-wrap-plus").p.get_text()
    minus = updownbox.find("div", class_="icon-rate-wrap-minus").p.get_text()
    #미디어
    media = []
    for i in re.finditer(r'http.*(jpg|jpeg|png|mp4|gif)', text_jp, re.I):#나중에 확장자 더 필요하면 추가하기
        media.append(i.group(0))
    return num, datetime, text_jp, text_kr, anchor, plus, minus, media,

####아래는 다른것들과 거의 비슷#####
import json
def comment_jsonify(num, datetime, text_jp, text_kr, anchor, plus, minus, media): #위에선 comment_num을 걍 num이라고해버림...
    return {"comment_num": num, "comment_datetime": datetime, "comment_authorId": "익명", "comment_anchor": anchor, "comment_media": media, "comment_text": text_jp, "comment_text_kr": text_kr, "plus": plus, "minus": minus}
def thread_jsonify(thread_url, thread_title, thread_opId, comments):
    thread_title_kr = papago(thread_title)
    return {"thread_url": thread_url, "thread_title": thread_title, "thread_title_kr": thread_title_kr, "thread_opId": thread_opId, "comments": comments}
def comments_jsonify(list__): #나눌수도있겠지만 걍 한번에 1~99999까지 여기서 해결해버리게 짰음. 나중에 나눌려면 나누셈...한 soup(한페이지)만 받아서 하고 다른곳에서 for loop으로 이 함수 불러와서 다시금 append하는식으로 #참고로 list__는없어도됌 그냥 넣음..
    list___ = [i for i in list__ if i] #맨위에 list__를 [['1','250','500'],[],['1001','1444']]처럼 남겨놓은것은, 변수 res때문에, 빈 list를 버릴수가없었다. 하지만 여기서는 버려야한다. list___는 [['1','250','500'], ['1001','1444']] 이런식
    i = [ comment_jsonify(*comment_extract(p, soup[r])) for r, q in enumerate(list___) for p in q ]
    global thread_opId
    thread_opId = list(thread_opId) #set은 JSON파일에 부적합 #global선언하는거 좋지않은거같다. 코드 수정하자?
    return i
def completed(list__):
    comments = comments_jsonify(list__)
    return thread_jsonify(thread_url, thread_title, thread_opId, comments)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[\\/*?:"<>|]', '-', s)

def save_completed(list_):
    #with open(f'{save_path}/{get_valid_filename(thread_title)}.json', 'w', encoding="utf-8") as f: #파일명.json으로하면 파일명에 들어가면안되는 문자가 들어갈수도있지않나...
    import datetime
    with open(f'{save_path}/{datetime.datetime.today().strftime("%Y%m%d")}.json', 'w', encoding="utf-8") as f:#위에꺼는 json파일명이 일본어합쳐져서 나오는버전이고, 걍 이거 싫어서 이제는 날짜.json으로 할꺼..그게 이거
        json.dump(completed(list_), f, ensure_ascii=False, indent=2)

#저장경로 configuration
from pathlib import Path
relative_path = "jsons"
save_path = (Path(__file__).parent / relative_path).resolve()

save_completed(list__)