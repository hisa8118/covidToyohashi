
from numpy.lib.function_base import append
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.city.toyohashi.lg.jp/41805.htm'
dfs = pd.read_html(url)
# %% Main
# 感染者データのみ読み込み
lis = [df for df in dfs if(len(df.columns) > 5)]
index = 0
dfa = lis[0]
# %% Main
# 感染者データのみ読み込み
for df in lis:
    print("listIndex",index)
    index +=1
    print(df.head(2))
 # %% Soup
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
# %% 発表日
datelist = []
for element in soup.find_all("h5"):
    # print(element.text)
    s = element.text
    match = re.split("[ |（|(|・|~|～|例目|（|発]", s)
    # print(match)
    l = []
    for x in match:
        if "月" in x:
            dd = x.translate(s.maketrans({'月':'/','日':''}))
            y = "2021/" if (len(l) > 1 and l[0] > 441) else "2020/"
            l.append(y+dd)
        try:
            l.append(int(x))
        except:
            pass
    
    # print(l)
    if(len(l) > 1): datelist.append(l)
datelist
index = 0
for i1 in datelist:
    lis[index].insert(0,"発表日",i1[-1])
    index += 1
# %%
