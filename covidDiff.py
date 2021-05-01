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
    print("checkData--------")
    d = d.sort_values(by="患者例",ascending=True)
    dd = d.reset_index()
    i2 = 1
    for i1 in dd["患者例"]:
        if(i1 != i2+1000): print(i1,i2+1000)
        i2 +=1
    print("check null data--------")
    print(dfOut.info())
    print("end")
    return dd 
# -------------------------------------
# MIAN
# -------------------------------------
url = 'https://www.city.toyohashi.lg.jp/41805.htm'
lis = pd.read_html(url,match="患者例")
print(lis)
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
            y = "2021/"
            l.append(y+dd)
        try:
            l.append(int(x))
        except:
            pass
    if(len(l) > 1): datelist.append(l)
#2/12 仕様フォーマット変更によりアルゴリズム変更
index = 0
for i1 in datelist:
    lis[index].insert(0,"発表日",i1[-1])
    index += 1
# dfMain = pd.concat(lis)
# dfMain = pd.concat(lis).dropna(how="any")  # 欠損値があれば行削除
dfMain = pd.concat(lis).dropna(thresh=3, axis=1) # 欠損値3以上の列を削除する
#%% ##採取日の整形
dfOut = pd.concat([dfMain],ignore_index=True)
dfOut.columns = dfOut.loc[0]
dfOut.rename(columns={dfOut.columns[0]:"発表日"},inplace=True) 
dfOut = dfOut[dfOut["年代"] != "年代"]
dfOut = dfOut[dfOut["患者例"] != "患者例"]
dfOut = dfOut.dropna(subset=["患者例"])
dfOut["患者例"] = dfOut["患者例"].astype('uint64')
dfOut = dfOut.sort_values(by="患者例",ascending=False)
# %%xport All
# dfOut.to_excel('data/test_dataAll.xls', index=False)
# dfOut.to_csv('data/test_dataAll.csv', index=False)
buf = dfOut.to_csv(index=False)
upload.uploadCsv(buf)
dd = checkdata(dfOut)