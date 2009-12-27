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

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

def web_socket_transfer_data(request):
    remote_ip = request.connection.get_remote_addr()[0]
    r = redis.Redis()
    count = r.get('nickcount')
    
    if count==None:
        count = 0

    r.set('nickcount',count)
    uid = r.get (remote_ip)
    
    if uid==None:
        uid = count + 1
        r.set ('nickcount', uid)
        r.set (remote_ip, uid)

    r.save()
    msgutil.send_message(request, str(uid))
