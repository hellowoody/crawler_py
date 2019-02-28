# -*- coding: utf-8 -*-
import normal.constant as constant
import normal.utils as utils
import json
import multiprocessing
import time

def getList():
    print('aaa')
    for url in constant.URL_LIST:
        try:
            soup = utils.getContentSoup(url)
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

def downloadImages(itemUrl,soupContent):
    imgList = soupContent.select('div.t_msgfont > img ')
    utils.mkdir(constant.FILES_IMAGE_NAME)
    for i in imgList:
        imgSrc = i['src']
        if imgSrc.startswith('http'):
            utils.downloadImage(i['src'],constant.FILES_IMAGE_NAME,itemUrl['name'])

def downloadTorrents(itemUrl,soupContent):
    torrentUrlList = soupContent.select('dl.t_attachlist > dt > a ')
    for i in torrentUrlList:
        if i['href'].startswith('attachment.php?'):
            torrentPageUrl = constant.BASE_URL + i['href']
            soup = utils.getContentSoup(torrentPageUrl)
            torrentUrl = constant.BASE_URL + soup.select_one('a[class="btn btn-danger"]')['href']
            utils.downloadFile(torrentUrl,constant.FILES_NAME,itemUrl['name']+'.torrent')


def crawlItem(i,l):
    l.acquire()
    print('aaa')
    itemUrl = constant.itemUrlList_JsonArray[i]
    soup = utils.getContentSoup(itemUrl['url'])
    downloadImages(itemUrl, soup)
    downloadTorrents(itemUrl, soup)
    l.release()

def main():
    startTime = time.time()
    getList()
    print('waiting...')
    l = multiprocessing.Lock()  # 定义一个进程锁
    for i in range(len(constant.itemUrlList_JsonArray)):
        process = multiprocessing.Process(target=crawlItem, args=(i,l))
        process.start()
    print('finished')
    endTime = time.time()
    print("total time:", endTime - startTime)

if __name__=="__main__":
    print('this is multiprocessing version.')
    main()