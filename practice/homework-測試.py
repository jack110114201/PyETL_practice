#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import bs4
import csv
import random,time
import os



if not os.path.exists('./104file'):
    os.mkdir('./104file')

url_A ='https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E6%95%B8%E6%93%9A%E5%88%86%E6%9E%90%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=12&asc=0&'


url_B = '&mode=s&jobsource=keyword2Keyword'

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
headers = {'User-Agent' : userAgent}
    

my_params = {'ro':'1', # 限定全職的工作，如果不限定則輸入0
             'keyword':'資料科學', # 想要查詢的關鍵字
             'area':'6001001000', # 限定在台北的工作
             'isnew':'30', # 只要最近一個月有更新的過的職缺
             'mode':'l'} # 清單的瀏覽模式
    

all_job_datas=[]
for page in range(1,19+1):
    url = url_A+str(page)+url_B
    print(url)
    htmlFile = requests.get(url,headers=headers,data=my_params)
    ObjSoup=bs4.BeautifulSoup(htmlFile.text,'html.parser')
    jobs = ObjSoup.find_all('article',class_='js-job-item')                 #搜尋所有職缺  
       
    for job in jobs:
        job_name=job.find('a',class_="js-job-link").text                    #職缺內容
        job_content=job.find('p',class_='job-list-item__info').text.split('\n')        #工作內容
        job_company=job.get('data-cust-name')                               #公司名稱
        job_loc_ALL=job.find('ul', class_='job-list-intro').findAll('li')
        for i in job_loc_ALL:
            job_loc = job_loc_ALL[0].text  #地址
            work_year = job_loc_ALL[1].text #工作經歷
            education = job_loc_ALL[2].text #學歷
        job_pay=job.find('span',class_='b-tag--default').text               #薪資
        job_url=job.find('a').get('href')[2:]                                   #網址
        job_data={'公司名稱':job_company,'職缺內容':job_name, '工作內容':job_content,
                         '地址':job_loc,'工作經歷':work_year,'學歷':education,'薪資':job_pay,'網址':job_url}
        all_job_datas.append(job_data)
        print(job_name)
        print(job_content)
        print(job_company)
        print(job_loc)
        print(work_year)
        print(education)
        print(job_pay)
        print(job_url)
        #print(job_data)
        print('========================================================')

    time.sleep(random.randint(1,3))
             
fn='104測試.csv'                                             #取CSV檔名
columns_name=['公司名稱','職缺內容','工作內容','地址','工作經歷','學歷','薪資','網址']                     #第一欄的名稱
with open(fn,'w',newline='',encoding='utf_8_sig') as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile,fieldnames=columns_name)            #定義寫入器
    dictWriter.writeheader()       
    for data in all_job_datas:
        dictWriter.writerow(data)              
                
                
import pandas as pd

df = pd.read_csv('./104測試.csv')
df.columns = columns_name
df 

