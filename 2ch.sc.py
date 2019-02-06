##2ch.sc는 자바스크립트모드on하면 쿠키값 READJS의 값이 "on"으로, cgi모드로하면 "off"로 바뀜.
##따라서 지금은 그냥 잘되는데 나중에 쿠키값 설정해야만 parse할 수 있을지도 모름
##글고 여기 html구조가 개좆병신임. <dt>로시작해 </dt>같은 끝맺는게없고 등

import requests
import re
from bs4 import BeautifulSoup
from papago_translation import papago

from fetch import list_
from url_ import thread_url

#list_ = ['1','2','3','4','5','6','7','8','9','10']
#thread_url = "http://tomcat.2ch.sc/test/read.cgi/livejupiter/1548911167/"

res = requests.get(thread_url)
soup = BeautifulSoup(res.text, 'lxml')
thread_title = soup.title.get_text()
soup = soup.find("dl")

#매치가 1개인지 확인하는건 걍 생략함 (넣고싶으면 open2ch 참조)

thread_opId = set()
def comment_extract(num):
    comment_header = soup.select(f'dt:nth-of-type({int(num)})')[0]#찾는거 걍 num번째 dt로 해서 찾음..더 정확히는 "1  :"을 포함하는 뭐 이런식으로 찾는게 더 정확하겠지..
    comment_content = soup.select(f'dd:nth-of-type({int(num)})')[0]
    
    comment_header_text = comment_header.get_text("\n", strip=True)
    comment_text = comment_content.get_text("\n", strip=True)

    comment_datetime_before = re.search(r'([1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1]).*) ID:', comment_header_text)
    comment_datetime = comment_datetime_before.group(1)

    comment_authorId_before = re.search(r'(ID:)\s?(.*net)', comment_header_text) #어쩌면 net으로 안끝날수도..
    comment_authorId = comment_authorId_before.group(2)
    
    comment_anchor = re.findall(r'>>\d*', comment_text) #\d+로하는게나을까?

    global thread_opId
    #thread_opId.add() #<-2ch.sc에서 스레주인지 알수있는 방법이 아직까진 난 모른다..나중에 추가하던가하자
    
    comment_text_kr = papago(comment_text)
    return num, comment_datetime, comment_authorId, comment_text, comment_text_kr, comment_anchor,

#이하 open2ch.py와 같음
import json
def comment_jsonify(comment_num, comment_datetime, comment_authorId, comment_text, comment_text_kr, comment_anchor): #위에선 comment_num을 걍 num이라고해버림...
    return {"comment_num": comment_num, "comment_datetime": comment_datetime, "comment_authorId": comment_authorId, "comment_anchor": comment_anchor, "comment_text": comment_text, "comment_text_kr": comment_text_kr}
def thread_jsonify(thread_url, thread_title, thread_opId, comments):
    thread_title_kr = papago(thread_title)
    return {"thread_url": thread_url, "thread_title": thread_title, "thread_title_kr": thread_title_kr, "thread_opId": thread_opId, "comments": comments}
def comments_jsonify(list_): #soup를 파라미터로 넣을까...#soup를뺐는데, 그럼 list_도 파라미터에넣을필요가없잖아...?
    i = []
    for _ in list_:
        i.append(comment_jsonify(*comment_extract(_)))
    global thread_opId
    thread_opId = list(thread_opId) #set은 JSON파일에 부적합 #global선언하는거 좋지않은거같다. 코드 수정하자?
    return i
def completed(list_):
    comments = comments_jsonify(list_)
    return thread_jsonify(thread_url, thread_title, thread_opId, comments)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[\\/*?:"<>|]', '-', s)

def save_completed(list_):
    with open(f'{save_path}/{get_valid_filename(thread_title)}.json', 'w', encoding="utf-8") as f: #파일명.json으로하면 파일명에 들어가면안되는 문자가 들어갈수도있지않나...
        json.dump(completed(list_), f, ensure_ascii=False, indent=2)

#저장경로 configuration
from pathlib import Path
relative_path = "jsons"
save_path = (Path(__file__).parent / relative_path).resolve()

save_completed(list_)