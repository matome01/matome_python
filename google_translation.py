from pathlib import Path
from google.oauth2 import service_account
from google.cloud import translate
import six
credentials = service_account.Credentials.from_service_account_file(Path('./jp kr-5eb87c64ec67.json').resolve())
#scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

translate_client = translate.Client(credentials=credentials)

# The text to translate
text = u'''
自分は大学院2年生の8月末から東欧に留学していた
留学中は現地の大学の講義を受けて、大学寮に入ってた
でも、その子は、寮の玄関前に座り込んで、泣きもせずにずっと夜までじっとしてた
一度自分が変に手を出した責任も感じたし、湯冷めして風邪引いちゃいけないし、とにかく可哀想に思ってしまって、「今日1日だけ泊まっていく？」と聞いたら、パッと立ち上がって自分の部屋に入ってきて、ココアとベッドを奪って凄い勢いで寝始めた
友達は「金盗られるぞ」と怒ってた
ちなみに寮費はひと月4,000円弱
かなり物価の安い国
講義は平日9時から18時くらいまでビッシリ入っていたけど、週末は暇だった
暇すぎたので、いつも美術館か博物館か寮近くの喫茶店で時間を潰して過ごしてた
友達も少なかったし、日本人どころかアジア系の人もいなかったし
「金がなくて困ってるから金をくれ」とまた言われた
その時は講義直前だったし、相手は一人だったから、「また後で」と言って全力ダッシュで逃げた
24歳にもなって本気で走って子供から逃げることになるとは思わなかった
もう本気で逃げた
'''

if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Translates some text into Korean
translation = translate_client.translate(
    text, #text에 ['~','~']이렇게 array of strings 넣을수있음
    target_language='ko',
    source_language='ja',
    model='nmt') #or 'base' #아직 en<->하고만 nmt제공하고 다른건 다 base(phrase-based machine translation)임..ㅅㅂ..

#print(u'Text: {}'.format(text))
print(u'Text: {}'.format(translation['input']))
print(u'Translation: {}'.format(translation['translatedText']))
#print(u'Detected source language: {}'.format(translation['detectedSourceLanguage'])) #위 translate의 parameter에 source_language를 넣으면 이건 오류남
print(u'Used model: {}'.format(translation['model']))



#pip install --upgrade google-cloud-translate 지금깔린버전은 1.3.3
#텍스트하나하나를 하지말고 걍 list of stirngs로 해서 한번만 requeset보낼까