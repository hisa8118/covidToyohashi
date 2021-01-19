import pandas as pd
import numpy as np
#1/18 695
url = 'https://www.city.toyohashi.lg.jp/41805.htm'
dfs = pd.read_html(url)
# %% フォーマットの違いを調整
# 感染者データのみ読み込み
lis = [df for df in dfs if(len(df.columns) > 5)]
# dfALL = pd.concat(lis, ignore_index=True)
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
        if(lis[i].values[1][0] == id):
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
dfMain4[0] = tmp[0]
dfMain4[1] = tmp[2]
dfMain4[2] = tmp[3]
dfMain4[3] = pd.Series()
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
dfOut = dfOut[dfOut["年代"] != "年代"]
dfOut = dfOut[dfOut["患者例"] != "患者例"]
dfOut["患者例"] = dfOut["患者例"].astype('uint')
# dfOut['発症日'] = dfOut[['患者例','発症日']].apply(lambda x: adjustDate(*x), axis = 1)
dfOut['採取日'] = dfOut[['患者例','採取日']].apply(lambda x: adjustDate(*x), axis = 1)
dfOut = dfOut.sort_values(by="患者例",ascending=False)
# %%xport All
dfOut.to_excel('dist/dataAll.xlsx', index=False)