from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup


url = 'http://stih.su/' 
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
for author in authors_lst:
    resp = urlopen(url+author) 
    html = resp.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')

    poems_div = soup.find('ol', {'class': 'number-navi all'}) 
    poems_tags = list(poems_div.find_all("a"))
    links = [a.attrs['href'] for a in poems_tags]
    poems_links.append(links)

print(poems_links)



