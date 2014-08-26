#!/usr/bin/python
# coding:utf8

from plugins import BasePlugin
from bs4 import BeautifulSoup
import urllib2

class FetchTitle():
    def __init__(self):
        self.url = 'http://www.google.com'
    def trimemptyline( old_string ):
        line,new_string = '',''
        for line in old_string.split('\n'):
            if line.strip() == '': continue
            new_string += line + ' '
        print new_string
        return new_string
    
    def chkurl( url ):
        url = url.strip()
        return url.startswith('https://') or url.startswith('http://')
    
    
    def getHtmlTitle(self, url, callback ):
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36 LBBROWSER')
        opener = urllib2.build_opener()
        opener.addheaders = [headers]
        req = opener.open(url).read()
        
        soup = BeautifulSoup(req)
        title = soup.title.string
        callback( trimemptyline(title) )


class fetchtitlePlugin(BasePlugin):
    title = None
    def is_match(self, from_uin, content, type):
        if content.startswith("-t"):
            self.url = content.split(" ")[1]
            self._format = u"\n {0}" if type == "g" else u"{0}"
            if self.title is None:
                self.title = FetchTitle()
            return True
        return False


    def handle_message(self, callback):
        self.title.getHtmlTitle(self.url, callback)
 
