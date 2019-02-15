import requests
import re
from bs4 import BeautifulSoup
from papago_translation import papago

def execute(thread_url, list_):
    res = requests.get(thread_url)
    soup = BeautifulSoup(res.text, 'lxml')
    thread_title = soup.title.get_text()
    thread_opId = set()
    #매치가 1개인지 확인하기
    try:
        for _ in list_:
            if len(soup.find_all("dt", { "res": _ })) != 1:
                raise ValueError("에러: BeautifulSoup의 find_all 검색결과 매치가 1개가 아닌 항목이 있습니다")
    except ValueError:
        raise
    else:
        print("성공: BeautifulSoup의 find_all 검색결과 모든 매치가 1개입니다")
    
    def comment_extract(num): #num은 '1'같은 숫자 스트링 #캡쳐한것:작성시각,ID,앵커,리플텍스트,글쓴이ID바뀌는거캐치 #닉네임은 캡쳐할필요없어서 안함 #soup를 파라미터로 넣을까...
        #author가공
        comment_header = soup.find("dt", { "res" : num }) #dt캡쳐완료
        comment_datetime = comment_header.find(string=re.compile(r'[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])'))
        comment_datetime = comment_datetime[1:-1] #위의 comment_datime은 '：2019/01/29(火)17:40:50 '의형식. 이걸 가공
        #comment_authorId = comment_header.find(class_="id").get_text() #<-옵션1. 맨윗놈글쓴놈은 ID:라는게 앞에 붙어버림
        comment_authorId = comment_header.find(class_="_id").get("val") #<-옵션2. 이걸로할까? 위에완다르게 이건 맨윗글도 ID:라는거 안붙는데...
        ##author가공->스레주id가공
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
        comment_media = []
        for i in re.finditer(r'h?ttp.*(jpg|jpeg|png|mp4|gif)', comment_text, re.I):#나중에 확장자 더 필요하면 추가하기
            comment_media.append(i.group(0))
        comment_text_kr = papago(comment_text)
        return num, comment_datetime, comment_authorId, comment_anchor, comment_media, comment_text, comment_text_kr,

    def comment_list(list_): #soup를 파라미터로 넣을까...#soup를뺐는데, 그럼 list_도 파라미터에넣을필요가없잖아...?
        i = []
        for _ in list_:
            dicted = dict(zip(["comment_num", "comment_datetime", "comment_authorId", "comment_anchor", "comment_media", "comment_text", "comment_text_kr"], comment_extract(_)))
            i.append(dicted)
        return i

    def completed_json(list_):
        comments = comment_list(list_)
        thread_title_kr = papago(thread_title)
        nonlocal thread_opId
        thread_opId = list(thread_opId)
        thread_opId.append(comment_extract(list_[0])[2]) #걍 처음에나오는애를 opId로 넣음
        return {"thread_url": thread_url, "thread_title": thread_title, "thread_title_kr": thread_title_kr, "thread_opId": thread_opId, "comments": comments}

    def save(list_):
        import json
        import datetime
        from pathlib import Path
        save_path = (Path(__file__).parent / "jsons").resolve()
        filename = datetime.datetime.today().strftime("%Y%m%d") #원래는 get_valid_filename(thread_title)<-이거였음
        with open(f'{save_path}/{filename}.json', 'w', encoding="utf-8") as f:#위에꺼는 json파일명이 일본어합쳐져서 나오는버전이고, 걍 이거 싫어서 이제는 날짜.json으로 할꺼..그게 이거
            json.dump(completed_json(list_), f, ensure_ascii=False, indent=2)
    
    save(list_)

    
    #def get_valid_filename(s): #지금은 사용안하는함수이지만 지우지않고 그냥 놥둠
    #    s = str(s).strip().replace(' ', '_')
    #    return re.sub(r'[\\/*?:"<>|]', '-', s)