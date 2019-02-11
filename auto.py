from importlib import import_module

from fetch import site

if site in ['5ch.net', '2ch.sc']:
    import_module('2ch')
if site in ['open2ch.net']:
    import_module('open2ch')

##위에서 fetch하고 import_module안에서 한번 더 fetch를 import하는데 한번만 실행되네...즉 같은모듈을 import 두번해도 한번만 실행하는듯..?