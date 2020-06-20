from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re

def souper():
    pass

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
for author in authors_lst[0:2]:
    resp = urlopen(url+author) 
    html = resp.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    poems_div = soup.find('ol', {'class': 'number-navi all'}) 
    poems_tags = list(poems_div.find_all("a"))
    links = [a.attrs['href'] for a in poems_tags]
    poems_links += links

count = 1
poems_path = "poemsData"
for poem_link in poems_links:
    resp = urlopen(poem_link)
    html = resp.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    poem_title = soup.find('h1', {'class': 'entry-title'})
    poem_title = poem_title.next_element
    print(f'{count}:', poem_title)

    poem = soup.find('div', {'class': 'entry-content'})
    poem_lines = list(poem)[3:-1]

    poemsPath = "poemsData"
    path = f'{poemsPath}/{poem_title}.txt'
    with open(path, 'w', encoding='utf8') as file:
        for l in poem_lines:
            string = re.sub(r"<p>|<br\/>|<\/p>", "", str(l))
            file.write(string+'\n')
    count += 1 
