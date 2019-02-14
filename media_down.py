import requests
import datetime
import pathlib
#url = "https://i.imgur.com/cYpit4p.jpg"
def down(url, filename=None):
    if filename is None:
        filename = './images/' + datetime.datetime.today().strftime('%Y%m%d/') + url.split("/")[-1]
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        if not pathlib.Path('./images/' + datetime.datetime.today().strftime('%Y%m%d/')).exists():
            pathlib.Path('./images/' + datetime.datetime.today().strftime('%Y%m%d/')).mkdir() #mkdir에 parents=True, exist_ok=True 넣을수도있지만 넣을필요가없다
        with open(filename, 'wb') as f:
            f.write(r.content)

if __name__ == '__main__':
    down("https://video.twimg.com/ext_tw_video/1093422301524062208/pu/vid/720x1280/4_aJ-IljVeMDG_kK.mp4")