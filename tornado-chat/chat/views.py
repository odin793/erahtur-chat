# _*_ coding: utf-8 _*_;

from django.template import RequestContext
from django.conf import settings
from hashlib import sha256
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
import time 
import tornado.web
from django_tornado.decorator import asynchronous

#
#
#
class Channel(object) :
    def __init__(self) :
        self._messages = []
        self._callbacks = []

    def message(self, type, nick, text="") :
        m = { 'type': type, 'timestamp' : int(time.time()), 'text' : text, 'nick' : nick }

        for cb in self._callbacks :
            cb([m])
        self._callbacks = []

        self._messages.append(m)
        if len(self._messages) > 20:
            self._messages.remove(self._messages[0])

    def query(self, cb, since) :
        msgs = [m for m in self._messages if m['timestamp'] > since]
        if msgs :
            return cb(msgs)
        self._callbacks.append(cb)

    def size(self) :
        return 1024

channel = Channel()

class Session(object) :
    SESSIONS = {}
    CUR_ID  = 100

    def __init__(self, nick) :
        for v in self.SESSIONS.values() :
            if v.nick == nick : # user didn't logout correctly 
                # delete old user's session
                Session.remove(str(v.id))                
        self.nick = nick 
        Session.CUR_ID += 1
        self.id   = Session.CUR_ID 

        Session.SESSIONS[str(self.id)] = self # create new one

    def poke(self) :
        pass

    @classmethod
    def who(cls) :
        return [ s.nick for s in Session.SESSIONS.values() ]

    @classmethod
    def get(cls, id) :
        return Session.SESSIONS.get(str(id), None)

    @classmethod
    def remove(cls, id) :
        if id in cls.SESSIONS :
            del Session.SESSIONS[id]

#
#
#
class ChatResponseError(HttpResponse) :
    def __init__(self, message) :
        super(ChatResponseError, self).__init__(status=400, content=json.dumps({ 'error' : message }))

class ChatResponse(HttpResponse) :
    def __init__(self, data) :
        super(ChatResponse, self).__init__(content=json.dumps(data))

#
#
#
def index(request) :
    if request.method == "POST":
        #where_from = request.META.get('HTTP_REFERER', '')
        nickname = request.POST.get('nickname', '')
        request_chat_auth_token = request.POST.get('chat_auth_token', '')
        local_chat_auth_token = sha256(settings.SECRET_KEY + ":" + nickname).hexdigest()
        if request_chat_auth_token != local_chat_auth_token:
            #return ChatResponseError("Bad nickname")
            nickname = ''
    else: 
        nickname = ''
    return render_to_response('chat/index.html', {
        'nickname': nickname,
    })

def clientjs(request) :
    return render_to_response('chat/client.js')

def join(request) :
    nick = request.GET['nick']

    if not nick :
        return ChatResponseError("Bad nickname")

    try :
        session = Session(nick)
    except Exception, e:
        return ChatResponseError("Nickname in use")
        

    channel.message('join', nick, "%s joined" % nick)

    return ChatResponse({ 
                    'id' : session.id,
                    'nick': session.nick,
                    'rss': channel.size(), 
                    'starttime': int(time.time())*1000, # 1000 converts sec to mses for js's Date() class
            })

def part(request) :
    id = request.GET['id']

    session = Session.get(id)
    if not session :
        return ChatResponseError('session expired')

    channel.message('part', session.nick)

    Session.remove(id)
    
    return ChatResponse({ 'rss': 0 })

def send(request) :
    id = request.GET['id']
    session = Session.get(id)
    if not session :
        return ChatResponseError('session expired')

    channel.message('msg', session.nick, request.GET['text'])

    return ChatResponse({ 'rss' : channel.size() })

def who(request) :
    return ChatResponse({ 'nicks': Session.who(), 'rss' : channel.size() })

@asynchronous
def recv(request, handler) :
    response = {}

    if 'since' not in request.GET :
        return ChatResponseError('Must supply since parameter')
    if 'id' not in request.GET :
        return ChatResponseError('Must supply id parameter')

    id = request.GET['id']
    session = Session.get(id)
    if session :
        session.poke()

    since = int(request.GET['since'])

    def on_new_messages(messages) :
        if handler.request.connection.stream.closed():
            return
        handler.finish({ 'messages': messages, 'rss' : channel.size() })

    channel.query(handler.async_callback(on_new_messages), since)
