import requests
import re
from bs4 import BeautifulSoup
from url_ import url
#print(f'url: {url}') #뭐하러이걸표시하나, 아래에서 title을 표시하는데.
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml') #res.content? #type(res.text) == String
#print(soup.title.get_text())
#soup = soup.body #이거 새로넣었는데 괜찮을까?? body만 취득하게끔...걍버리자..아래 이미 body를넣어놔서...귀찮게됌
#soup = BeautifulSoup(soup.prettify(), 'lxml')
#print(soup.body.get_text())
#print(soup.prettify())
#print(soup.find_all("script"))
for _ in soup.find_all("script"):
    _.decompose()
for _ in soup.find_all("style"):
    _.decompose()
#print(f'스크립트, 스타일태그 전부 제거 완료 여부: {soup.find_all("script") == soup.find_all("style") == []}') #뭐하러 이걸 표시하나, 위에서 이미 확실하게 지웠는데
#print(soup.body.get_text())

#thread_url 추출
thread_url = ''
for site in ['open2ch.net', '2ch.sc', '5ch.net']:
    try:
        #print(1)
        thread_url = re.search(fr'http.*{site}/test/.*\d{{5,}}', soup.body.find(string=re.compile(fr'http.*{site}/test/.*\d{{5,}}'))).group(0)
        #print(2)
    except TypeError:
        #print(3)
        thread_url = soup.body.find(href=re.compile(fr'http.*{site}/test/.*\d{{5,}}')) and soup.body.find(href=re.compile(fr'http.*{site}/test/.*\d{{5,}}'))['href']
        #print(4)
    finally:
        if thread_url:
            break
thread_url = thread_url.replace("5ch.net", "2ch.sc")
print(thread_url)

regex = re.compile(r'[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])').findall(soup.body.get_text()) #2019/01/01
#regex2 = re.compile(r'(\d{1,3})(：|:\s|\s[:：]|\s名前：)').findall(soup.body.get_text()) #281 : #\s名前는 VIPPER나오레때문에 붙였음 맨앞에 \b버림. ㅁㅇㄹ14: 이런식으로 prettify하지않았을때 인식못해버려서.
regex2 = re.compile(r'(\d{1,3})(：|:\D|\s[:：]|\s名前：)').findall(soup.body.get_text()) #새로 만들어봤는데 어떨까? 테스트
#regex2 = re.compile(r'(^\d{1,3})(：|:|\s)', re.M).findall(soup.body.get_text()) #3번째버전. 새롭게만들어봤는데 어떨까? 테스트 #줄바꿈안되있는것이 있네 -_- 이거랑 위에꺼랑 번갈아가면서 쓰자
regex3 = re.compile(r'(([0-1][0-9])|([2][0-3])):([0-5][0-9]):([0-5][0-9])').findall(soup.body.get_text()) #18:03:58  <--할일: 첫매치가 두번쨰매치보다 미래의시간인경우 없애기 or script태그 없애고 시작하기 등 <-스크립트테그없앰
regex4 = re.compile(r'ID\s?[:：](ID)?').findall(soup.body.get_text()) #ID: #(ID)?는 ID:ID어쩌고라고 나와서 2번카운트되는경우가있어서 이렇게바꿈
#for i in regex:
#    print(i.group(0))
#for i in regex2:
#    print(i)
#print(regex2)
list_ = [i[0] for i in regex2]
if len(regex2) == len(list_):
    print(f'2019/01/01\t281:\t18:03:58\tID:\n{len(regex)}\t{len(regex2)}\t{len(regex3)}\t{len(regex4)}')
print(list_)
trim = input("list를 자동으로 trim하시겠습니까? (두번째 1: 이후 삭제): ") #마토메사이트댓글 거르기
if trim in ["Y", "y"]:
    #indexes = [i for i, x in enumerate(list_) if x == '1'] ##<--처음이 ['2','3',....,'1',...]이렇게 2부터 시작하는경우엔 에러생겨서 이걸 쓸수없다
    #list_ = list_[0:indexes[1]]
    try:
        index = list_[3:].index("1") #위의 문제를 수정한 버전 3:은 그냥 임의로 넣은숫자. 인덱스3이후에 1이오는걸 거른다.
        list_ = list_[0:index+3] #+3해줘야함 위에 3:이니까
    except ValueError:
        print("나중에 등장하는 1이 없습니다")
    print(f'trimmed list:\n{list_}')
        
trim2 = input("list를 한번 더 수동으로 trim하시겠습니까? : ") #수동 리스트작성
if trim2 in ["Y", "y"]:
    list_ = eval(input("list_ = ")) #eval은 매우위험

#For debug purpose:
if 0:
    for i in re.compile(r'[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])').finditer(soup.body.get_text()):
        print(i.group(0))
    for i in re.compile(r'\b(\d{1,3})(：|:\s|\s[:：]|\s名前：)').finditer(soup.body.get_text()):
        print(i.group(0))
    for i in re.compile(r'(([0-1][0-9])|([2][0-3])):([0-5][0-9]):([0-5][0-9])').finditer(soup.body.get_text()):
        print(i.group(0))
    for i in re.compile(r'ID\s?[:：]').finditer(soup.body.get_text()):
        print(i.group(0))
if 0:
    print(soup.body.get_text())

continue_ = input("fetch.py 실행완료. 계속 진행하시겠습니까? y/n: ")
if continue_ in ["n", "N"]:
    raise SystemExit(0)