# -*- coding: utf-8 -*-
'''
Sun Dec 27 12:10:13 IST 2009             Abhishek Mishra <ideamonk at gmail.com>
                       ____        __         ____        __
                      / __ )____ _/ /______ _/ __ )____  / /_
                     / __  / __ `/ //_/ __ `/ __  / __ \/ __/
                    / /_/ / /_/ / ,< / /_/ / /_/ / /_/ / /_
                   /_____/\__,_/_/|_|\__,_/_____/\____/\__/ 
'''

from mod_pywebsocket import msgutil
import redis
import time
import logging

timeout = 600
__KillerWords__ = '__ImDoneWithIt__'

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

def web_socket_transfer_data(request):
    lastmsg = ''
    r = redis.Redis()
    timelim = time.time() + timeout
    
    while True:
        #words = msgutil.receive_message(request)
        #if words == __KillerWords__:
        #    break
            
        # get last 10 messages
        messages = r.lrange('msgs',0,9)
        try:
            # give remaining messages from buffer
            lastindex = messages.index(lastmsg)
            if (lastindex>0):
                timelim = time.time() + timeout
                for i in xrange(0,lastindex):
                    msgutil.send_message(request,
                                    messages[lastindex - i -1].split('|',1)[1])
        except ValueError:
            # client has not received anything at all, give the whole buffer
            for msg in messages[::-1]:
                msgutil.send_message(request, msg.split('|',1)[1])
            timelim = time.time() + timeout
            
        lastmsg = messages[0]

        if (time.time() > timelim):
            print "A receive timedout"
            r.disconnect()
            break