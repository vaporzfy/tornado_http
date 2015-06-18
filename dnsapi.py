#!/usr/bin/env python

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

define("port", default=8000, help="run on the given port", type=int)


#function
def z_start_named():
  getstatus('cd /opt/named/sbin')
  (status, output) = getstatusoutput('named')

def z_stop_named():
  (status, output) = getstatusoutput('ps -ef | grep named')
  output = output + '\n'  #deal last line
  count = output.count('\n')
  for item in range(count):
    br = output.index('\n')
    line = output[:br].split()
    getstatusoutput('kill -9 %s'%line[1])
    output = output[br+1:]


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
        if "start" == input:
          z_start_named()
          self.write("run")
        if "stop" == input:
          z_stop_named()
          self.write("stop")

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
