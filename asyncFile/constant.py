BASE_URL = 'http://104.194.212.10/forum/'
URL_POSTFIX = 'forum-58-'
URL_LIST = []
itemUrlList_JsonArray = []
PAGES = 2
FILES_NAME = 'downloads/files'
FILES_IMAGE_NAME = 'downloads/images'
ITEM_URL_LIST_PATH = FILES_NAME + '/itemUrlList.json'
for i in range(PAGES):
    url = BASE_URL + URL_POSTFIX + str(i) + '.html'
    URL_LIST.append(url)