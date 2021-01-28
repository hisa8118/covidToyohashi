# %% main
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import re
import io

# %%  感染者データのみ読み込み
url = 'https://www.city.toyohashi.lg.jp/41805.htm'
dfs = pd.read_html(url)
lis = [df for df in dfs if(len(df.columns) > 5)]
# dfALL = pd.concat(lis, ignore_index=True)
 # %% Soup
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
# %% 発表日
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
datelist
index = 0
for i1 in datelist:
    lis[index].insert(0,"発表日",i1[-1])
    index += 1
lis[-1].insert(0,"発表日","")
def adjustData(adf: pd.DataFrame):
    adf = adf.drop(8,axis=1)
    adf[4] = adf[4].replace({'抗原':'','PCR':''},regex=True)
    adf[1] = adf[1].replace({'（日本国籍）':'','（外国籍）':''},regex=True)
    return adf
#感染者データIDをもつリストを検索
def findIndex(id:int):
    id = str(id)
    i = 0
    for l in lis:
        if(lis[i].values[1][1] == id):
            return i
            break
        i +=1
# Format4 From 460  221
dfMain = pd.concat(lis[:findIndex(460)])
# Format3 From 421 - 460 45
dfMain2 = pd.concat(lis[findIndex(460):findIndex(421)])
dfMain2 = adjustData(dfMain2)
# Format2 From 281 - 421 162
dfMain3 = pd.concat(lis[findIndex(421):findIndex(280)])
dfMain3 = adjustData(dfMain3)
#%% Format1  From 1 - 280
tmp = pd.concat(lis[findIndex(280):])
dfMain4 = pd.DataFrame()
#%% ##データの整形
def aDate(s:str):
    if("月" in s):
        s = "2020/" + s.translate(s.maketrans({'月':'/','日':''}))
        s = s.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    return s
# 280よりまえは発表日に陽性判明日を仕様
dfMain4["発表日"] = tmp[1].replace({'令和２年':''},regex=True).apply(lambda x : aDate(x))
dfMain4[0] = tmp[0]
dfMain4[1] = tmp[2]
dfMain4[2] = tmp[3]
dfMain4[3] = pd.Series()
# dfMain4[4] = dfMain4["発表日"] 
dfMain4[4] = tmp[1].replace({'令和２年':''},regex=True)

#%% ##データの整形
def adjustDate(id,s:str):
    if(type(s) != str): return
    if("月" in s or "/" in s):
        if(id > 456 or id == 443 or id == 442):
            s = "2021/" + s
        else:
            s = "2020/" + s
        s = s.translate(s.maketrans({'月':'/','日':''}))
        s = s.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    return s
dfOut = pd.concat([dfMain,dfMain2,dfMain3,dfMain4],ignore_index=True)
dfOut.columns = dfOut.loc[0]
dfOut.rename(columns={dfOut.columns[0]:"発表日"},inplace=True) 
dfOut = dfOut[dfOut["年代"] != "年代"]
dfOut = dfOut[dfOut["患者例"] != "患者例"]
dfOut["患者例"] = dfOut["患者例"].astype('uint')
# dfOut['発症日'] = dfOut[['患者例','発症日']].apply(lambda x: adjustDate(*x), axis = 1)
dfOut['採取日'] = dfOut[['患者例','採取日']].apply(lambda x: adjustDate(*x), axis = 1)
dfOut = dfOut.sort_values(by="患者例",ascending=False)
# %% クラスター情報の追加
# df = pd.read_csv('cluster.csv')
url="https://script.google.com/macros/s/AKfycbz1udVFxPqvT4-kQb4M-7yx6zjXugS02vj5aZ7Cmzuc1yFW22FQoJLGPg/exec"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')))
df = df.fillna(0).astype(np.int64)
cl = df.columns
for st in cl:
     dfOut.loc[dfOut["患者例"].isin(df[st]),"クラスタ"] = st
    # dfOut[st] = dfOut["患者例"].isin(df[st])  
# %%xport All
dfOut.to_excel('data/dataAll.xls', index=False)
dfOut.to_csv('data/dataAll.csv', index=False)
# %% 患者IDの欠損チェック
def checkdata(d:DataFrame):
    print("checkData---")
    d = d.sort_values(by="患者例",ascending=True)
    dd = d.reset_index()
    i2 = 1
    for i1 in dd["患者例"]:
        if(i1 != i2): print(i1,i2)
        i2 +=1
    return dd 
    print("end")
dd = checkdata(dfOut)
# dfOut.iloc[[2,3,5]]# %%
