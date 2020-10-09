import requests
from bs4 import BeautifulSoup
import pandas as pd
from queue import Queue
import threading
import os
import re

book_name = list()

# base_url = 'https://tw.manhuagui.com/list/'
# response = requests.get(base_url)

# soup = BeautifulSoup(response.text, "html.parser")

def comicfinder(bs):
  books = bs.find('div', class_="book-list")
  booklist = books.select("ul", class_="contList")
  for b in booklist:
    comics = b.find_all('li')
    for comic in comics:
      hrefs = comic.find_all('a')
      for href in hrefs:
        if href.has_attr('class') and href['class'][0] == 'bcover':
          comic_name = href.get('title')
          book_name.append(comic_name)
          # print(comic_name)

def getNextUrl(url,que):
    '''

    :return:
    '''
    if url==None or len(url)==0:
        return

    try:
        html = requests.get(url)
        html.encoding = None
        bs = BeautifulSoup(html.text, 'html.parser')
        #启动一个子线程进行内容处理
        t = threading.Thread(target=comicfinder, args=(bs,))
        t.start()
        t.join()

        new_url = bs.findAll("a", {"class": "prev"})[0].attrs['href']
        new_url= domain_prefix+new_url
        que.put(new_url)
        getNextUrl(new_url,que)
    except Exception as e:
        print("get attr error!")
        print(e)

domain_prefix = r'https://tw.manhuagui.com'
base_url = r'https://tw.manhuagui.com/list/'
html = requests.get(base_url)
html.encoding = None
soup = BeautifulSoup(html.text,'html.parser')

urls=Queue()
getNextUrl(base_url,urls)

data = {'漫畫': book_name}
dataframe = pd.DataFrame(data = data)
dataframe.to_csv("comics.csv", index=False, sep=',')