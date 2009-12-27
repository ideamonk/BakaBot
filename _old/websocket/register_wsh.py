# -*- coding: utf-8 -*-
from mod_pywebsocket import msgutil
import redis

_GOODBYE_MESSAGE = '___ImDoneWithIt___'

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

def web_socket_transfer_data(request):
    r = redis.Redis()
    while True:
        nick = msgutil.receive_message(request)
        if (nick == _GOODBYE_MESSAGE):
            return
            
        present_nicks = r.lrange('regs',0,-1)
        
        try:
            present_nicks.index(nick)
            msgutil.send_message(request, "gtfo")
        except ValueError:
            r.push ('regs',nick)
            msgutil.send_message(request, nick)
