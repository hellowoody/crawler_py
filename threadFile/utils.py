# -*- coding: utf-8 -*-
import os
import requests
from urllib import request
from bs4 import BeautifulSoup

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('create path :',path)

def downloadImage(url,path,name):
    suffix = url.split('.')[-1]
    filepath = os.path.join(str(path),str(name+'.'+suffix))
    downloadFromHttp(url,filepath)

def downloadFile(url,path,name):
    filepath = os.path.join(str(path),str(name))
    downloadFromHttp(url,filepath)

def downloadFromHttp(url,filepath):
    opener = request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    request.install_opener(opener)
    request.urlretrieve(url, filename=filepath)

def getContentSoup(url):
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    return soup
