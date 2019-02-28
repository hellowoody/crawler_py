# -*- coding: utf-8 -*-
import asyncFile.constant as constant
import asyncFile.utils as utils
import concurrent.futures as cf
import requests
import json
import asyncio
import time
from bs4 import BeautifulSoup

loop = asyncio.get_event_loop()

def getList():
    for url in constant.URL_LIST:
        try:
            response = requests.get(url)
            content = response.content
            soup = BeautifulSoup(content, "html.parser",from_encoding="gbk")
            itemUrlList = soup.select('tbody > tr > th.new > span > a')
            itemUrlList2 = soup.select('tbody > tr > th.content > span > a')
            if len(itemUrlList2) > 0:
                itemUrlList.append(itemUrlList2)
            constant.itemUrlList_JsonArray = []
            for itemUrl in itemUrlList:
                itemUrlList_Json = {}
                itemUrlList_Json['url'] = constant.BASE_URL + itemUrl['href']
                itemUrlList_Json['name'] = itemUrl.text
                itemUrlList_Json['done'] = 'false'
                constant.itemUrlList_JsonArray.append(itemUrlList_Json)
            utils.mkdir(constant.FILES_NAME)
            with open(constant.ITEM_URL_LIST_PATH, 'w') as f:
                f.write(json.dumps(constant.itemUrlList_JsonArray,ensure_ascii=False))   #ensure_ascii=False 中文转码
            print('itemUrlList.json lines:',len(constant.itemUrlList_JsonArray))
        except Exception as e:
            print('getList error:',e)

def downloadImages(itemUrl):
    response = requests.get(itemUrl['url'])
    content = response.content
    soup = BeautifulSoup(content,"html.parser")
    imgList = soup.select('div.t_msgfont > img ')
    utils.mkdir(constant.FILES_IMAGE_NAME)
    for i in imgList:
        imgSrc = i['src']
        if imgSrc.startswith('http'):
            print(i)
            utils.downloadFile(i['src'],constant.FILES_IMAGE_NAME,itemUrl['name'])
            print('aaa')

def downloadTorrents(itemUrl):
    pass

async def downloadImagesAsync():
    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        futures = (loop.run_in_executor(executor,downloadImages,itemUrl) for itemUrl in constant.itemUrlList_JsonArray)
        for result in await asyncio.gather(*futures):
            pass

def crawlItem():
    t1 = time.time()
    loop.run_until_complete(downloadImagesAsync())
    loop.close()
    print("Async total time:", time.time() - t1)

def main():
    getList()
    crawlItem()

if __name__=="__main__":
    print('this is async version.')
    main()