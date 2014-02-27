#!/usr/bin/env python
# -*- coding=utf-8 -*-

import cherrypy 

class web(object):
    @cherrypy.expose
    def index(self):
        return '''
            <html>
            <body style="background-color: #FFDAB9;">
            <head><title> welcome to Sean's blog</title>
            <p>this is the home page</p>
            <form action="greetuser" method="POST">
            What is your name?
            <input type="text" name="name" />
            <input type="submit" />
            </form>
            </head>
            </body>
            <html>
            '''
    @cherrypy.expose
    def greetuser(self,name=None):
        if name:
            return "hello %s ,what's up " %name
        else:
            return '''Please enter your name 
                <body style="background-color: #FFDAB9;">
                <a href='./'>here</a>.
                </body>
                '''

cherrypy.config.update({'server.socket_host':'192.168.6.168',
                        'server.socket_port':80})
#cherrypy.config.update('./cherry.conf')
cherrypy.quickstart(web())


