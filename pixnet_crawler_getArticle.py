#!/usr/bin/env python
# coding: utf-8

# ### pixnet get Article

# In[3]:


import requests
from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# In[33]:
df = pd.read_csv("Pinex_bytags.csv")
df = df.iloc[:,1:]
df


# In[42]:
article_urls = df["article_url_list"].tolist()
article_urls


# In[44]:
article_urls = set(article_urls)



# In[48]:
def get_Article(urls):
    for i in urls:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        r = session.get(i)
        #r = requests.get(i)
        r.encoding='utf-8'
        html_str = r.text
        soup = BeautifulSoup(html_str)
        time.sleep(2)
        try:
            article_title_2nd = [i.text.strip() for i in soup.select(".title")]
            article_content = [i.text for i in soup.select(".article-content")]
        except:
            print("notfound: "+ [i])
        return article_title_2nd, article_content



# In[49]:
article_title_2nd_list = []
article_content_list = []
article_url_list_2nd = []

for i in article_urls:
    if i =='article_url_list':
        print('its article_url_list')
    else:
        article_title_2nd, article_content = get_Article([i])
        article_title_2nd_list.extend([article_title_2nd])
        article_content_list.extend([article_content])
        article_url_list_2nd.extend([i])


# In[31]:
df2 = pd.DataFrame()
df2["article_url_list"] = article_url_list_2nd
# df2["article_title"] = article_title_2nd_list
df2["article_content"] = article_content_list
df2


# In[32]:
result = pd.merge(df, df2, on='article_url_list')
result


# In[28]:
result.to_csv(r'articles.csv', mode='a', encoding='utf_8_sig')

