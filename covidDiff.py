import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import re
import io
import upload
# -------------------------------------
# ID:1001 2/2以降のデータを抽出して出力
# -------------------------------------
#感染者データIDをもつリストを検索
def findIndex(id:int,lis:list):
    id = str(id)
    i = 0
    for l in lis:
        if(lis[i].values[1][1] == id):
            return i
            break
        i +=1
# 患者IDの欠損チェック
def checkdata(d:DataFrame):
    print("checkData---")
    d = d.sort_values(by="患者例",ascending=True)
    dd = d.reset_index()
    i2 = 1
    for i1 in dd["患者例"]:
        if(i1 != i2+1000): print(i1,i2+1000)
        i2 +=1
    print("end")
    return dd 
# -------------------------------------
# MIAN
# -------------------------------------
url = 'https://www.city.toyohashi.lg.jp/41805.htm'
lis = pd.read_html(url,match="患者例")
# %% Soup
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
# %% 発表日の抽出
datelist = []
for element in soup.find_all("h5"):
    s = element.text
    match = re.split("[ |（|(|・|~|～|例目|（|発]", s)
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
    if(len(l) > 1): datelist.append(l)
#2/1 id 1001以降のデータを抽出
index = 0
for i1 in datelist:
    lis[index].insert(0,"発表日",i1[-1])
    index += 1
    if(i1[-1] == "2021/２/１"): break
lis[-1].insert(0,"発表日","")
dfMain = pd.concat(lis[:findIndex(1001,lis)+1])
#todo クラスター情報の自動抽出 
#%% ##採取日の整形
dfOut = pd.concat([dfMain],ignore_index=True)
dfOut.columns = dfOut.loc[0]
dfOut.rename(columns={dfOut.columns[0]:"発表日"},inplace=True) 
dfOut = dfOut[dfOut["年代"] != "年代"]
dfOut = dfOut[dfOut["患者例"] != "患者例"]
dfOut = dfOut.dropna(subset=["患者例"])
dfOut["患者例"] = dfOut["患者例"].astype('uint64')
dfOut = dfOut.sort_values(by="患者例",ascending=False)
# %% クラスター情報の追加
# df = pd.read_csv('data/cluster.csv')
url="https://script.google.com/macros/s/AKfycbz1udVFxPqvT4-kQb4M-7yx6zjXugS02vj5aZ7Cmzuc1yFW22FQoJLGPg/exec"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))
df = df.fillna(0).astype(np.int64)
cl = df.columns
for st in cl:
    dfOut.loc[dfOut["患者例"].isin(df[st]),"クラスタ"] = st
# %%xport All
# dfOut.to_excel('data/test_dataAll.xls', index=False)
# dfOut.to_csv('data/test_dataAll.csv', index=False)
buf = dfOut.to_csv(index=False)
upload.uploadCsv(buf)
dd = checkdata(dfOut)