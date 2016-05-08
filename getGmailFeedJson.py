#!/usr/bin/env python

from urllib.request import FancyURLopener
import feedparser
#import usersettings
import json
import sys
import keyring
import time

def feedToJson(feed):
    if feed==None:
        return "null"

    result={}
    result["unreadCount"]=str(feed["feed"]["fullcount"])
    result["entries"]=[]
    for elem in feed["entries"]:
        tmp={}
        tmp["author"]=  elem["author_detail"]["name"]
        tmp["summary"]= elem["summary"]
        tmp["title"]=   elem["title"]
        for key,item in tmp.items():
            if len(item)>40:
                tmp[key]=item[0:40]+"..."
        tmp["link"]=    elem["link"]
        tmp["time"]=    elem["published"]
        result["entries"].append(tmp)
    return json.dumps(result)

def getFeed(url):
    try:
        opener = FancyURLopener()
        page = opener.open(url)
        contents = page.read().decode('utf-8')
        feed=feedparser.parse(contents)
        return feed
    except:
        return None

def printElemInFeed(feed):
    for elem in feed["entries"]:
        print(elem)
        break

def main():
    username=sys.argv[1]
    try:
        password=keyring.get_password("mailnotifier",username)
        url = 'https://%s:%s@mail.google.com/mail/feed/atom' % (username, password)
        print(feedToJson(getFeed(url)))
    except:
        print("null")

main()
