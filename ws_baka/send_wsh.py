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
from socket import *
import redis
import time

host = "localhost"
port = 31337
buf = 1024
addr = (host,port)
max_msg_size = 300

def web_socket_do_extra_handshake(request):
    pass  # Always accept.

def web_socket_transfer_data(request):
    # request.connection.remote_ip
    UDPSock = socket(AF_INET,SOCK_DGRAM)
    r = redis.Redis()
    while True:
        data = msgutil.receive_message(request)
        data = data.replace ('<','&lt;').replace('>','&gt;')[:max_msg_size]
        message = '%s|user%s' % (time.time(), data)
        r.push ('msgs',message,head=True)
        if (message.find('@baka ') > 0):
            # send a copy to bokkabot
            UDPSock.sendto(message,addr)
        
    UDPSock.close()