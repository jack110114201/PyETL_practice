import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('./pttjoke'):
    os.mkdir('./pttjoke')


list = list('[\\/:*?"<>|\r\n.]+')

url = 'https://www.ptt.cc/bbs/joke/index7657.html'

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

headers = {'User-Agent' : UserAgent}


for i in range(0,1): 
    res = requests.get(url, headers = headers)

    soup = BeautifulSoup(res.text,'html.parser')

    ArticleList = soup.select('div.title')
    #print(ArticleList)
    for tag in ArticleList:
        try:
            title = tag.select("a")[0].text
            articleUrl = "https://www.ptt.cc" + tag.select("a")[0]["href"]
            articleRes = requests.get(articleUrl, headers=headers)
            articleResSoup = BeautifulSoup(articleRes.text, 'html.parser')
            textarticleCoent = articleResSoup.select('div[id="main-content"]')[0].text.split('※ 發信站')[0]
            try:
                with open('./pttjoke/{}.txt'.format(title),'w',encoding='utf-8') as f:  #以title命名檔案名稱
                        f.write(articleUrl) #先把網址寫進文章裡
            except OSError:
                for i in list: 
                    title = title.replace(i,"-")  #解決title有非法字元的問題
                with open('./pttjoke/{}.txt'.format(title),'w',encoding='utf-8') as e:
                    e.write(articleUrl)
            try:
                with open('./pttjoke/{}.txt'.format(title),'a',encoding='utf-8') as f:
                        f.write(textarticleCoent)  #再把文章寫進去
            except OSError:
                for i in list:
                    title = title.replace(i,"-")
                with open('./pttjoke/{}.txt'.format(title),'a',encoding='utf-8') as e:
                    e.write(textarticleCoent)            
        except IndexError as e: #文章被刪除，會跑IndexError
            print(tag)
    url_new = "https://www.ptt.cc" + soup.select('a[class="btn wide"]')[1]['href'] #取得上一頁的網址
    url = url_new 




