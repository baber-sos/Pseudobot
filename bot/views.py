# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from subprocess import Popen, PIPE
from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import string, random
import datab
import json

sessionRequests = {};

def generate_random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))



def index(request):
    resp = FileResponse(open(os.getcwd() + '/bot/frontend/index.html', 'rb'))
        
    cookies = request.COOKIES
    if ('id' not in cookies):
        resp.set_cookie('id',generate_random_string())
    print cookies
    return resp

def query(request):

    cookies = request.COOKIES
    print cookies
    session_id = ''
    if 'id' in cookies:
        session_id = cookies['id']
    params = request.GET
    print session_id
    q =""
    try:
        #accessToken ko as command line argument bhej diya hua, wahan recieve kr k shit kr lena agey
        q = params['query']
        assistant = params['ass']
        accessToken = params['token']
        userEmail = params['emailId']
    except:
        return HttpResponse("")

    datab.update(session_id,q, 0)

    p = Popen(['python', 'botlogic.py',q, assistant, accessToken, userEmail, session_id], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    print err
    if rc > 0:
        return HttpResponse("There was a problem with the server...")
    datab.update(session_id,output, 1)
    return HttpResponse(output)

def chat(request):
    cookies = request.COOKIES;
    cookieId = '';
    if 'id' in cookies:
        cookieId = cookies['id'];
    respData = datab.read(cookieId);
    return HttpResponse(json.dumps(respData), content_type="application/json");

def logo(request):
    return FileResponse(open(os.getcwd() + '/bot/frontend/logo.png', 'rb'))

def css(request):
    return FileResponse(open(os.getcwd() + '/bot/frontend/index.css', 'rb'))
