# -*- coding: utf-8 -*-
from mod_pywebsocket import msgutil
import redis
import time
import logging

_GOODBYE_MESSAGE = '___ImDoneWithIt___'

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

def web_socket_transfer_data(request):
    lastmsg = ''
    r = redis.Redis()
    while True:
        #recv = msgutil.receive_message(request)
        #if (recv == _GOODBYE_MESSAGE):
        #    return
            
        messages = r.lrange('msgs',0,9)
        
        try:
            lastindex = messages.index(lastmsg)
            logging.info (lastindex)
            for i in xrange(0,lastindex):
                msgutil.send_message(request, messages[i])
                time.sleep(0.2)
        except ValueError:
            # client has not received anything at all or new connect
            for msg in messages[::-1]:
                msgutil.send_message(request, msg)
                time.sleep(0.2)

        lastmsg = messages[0]
