# -*- coding: utf-8 -*-

import sys
from video.porn_91 import *
from video.common import *
from video.ttmj import *

_handle = int(sys.argv[1])
_url = sys.argv[0]


Category = \
[
    { "title":"91porn","home_url":"http://91porn.com/v.php?category=long&viewtype=basic","call_back":"start_91"},
    { "title":"天天美剧","home_url":"http://www.msj1.com","call_back":"start_ttmj"}
]


@plugin.route('/')
def root():
    items = []
    for c in Category:
        path = plugin.url_for(c["call_back"],home_url=c['home_url'],label= c['title'])
        items.append({'label': c['title'], 'path': path})
    return items

def main(argv):
    plugin.run(True)

if __name__ == '__main__':
    main(sys.argv[2][1:])