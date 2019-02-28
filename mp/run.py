# -*- coding: utf-8 -*-
import mp.constant as constant
import mp.utils as utils
import json
import multiprocessing
import time

def getList():
    constant.itemUrlList_JsonArray = []
    for url in constant.URL_LIST:
        try:
            soup = utils.getContentSoup(url)
            itemUrlList = soup.select('tbody > tr > th.new > span > a')
            itemUrlList2 = soup.select('tbody > tr > th.content > span > a')
            if len(itemUrlList2) > 0:
                itemUrlList.append(itemUrlList2)
            for itemUrl in itemUrlList:
                itemUrlList_Json = {}
                itemUrlList_Json['url'] = constant.BASE_URL + itemUrl['href']
                text_tmp = itemUrl.text
                text_tmp = text_tmp.replace('【','[').replace('】',']')
                itemUrlList_Json['name'] = text_tmp
                itemUrlList_Json['done'] = False
                constant.itemUrlList_JsonArray.append(itemUrlList_Json)
        except Exception as e:
            print('getList error:',e)
    utils.mkdir(constant.FILES_NAME)
    with open(constant.ITEM_URL_LIST_PATH, 'w') as f:
        f.write(json.dumps(constant.itemUrlList_JsonArray, ensure_ascii=False))  # ensure_ascii=False 中文转码
    print('itemUrlList.json lines:', len(constant.itemUrlList_JsonArray))

def downloadImages(itemUrl):
    soupContent =  utils.getContentSoup(itemUrl['url'])
    imgList = soupContent.select('div.t_msgfont > img ')
    utils.mkdir(constant.FILES_IMAGE_NAME)
    for i in imgList:
        imgSrc = i['src']
        if imgSrc.startswith('http'):
            utils.downloadImage(i['src'],constant.FILES_IMAGE_NAME,itemUrl['name'])

def downloadTorrents(itemUrl):
    soupContent = utils.getContentSoup(itemUrl['url'])
    torrentUrlList = soupContent.select('dl.t_attachlist > dt > a ')
    for i in torrentUrlList:
        if i['href'].startswith('attachment.php?'):
            torrentPageUrl = constant.BASE_URL + i['href']
            soup = utils.getContentSoup(torrentPageUrl)
            torrentUrl = constant.BASE_URL + soup.select_one('a[class="btn btn-danger"]')['href']
            torrentName = itemUrl['name']+'.torrent'
            print(torrentName)
            utils.downloadFile(torrentUrl,constant.FILES_NAME,torrentName)

# def downloadFunc(lock,itemUrl):
#     lock.acquire()
#     downloadImages(itemUrl)
#     downloadTorrents(itemUrl)
#     lock.release()

def downloadFunc(itemUrl):
    downloadImages(itemUrl)
    downloadTorrents(itemUrl)

def crawlItem():
    try:
        coreCount = multiprocessing.cpu_count()
        print('cores : ', coreCount)
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        pool = multiprocessing.Pool(processes=2)
        # partial_downloadFunc = partial(downloadFunc, lock)
        # for itemUrl in constant.itemUrlList_JsonArray:
        #     pool.apply(downloadFunc,args=(lock,itemUrl))
        pool.map(downloadFunc,constant.itemUrlList_JsonArray)
        pool.close()
        pool.join()
    except Exception as e:
        print('crawlItem error : ',e)

def main():
    startTime = time.time()
    getList()
    print('waiting...')
    crawlItem()
    print('finished')
    endTime = time.time()
    print("total time:", endTime - startTime)

if __name__=="__main__":
    print('this is multiprocessing version.')
    main()