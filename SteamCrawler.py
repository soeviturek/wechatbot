#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import bs4
import csv 
import pandas as pd


url = "https://store.steampowered.com/app/1061880/Conan_Chop_Chop/"


def get_more_like_this_url(url,soup):
    content = soup.select('div[class="right"]')
    murl= ""
    for c in content:
        m_url = c.find('a')
        m_url = m_url['href']
    return m_url.split('?')[0]
def get_from_morelike_url(m_url,soup,level):
    res = requests.get(m_url)
    soup = bs4.BeautifulSoup(res.text)
    contents = soup.select('div[class="recommendation_area_ctn similar_grid_ctn similar_grid_flex"]')
#     game_names = []
    game_urls = []
    morelike_urls = []
    finall = []
    for c in contents: #4个大block,每个块
#         print(c)
        #找出所有大板块里的href
        atags = c.find_all('a')
        l = [atags[i:i + 2] for i in range(0, len(atags), 2)] #拆分成2pairs
#         print('length of l:',len(l))
        for i in l:
            f = []
            game_url = i[0]['href']
            game_url = game_url.split('?')
            game_urls.append(game_url[0])
            game_name = game_url[0].split('/')[5]
            
            morelikev2_url = i[1]['href']
#             print(morelikev2_url)
#             print(game_url)
            morelike_urls.append(morelikev2_url.split('?')[0])
            
            f.append(level)
            f.append(game_name)
            f.append(game_url[0])
            finall.append(f)
    return finall, morelike_urls

def start_request(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    
    #获取0级游戏的more like this url
    m_url = get_more_like_this_url(url,soup)
    print("0 more like this see all: ",m_url)
    
    #go to url，获取所有1级相关游戏的url
    finall_v1, morelike_urls_v2 = get_from_morelike_url(m_url,soup,'1')
    #finall_v1 = [[1,ada,33333]]
    
    #从more like this界面中遍历出所有2级推荐游戏
    for i in morelike_urls_v2:
        finall, morelike_urls_v3 = get_from_morelike_url(i,soup,'2')
        #[[2,ada,3333],[2,ada,3232131]]
        for j in finall:
            finall_v1.append(j)
      
        
    return finall_v1

# l = start_request(url)

# print(l)
# field names 
fields = ['Level', 'Name', 'Url'] 

# name of csv file 
filename = "morelike.csv"
    
# writing to csv file 
with open(filename, 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields)    
    # writing the data rows 
    csvwriter.writerows(l)


df = pd.read_csv('morelike.csv')
print(df.shape)
df.head(30)


# df.drop_duplicates(subset=['Name'],inplace=True)
# df.shape

df.to_csv('morelike.csv',index=False,)
file_data = open('morelike.csv', 'rb').read()
open('morelike.csv', 'wb').write(file_data[:-2])




