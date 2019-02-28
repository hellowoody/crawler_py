# -*- coding: utf-8 -*-
import os
from urllib import request
from bs4 import BeautifulSoup

BASE_URL = 'http://104.194.212.10/forum/'
path = 'files222'

def mkdir(p):
    folder = os.path.exists(p)
    if not folder:
        os.makedirs(p)
        print('create n folder !')


def crawl(url,name):
    opener = request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    request.install_opener(opener)
    request.urlretrieve(url,filename=name)

def main():
    files = os.listdir(path)
    torrents = os.listdir(path+'/full')

    for file in files:
        path_tmp = os.path.join(path,file)
        if os.path.isfile(path_tmp):
            for i in torrents:
                if i[:10] == file[:10] :
                    torrentFilePath = os.path.join(path+'/full/'+i)
                    with open(torrentFilePath,'rb') as f :
                        content = f.read()
                        soup = BeautifulSoup(content,"html.parser")
                        torrentUrl = BASE_URL+soup.select_one('a[class="btn btn-danger"]')['href']
                        mkdir(os.path.join(path+'/n'))
                        crawl(torrentUrl,os.path.join(path+'/n/'+i))

if __name__ == '__main__':
    main()