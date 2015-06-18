#!/usr/bin/env python

#05/29/2015 test success
#named start/stop/reload
#06/01/2015 
#add:amend named start/stop/reload is class Znamed

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from commands import *
from tornado.options import define, options
import dns.resolver
import json

define("port", default=8000, help="run on the given port", type=int)


#class
class Znamed:
  def start_named(self):
    (status, output) = getstatusoutput('/opt/named/sbin/named')
    obj = {status:output}	
    jsobj = json.dumps(obj)
    return jsobj

  def stop_named(self):
    (status, output) = getstatusoutput('ps -ef | grep named')
    output = output + '\n'  #deal last line
    count = output.count('\n')
    for item in range(count):
      br = output.index('\n')
      line = output[:br].split()
      getstatusoutput('kill -9 %s' % line[1])
      output = output[br+1:]
    (status, output) = getstatusoutput('ps -ef | grep named')
    obj = {status:output}	
    jsobj = json.dumps(obj)
    return jsobj

  def reload_named(self):
    (status, output) = getstatusoutput('/opt/named/sbin/rndc reload')
    obj = {status:output}	
    jsobj = json.dumps(obj)
    return jsobj


class Zdns:
  def dns_res(self, ipaddr):
    answers = dns.resolver.query(ipaddr)
    for rdata in answers:
      print 'rdata=', rdata
  

class Application(tornado.web.Application):
#**customize
  def __init__(self):
    handlers = [
      (r"/", Nothing),
      (r"/dnsapi/(\w+)", MainHandler),

    ]
#customize**#
    settings = dict(
      cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      autoescape=None,
      )
    tornado.web.Application.__init__(self, handlers, **settings)

#**customize
class Nothing(tornado.web.RequestHandler):
  def get(self):   
    pass
  def post(self,input):
    pass

class MainHandler(tornado.web.RequestHandler):
  def get(self,input): 
    zt = Znamed()
    if "start" == input:
      rec = zt.start_named()
      self.write(rec)
    if "stop" == input:
      rec = zt.stop_named()
      self.write(rec)
    if "reload" == input:
      rec = zt.reload_named()
      self.write(rec)
    if "dig" == input[:3]:
      self.write(input)
      

  def post(self,input):
    pass

#customize**#


def main():
  tornado.options.parse_command_line()
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
  main()
