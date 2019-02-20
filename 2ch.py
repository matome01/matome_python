##2ch.sc는 자바스크립트모드on하면 쿠키값 READJS의 값이 "on"으로, cgi모드로하면 "off"로 바뀜. 따라서 지금은 그냥 잘되는데 나중에 쿠키값 설정해야만 parse할 수 있을지도 모름
##글고 여기 html구조가 개좆병신임. <dt>로시작해 </dt>같은 끝맺는게없고 등
import requests
import re
from bs4 import BeautifulSoup
from papago_translation import papago

def execute(thread_url, list_):
    res = requests.get(thread_url)
    thread_url = res.url #리다이렉트후 url
    soup = BeautifulSoup(res.text, 'lxml')
    thread_title = soup.title.get_text()
    soup = soup.find("dl")
    headers = soup.find_all("dt")
    contents = soup.find_all("dd")
    thread_opId = set()
    #매치가 1개인지 확인하는건 걍 생략함 (넣고싶으면 open2ch 참조)
    def comment_extract(num):
        comment_header = headers[int(num)-1] #soup.select(f'dt:nth-of-type({int(num)})')[0] <-select는 css selector이용하는건데 이거 존나느림 (select가 느린게아니라 내 css selector가 존나느린 selector인걸수도)
        comment_content = contents[int(num)-1] #soup.select(f'dd:nth-of-type({int(num)})')[0]
        
        comment_header_text = comment_header.get_text("\n", strip=True)
        comment_text = comment_content.get_text("\n", strip=True)
        
        comment_datetime = re.search(r'([1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1]).*\d)\s\S+net', comment_header_text).group(1)        
        comment_authorId = re.search(r'\s(ID:)?(\S*\.net)', comment_header_text).group(2) #어쩌면 net으로 안끝날수도..
        comment_anchor = re.findall(r'>>\d+', comment_text)
        #thread_opId.add() #<-2ch.sc에서 스레주인지 알수있는 방법이 아직까진 난 모른다..나중에 추가하던가하자
        comment_media = []
        for i in re.finditer(r'h?ttp.*\.(jpg|jpeg|png|mp4|gif)', comment_text, re.I):#나중에 확장자 더 필요하면 추가하기
            comment_media.append(i.group(0))

        comment_text_kr = papago(comment_text)
        print(f'{num} - Translation completed')
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