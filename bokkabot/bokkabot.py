#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
log = logging.getLogger ("Bokkabot")
log.setLevel(logging.INFO)

log.info ("Connecting to Redis Server...")
r = redis.Redis()
log.info ("Binding Bokkabot on %s:%s" % addr)
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

log.info ("Bootstrapping Bokka's brain from bokkabot.brn")
k = aiml.Kernel()
if os.path.isfile("bokkabot.brn"):
    k.bootstrap(brainFile = "bokkabot.brn")
else:
    print "Bokka couldn't find its brain - bokkabot.brn"
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
                            'bokka',
                            ' @%s %s' % (nick, k.respond(msg))
                            )
        r.push ('msgs',response,tail=True)
