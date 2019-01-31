import requests
import re
from bs4 import BeautifulSoup
#url = "http://michaelsan.livedoor.biz/archives/51968268.html" #모미아게
#url = "http://hamusoku.com/archives/9982700.html" #하무소쿠 <--VIPPER나오래때문에 \s名前추가했더니 이번엔 이곳 하무소쿠전용 코멘트들이 걸려버리네..
#url = "http://matometanews.com/archives/1926208.html" #마토메타뉴스
#url = "http://alfalfalfa.com/articles/245007.html" #알파루파모자이크
#url = "http://news4vip.livedoor.biz/archives/52309674.html" #2ch뉴속퀄리티 <-첫빠따가 ID:ID로시작함-_-그래서2번잡힘
#url = "http://workingnews.blog117.fc2.com/blog-entry-12334.html" #하타라쿠모노
#url = "http://blog.livedoor.jp/dqnplus/archives/1986778.html" #이타이뉴스 <-첫빠따가 regex2에서빠져있고 regex3에서는 안보이는 글쓴시점이 추가되어나옴 <-VIPPER나오레를 위해 \s名前를 추가했던게 여기서 첫빠따까지 포함시키는 우연한 해결이 되버림
#url = "http://blog.livedoor.jp/news23vip/archives/5448512.html" #VIPPER나오레 <-위와 마찬가지로 글쓴시점 추가되어나옴, ID가 아래 사이트리플까지 포함돼서 존나많게나옴
#url = "http://news4wide.livedoor.biz/archives/2216466.html" #VIP와이드가이드 <-위와 마찬가지로 글쓴시점 추가되어나옴, ID가 아래 사이트리플까지 포함돼서 존나많게나옴, 1001: 짜리가달려있음
#url = "http://kanasoku.info/articles/116358.html" #카나소쿠 <- 걍 형태가 좆나달라서 포기함
#url = "http://blog.livedoor.jp/kinisoku/archives/5019579.html" #키니나루속보
#url = "http://himasoku.com/archives/52063383.html" #히마진
#url = "http://burusoku-vip.com/archives/1902784.html" #부루소쿠
#url = "http://blog.livedoor.jp/nwknews/archives/5448635.html" #철학뉴스
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml') #res.content? #type(res.text) == String
#soup = BeautifulSoup(soup.prettify(), 'lxml')
#print(soup.body.get_text())
#print(soup.prettify())
#print(soup.find_all("script"))
for _ in soup.find_all("script"):
    _.decompose()
for _ in soup.find_all("style"):
    _.decompose()
print(f'스크립트, 스타일태그 전부 제거 완료 여부: {soup.find_all("script") == soup.find_all("style") == []}')
regex = re.compile(r'[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1])').findall(soup.body.get_text()) #2019/01/01
regex2 = re.compile(r'(\d{1,3})(：|:\s|\s[:：]|\s名前：)').findall(soup.body.get_text()) #281 : #\s名前는 VIPPER나오레때문에 붙였음 맨앞에 \b버림. ㅁㅇㄹ14: 이런식으로 prettify하지않았을때 인식못해버려서.
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