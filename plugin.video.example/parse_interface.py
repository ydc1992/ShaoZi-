#coding:utf-8
import urllib2
import re
import urlparse
import json
import urllib

class interface:
    def __init__(self,interface,referurl):
        self.interface = interface
        self.referurl =referurl

    def checkInterface(self):
        if "10087" in self.interface:
            video_url= eval("self.parse_10087")()
        elif "tangzhi" in self.interface:
            video_url = eval("self.parse_tangzi")()
        elif "zz22x" in self.interface:
            video_url = eval("self.parse_zz22x")()
        else:
            video_url = None
        return  video_url

    def parse_10087(self):
        send_header={
            "Host": "jx.10087.tv",
            "Referer":self.referurl
        }
        req = urllib2.Request(self.interface, headers=send_header)
        try:
            response = urllib2.urlopen(req).read()
        except Exception as e:
            pass
        video_url = re.findall("var video=\['(.*?)'];", response, re.S)[0]
        return video_url

    def  parse_tangzi(self):
        return self.interface


    def parse_zz22x(self):
        # 请求接口网址
        send_header = {
            "Host": "jvip.zz22x.com",
            "Referer": self.referurl
        }
        req = urllib2.Request(self.interface, headers=send_header)
        response = urllib2.urlopen(req).read()

        # 第一次跳转，拿到对应的post参数
        url_1 = re.findall("src=\"(.*?)\"", response, re.S)[0]
        uuu = urlparse.urlsplit(url_1)
        send_header = {
            "Host": uuu.hostname,
            "Referer": self.interface
        }

        req = urllib2.Request(url_1, headers=send_header)
        response = urllib2.urlopen(req).read()

        json = re.findall("\.post\(\"play\.php\", (\{.*?\})", response, re.S)[0]

        try:
            c = eval(json)
        except Exception as e:
            json = re.sub("pd1", "\"\"", json)
            c = eval(json)

        c["url"]=self.interface
        # 得到真实地址
        postData=urllib.urlencode(c)
        req = urllib2.Request(uuu.scheme+"://"+ uuu.hostname+"/vip/play.php", data=postData)
        response = urllib2.urlopen(req, data=postData).read()

        pass



