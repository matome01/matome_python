##할일: class="thread"로 추려도 될꺼같은데 왜 병신같이 script제거 등 개짓을했지?
##아 제거하건 하무소쿠 등 마토메였지...그렇긴하지만 여전히 class="thread"로 거르지 않은 이유?
##사실 거를이유가없지않나..? open2ch가 구조가 더러운것도아니고..?

import requests
import re
from bs4 import BeautifulSoup
from papago_translation import papago

from fetch import list_, thread_url
#from url_ import thread_url

res = requests.get(thread_url)
soup = BeautifulSoup(res.text, 'lxml')
thread_title = soup.title.get_text()

#매치가 1개인지 확인하기
try:
    for _ in list_:
        if len(soup.find_all("dt", { "res": _ })) != 1:
            raise ValueError("에러: BeautifulSoup의 find_all 검색결과 매치가 1개가 아닌 항목이 있습니다")
except ValueError as e:
    print(e)
else:
    print("성공: BeautifulSoup의 find_all 검색결과 모든 매치가 1개입니다")

#extracting
thread_opId = set()
def comment_extract(num): #num은 '1'같은 숫자 스트링 #캡쳐한것:작성시각,ID,앵커,리플텍스트,글쓴이ID바뀌는거캐치 #닉네임은 캡쳐할필요없어서 안함 #soup를 파라미터로 넣을까...
    #author가공
    comment_header = soup.find("dt", { "res" : num }) #dt캡쳐완료
    comment_datetime = comment_header.find(string=re.compile(r'[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])'))
    comment_datetime = comment_datetime[1:-1] #위의 comment_datime은 ': 2018/10/07(日)23:02:37 '의형식. 이걸 가공
    #comment_authorId = comment_header.find(class_="id").get_text() #<-옵션1. 맨윗놈글쓴놈은 ID:라는게 앞에 붙어버림
    comment_authorId = comment_header.find(class_="_id").get("val") #<-옵션2. 이걸로할까? 위에완다르게 이건 맨윗글도 ID:라는거 안붙는데...
    ##author가공->스레주id가공
    global thread_opId
    if comment_header.find_all(string="主"): #find_all인 이유: 主가 해더에 있을수도있다(예를들면 닉네임)
        if len(comment_header.find_all(string="主")) > 1:
            return print("에러: 한 코멘트에 主가 여러개발견됨") #raise Error로 바꿀까...
        thread_opId.add(comment_header.find(string="主").find_previous(class_="_id").get("val")) #find_all할필요없지. 위에서 이미 1개 초과면 return해버렸으니까 #find를 다시하게됨으로써 메모리가 낭비됨. 위에 find_all이랑 잘 합쳐서 한번만 검색하게 할 수도 있는데, 일단 지금은 귀찮아서 이대로함 
    #content가공
    comment_content = soup.find("dt", { "res" : num }).find_next_sibling("dd") #dd캡쳐완료 .get_text("\n")
    for _ in comment_content.find_all("ares"):
        _.decompose() #ares지우기
    for _ in comment_content.find_all("table"):
        _.decompose() #table지우기(이이네 이케나이 삭제)
    comment_anchor = [_.get_text() for _ in comment_content.find_all("a", { "class" : "_ank" })] #>>66 등 anchor캡쳐완료 #근데 두개달렸으면 어떻게처리하지? 리플박스를 두개로달아야하나...시발..답안나오네
    comment_text = comment_content.get_text("\n", strip=True)
    
    #print(comment_datetime, comment_authorId, comment_text, comment_anchor) #<-이것들을 추출했으니 여기서 골라쓰시오. #추가할것:트위터, 사진, 유투브 <-유투브는 링크가아래나오니까상관없나?
    #print(type(comment_datetime), type(comment_authorId), type(comment_text), type(comment_anchor))
    
    #ja -> ko translation
    comment_text_kr = papago(comment_text)
    return num, comment_datetime, comment_authorId, comment_text, comment_text_kr, comment_anchor,



#for i in range(1, 101):
#    comment_extract(str(i))

import json
def comment_jsonify(comment_num, comment_datetime, comment_authorId, comment_text, comment_text_kr, comment_anchor): #위에선 comment_num을 걍 num이라고해버림...
    return {"comment_num": comment_num, "comment_datetime": comment_datetime, "comment_authorId": comment_authorId, "comment_anchor": comment_anchor, "comment_text": comment_text, "comment_text_kr": comment_text_kr}
def thread_jsonify(thread_url, thread_title, thread_opId, comments):
    thread_title_kr = papago(thread_title)
    return {"thread_url": thread_url, "thread_title": thread_title, "thread_title_kr": thread_title_kr,"thread_opId": thread_opId, "comments": comments}
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