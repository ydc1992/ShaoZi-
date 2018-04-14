

from common import *
# from xbmcswift2 import Plugin, xbmc, xbmcgui
from common import *
# import requests,re
# from bs4 import BeautifulSoup


@plugin.route('/start_91/<label>/<home_url>')
def start_91(label,home_url):
    global  s
    items=[]
    s = requests.Session()
    while True:
         try:
             r = s.get(home_url)
             if r.status_code==200:
                 break
         except:
             pass
    try:
            c = r.cookies.get_dict()
            c.update(language="cn_CN")
    except Exception,e:
            pass
    jar=requests.utils.cookiejar_from_dict(c)
    r= s.get(home_url,cookies=jar)
    source = r.content

    for s in BeautifulSoup(source).find_all("div",class_="listchannel"):
         url,image,title = re.findall("<a href=\"(.*?)\" target=\"blank\">.*?<img src=\"(.*?)\".*?title=\"(.*?)\"",str(s),re.S)[0]

         items.append({
             "label":title,
             "path":plugin.url_for("porn_91",url=url),
             "thumbnail":image,
             "is_playable":True
         })
    return  items


def get_html(urls):
    r = requests.get(urls,headers=setHeader() )
    html = r.content.decode('utf-8')
    #  <source src="http://185.38.13.159//mp43/257492.mp4?st=KWCRf3DKLtuEEF-RlyyNng&e=1521117517" type='video/mp4'>
    u = re.findall("<source src=\"(.*?)\" type='video/mp4",html,re.S)[0]
    return u

@plugin.route('/porn_91/<url>')
def porn_91(url):
     plugin.set_resolved_url(get_html(url))