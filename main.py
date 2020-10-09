import requests
from bs4 import BeautifulSoup
import pandas as pd

book_name = list()

base_url = 'https://tw.manhuagui.com/list/'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

def comicfinder(soup):
  books = soup.find('div', class_="book-list")
  booklist = books.select("ul", class_="contList")
  for b in booklist:
    comics = b.find_all('li')
    for comic in comics:
      hrefs = comic.find_all('a')
      for href in hrefs:
        if href.has_attr('class') and href['class'][0] == 'bcover':
          comic_name = href.get('title')
          book_name.append(comic_name)
          print(comic_name)


data = {'漫畫': book_name}
dataframe = pd.DataFrame(data = data)
dataframe.to_csv("comics.csv", index=False, sep=',')