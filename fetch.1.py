import requests
import re
from bs4 import BeautifulSoup

#url = "http://michaelsan.livedoor.biz/archives/51968268.html"
#url = "http://hamusoku.com/archives/9982700.html"
#res = requests.get(url)
#soup = BeautifulSoup(res.text, 'lxml') #res.content? #type(res.text) == String
#soup = BeautifulSoup(soup.prettify(), 'lxml')
#print(soup.body.get_text())
#print(soup.prettify())
#regex = re.compile(r'\S.*[1-2]\d{3}(\/)(((0)[1-9])|((1)[0-2]))(\/)([0-2][0-9]|(3)[0-1]).*').finditer(soup.body.get_text()) #.*뒤에 $안붙여도 상관없나? 그리고 두번째 파라미터에 re.M 필요없나?
#for i in regex:
    #print(i.group(0))
    #print(i)