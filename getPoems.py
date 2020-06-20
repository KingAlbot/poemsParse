from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re


url = 'http://stih.su/' 
resp = urlopen(url) # скачиваем файл
html = resp.read().decode('utf8') # считываем содержимое
soup = BeautifulSoup(html, 'html.parser') # делаем суп

alphabet_div = soup.find("div", {"class": "alphabet_content"})

alhabet_links = list(alphabet_div.find_all("a"))
authors_lst = [a.attrs['href'] for a in alphabet_links]

for i in range(len(authors_lst)):
    if authors_lst[i].startswith("http"):
        authors_lst = authors_lst[:i]
        break


for author in authors_lst:
    resp = urlopen(url+author) 
    html = resp.read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    poems =  
    
print(links_lst)



