# -*- coding: utf-8 -*-

import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
from bs4 import BeautifulSoup
from xbmcswift2 import Plugin, xbmc, xbmcgui
import re
import urllib2
import urlparse
import json,urllib,os,cookielib

from parse_interface import  interface

plugin = Plugin()


main_url = "http://ljs.6621173.cn/"

pageNum = 1
hot = "NULL"
lang = "NULL"

a = \
    [
      [

        {"title": "全部类型", "id": 1},
        {"title": "VIP专区", "id": 30},
        {"title": "动作片", "id":5},
        {"title": "喜剧片", "id": 6},
        {"title": "科幻片", "id": 7},
        {"title": "恐怖片", "id": 9},
        {"title": "爱情片", "id": 8},
        {"title": "战争片", "id": 11},
        {"title": "悬疑片", "id": 16},
        {"title": "剧情片", "id": 10},
        {"title": "其他", "id": 19}
      ],

      [
          {"title": "国产剧", "id": 12},
          {"title": "港台剧", "id": 13},
          {"title": "日韩剧", "id": 14},
          {"title": "欧美剧", "id": 15},
          {"title": "其他剧", "id": 17},

      ],
      [
          {"title": "国产综艺", "id": 20},
          {"title": "港台综艺", "id": 21},
          {"title": "日韩综艺", "id": 24},
          {"title": "欧美综艺", "id": 22},
          {"title": "其他综艺", "id": 23},
      ],
      [
          {"title": "国产动漫", "id": 26},
          {"title": "日韩动漫", "id": 27},
          {"title": "其他动漫", "id": 29},

      ],
    ]



#电影视频类型
dianYing =[

]
#一级分类
Category = \
[
    { "title":"电影","id":0},
    { "title":"连续剧","id":1},
    { "title": "综艺","id":2},
    { "title":"动漫","id":3}
]

import pydevd
def debug(_debug):
    if _debug:
        pydevd.settrace(stdoutToServer=True, port=5678, stderrToServer=True)
    else:
        pass

_handle = int(sys.argv[1])
_url = sys.argv[0]



def get_page(url  ):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    req = urllib2.Request(url)

    response = urllib2.urlopen(req).read()
    return response


def Beautiful(soruce,csspath):
    return BeautifulSoup(soruce,"html.parser").select(csspath)



def parse_interface(interface_url,refer_url):
    a = interface(interface_url,refer_url)
    video_url = a.checkInterface()
    return video_url

def get_Video_url_list(url):
    video_list = []
    source = get_page(url)
    numList = Beautiful(source, "div.numList ul li a")

    for c in numList:
        video_list.append((c["title"],main_url+c["href"].encode("utf-8")))

    return video_list

@plugin.route('/play/<url>/<interface_url>')
def play(url,interface_url):
    debug(1)

    video_url = parse_interface(interface_url, url)
    plugin.set_resolved_url(video_url)


@plugin.route('/playseri/<url>')
def playseri(url):
    url=main_url+url

    video_list = []
    items = []

    source = get_page(url)
    numList = Beautiful(source, "div.numList ul li a")
    # 得到该页面所有的视频连接
    for c in numList:
        video_list.append((c["title"], main_url + c["href"].encode("utf-8")))

    # 添加kodi播放列表
    for v in video_list:
        interface_url = Beautiful(get_page(v[1]), "iframe")[0].attrs["src"]
        uuu = urlparse.urlsplit(interface_url)
        path = plugin.url_for('play', url= v[1],interface_url=interface_url)
        items.append({'label': v[0]+"[%s]"%uuu.hostname, 'path': path,"is_playable":True})
    return  items

@plugin.route('/video_list/<id>/<pageNum>/<hot>/<lang>/')
def video_list(id,pageNum,hot,lang):

    if hot=="NULL":
        hot=""
    if lang=="NULL":
        lang=""

    items = []
    full_url = "http://ljs.6621173.cn/index.php?m=vod-list-id-%s-pg-%s-order--by-%s-class--year--letter--area-%s-lang-.html" \
               % (id,pageNum, hot, lang)
    source = get_page(full_url)



    for soup in  Beautiful(source,"a.item-link"):
        items.append({
            'label':  soup.attrs["title"],
            'path': plugin.url_for('playseri',url=soup.attrs["href"]),
            "thumbnail":soup.select(".item-pic")[0].attrs["data-echo"]
        })


    if hot=="":
        hot="NULL"
    if lang=="":
        lang="NULL"

    items.append({
        'label': "下一页",
        'path': plugin.url_for('video_list',  id=id, pageNum=str(int(pageNum)+1),hot=hot, lang=lang),
    })
    return  items
@plugin.route('/recent_video/<url>')
def recent_video(url):
    debug(0)
    try:
        source = get_page(url)
    except Exception as e:
        pass

    items = []

    for soup in  Beautiful(source,"a.item-link"):
        items.append({
            'label':  soup.attrs["title"],
            'path': plugin.url_for('playseri',url=soup.attrs["href"]),
            "thumbnail":soup.select(".item-pic")[0].attrs["data-echo"]
        })

    return items
@plugin.route('/video_type/<id>')
def video_type(id):
    items = []
    url = "http://ljs.6621173.cn/?m=vod-type-id-%s.html"%(int(id)+1)
    path = plugin.url_for('recent_video',url=url )
    items.append({'label': "最近更新", 'path': path})

    for i in a[int(id)]:
        path = plugin.url_for('video_list',id=i["id"], pageNum=pageNum,hot=hot,lang=lang)
        items.append({'label':i["title"], 'path': path})
    return items


@plugin.route('/category/<tid>')
def category(tid):
    items = []
    for c in Category:
        path = plugin.url_for('video_type', id=c["id"])
        items.append({'label': c['title'], 'path': path})
    return  items

@plugin.route('/')
def root():

    items = [
        {'label': u'视频分类', 'path': plugin.url_for('category', tid = '0')},
    ]
    return items

def main(argv):
    plugin.run(True)

if __name__ == '__main__':
    main(sys.argv[2][1:])