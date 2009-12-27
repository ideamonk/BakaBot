# -*- coding: utf-8 -*-
# BrainMaker for BokkaBot 0.1                              ideamonk at gmail.com

# Based on - http://ravispeaks.wordpress.com/2009/09/16/diy-omegle-chat-bot
# which is based on the PyAIML and liberally uses code from PyOmegle
# PyAMIL:http://pyaiml.sourceforge.net/
# PyOmegle:http://code.google.com/p/pyomegle/

import aiml
import os

k = aiml.Kernel()

homedir=os.getcwd()
# You can get the AAA files from
#   http://aitools.org/Free_AIML_sets#Annotated_A.L.I.C.E
os.chdir('./aaa')
list=os.listdir('./');
for item in list:
    k.learn(item)
k.setPredicate("name","BokkaBot")
k.setPredicate("master","ideamonk")
os.chdir(homedir)
k.saveBrain("bokkabot.brn")