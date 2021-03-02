from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re
from sys import getsizeof
import time
from threading import Thread
import threading


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def getPoemsLinks():
    linksFile = open("links.txt", "r+")
    firstLine = linksFile.readline()
    if firstLine:
        return list(map(lambda x: x[:-1], file.readlines()))

    url = 'http://stih.su' 
    resp = urlopen(url) # скачиваем файл
    html = resp.read().decode('utf8') # считываем содержимое
    soup = BeautifulSoup(html, 'html.parser') # делаем суп

    alphabet_div = soup.find("div", {"class": "alphabet_content"})

    alphabet_links = list(alphabet_div.find_all("a"))
    authors_lst = [a.attrs['href'] for a in alphabet_links]

    for i in range(len(authors_lst)):
        if authors_lst[i].startswith("http"):
            authors_lst = authors_lst[:i]
            break

    poems_links = []
    for author in authors_lst:#[0:2]:
        resp = urlopen(url+author) 
        html = resp.read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')

        poems_div = soup.find('ol', {'class': 'number-navi all'}) 
        poems_tags = list(poems_div.find_all("a"))
        links = [a.attrs['href'] for a in poems_tags]
        poems_links += links  

    return poems_links


def getPoem(poem_link):
    resp = urlopen(poem_link)
    html = resp.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    poem_title = soup.find('h1', {'class': 'entry-title'})
    poem_title = poem_title.next_element

    poem = soup.find('div', {'class': 'entry-content'})
    poem_lines = list(poem)[3:-1]
    poem_lines = [re.sub(r"<p>|<br\/>|<\/p>", "", str(l)) for l in poem_lines]

    return (poem_title, poem_lines)


def savePoem(poem_title, poem_lines, poemsPath):
    poem_title = re.sub("[:*?\"<>|]", "", poem_title)
    poem_title = poem_title[:64] if len(poem_title) > 64 else poem_title
    path = f'{poemsPath}/{poem_title}.txt'
    with open(path, 'w', encoding='utf8') as file:
        for string in poem_lines:
            file.write(string + '\n')



def getPoems(poems_links):
    global count
    for link in poems_links:
        poem = getPoem(link)
        poem_title = poem[0]
        poem_lines = poem[1]
        poems_path = "poemsData"
        savePoem(poem_title, poem_lines, poems_path)
        count += 1
        printProgressBar(count, linksNum, prefix = 'Progress:', suffix = 'Complete', length = 50)


count = 1
poems_links = getPoemsLinks()
linksNum = len(poems_links)
print(linksNum)
threadsNumber = 4
start_time = time.time()
printProgressBar(0, linksNum, prefix = 'Progress:', suffix = 'Complete', length = 50)
for links in chunks(poems_links, len(poems_links)//threadsNumber):
    th = Thread(target=getPoems, args=(links, ))
    th.start()


while True:
    if threading.active_count() == 1:
        print("--- %s seconds ---" % (time.time() - start_time))
        break

