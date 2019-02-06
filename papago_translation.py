import os
import sys
import urllib.request
import json

def papago(jp_text):
    if not jp_text:
        return ''
    client_id = "0LXVE6HwgspFsDYf9jg0" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "80ijFS0PqF" # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(jp_text)
    data = "source=ja&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt" # <-NMT번역
    #url = "https://openapi.naver.com/v1/language/translate"# <-SMT번역
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        jsoned = json.loads(response_body.decode('utf-8'))
        return jsoned['message']['result']['translatedText']
        #print(response_body.decode('utf-8'))
    else:
        #print("Error Code:" + rescode)
        return "Error Code:" + rescode

if __name__ == '__main__':
    papago("俺は悪魔だ")

    #텍스트하나하나를 하지말고 걍 list of stirngs로 해서 한번만 requeset보낼까