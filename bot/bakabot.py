#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Sun Dec 27 12:10:13 IST 2009             Abhishek Mishra <ideamonk at gmail.com>
                       ____        __         ____        __
                      / __ )____ _/ /______ _/ __ )____  / /_
                     / __  / __ `/ //_/ __ `/ __  / __ \/ __/
                    / /_/ / /_/ / ,< / /_/ / /_/ / /_/ / /_
                   /_____/\__,_/_/|_|\__,_/_____/\____/\__/ 
'''

from socket import *
import logging
import time
import os

import redis
import aiml

host = "localhost"
port = 31337
buf = 1024
addr = (host,port)

logging.basicConfig()
log = logging.getLogger ("BakaBot ")
log.setLevel(logging.INFO)

log.info ("Connecting to Redis Server...")
r = redis.Redis()
log.info ("Binding BakaBot on %s:%s" % addr)
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

log.info ("Bootstrapping Baka's brain from bakabot.brn")
k = aiml.Kernel()
if os.path.isfile("bakabot.brn"):
    k.bootstrap(brainFile = "bakabot.brn")
else:
    print "Bokka couldn't find its brain - bakabot.brn"
    print "Please run makemeabrain.py"

log.info ("Bokka is ready to talk the talk...")

while True:
    data,addr = UDPSock.recvfrom(buf)
    if not data:
        print "Client has exited!"
        break
    else:
        # data is in format time|nick:msg
        log.info ("Received %s" % data)
        nick, msg = data.split('|',1)[1].split(':',1)
        response = "%s|%s:%s" % (
                            time.time(),
                            'baka',
                            ' @%s %s' % (nick, k.respond(msg.split('@baka',1)[1]))
                            )
        r.push ('msgs',response,head=True)
