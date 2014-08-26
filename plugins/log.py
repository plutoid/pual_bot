#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   
#   Desc    :   #  log group msg 
#
import json
import traceback
import os
import config

from plugins import BasePlugin

class LogPlugin(BasePlugin):
    def is_match( self, from_uin, content, type):
        ##if type is 'g' and self['result']['did'] is 1828904153 :
        if type is 'g' :
            print 'self.did: ', self
            #print 'self.nick: ',self.nick
            self.body = content+'\n'
            print 'from_uin: ', from_uin
            print 'content: ', content
            print 'type: ', type
            return True
        return False

    def handle_message( self, callback ):
        f = open("/home/tianhua/pual_bot/log.txt", "a")
        f.write( self.body.encode("utf-8") )
        f.close()
        print self.body.encode("utf-8")

    def read_result(self, resp, callback):
        web = self.is_web
        try:
            result = json.loads(resp.body)
        except ValueError:
            self.logger.warn(traceback.format_exc())
            body = u"error"
        else:
            errorCode = result.get("errorCode")
            if errorCode == 0:
                query = result.get("query")
                r = " ".join(result.get("translation"))
                basic = result.get("basic", {})
                body = u"{0}\n{1}".format(query, r)
                phonetic = basic.get("phonetic")
                if phonetic:
                    ps = phonetic.split(",")
                    if len(ps) == 2:
                        pstr = u"读音: 英 [{0}] 美 [{1}]".format(*ps)
                    else:
                        pstr = u"读音: {0}".format(*ps)
                    body += u"\n" + pstr

                exp = basic.get("explains")
                if exp:
                    body += u"\n其他释义:\n\t{0}".format(u"\n\t".join(exp))

                if web:
                    body += u"\n网络释义:\n"
                    web = result.get("web", [])
                    if web:
                        for w in web:
                            body += u"\t{0}\n".format(w.get("key"))
                            vs = u"\n\t\t".join(w.get("value"))
                            body += u"\t\t{0}\n".format(vs)

            if errorCode == 50:
                body = u"无效的有道key"

        if not body:
            body = u"没有结果"

        callback(body)
