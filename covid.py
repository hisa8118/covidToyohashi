import pandas as pd
import numpy as np

url = 'https://www.city.toyohashi.lg.jp/41805.htm'
dfs = pd.read_html(url)
# %% Main
# 感染者データのみ読み込み
lis = [df for df in dfs if(len(df.columns) > 5)]
# col = lis[0].loc[0]
# dfALL = pd.concat(lis, ignore_index=True)
##検体採取日から検証方法を削除
def adjustData(adf: pd.DataFrame):
    adf = adf.drop(8,axis=1)
    adf[4] = adf[4].replace({'抗原':'','PCR':''},regex=True)
    adf[1] = adf[1].replace({'（日本国籍）':'','（外国籍）':''},regex=True)
    return adf

#
##フォーマットの違いを調整
# Format4 From 460  221
dfMain = pd.concat(lis[:13])
# Format3 From 421 - 460 45
dfMain2 = pd.concat(lis[13:19])
dfMain2 = adjustData(dfMain2)
# Format2 From 285 - 460 162
dfMain3 = pd.concat(lis[19:43])
dfMain3 = adjustData(dfMain3)
#%% Format1  From 1 - 285
tmp = pd.concat(lis[43:])
dfMain4 = pd.DataFrame()
dfMain4[0] = tmp[0]
dfMain4[1] = tmp[2]
dfMain4[2] = tmp[3]
dfMain4[3] = pd.Series()
dfMain4[4] = tmp[1].replace({'令和２年':''},regex=True)

#%% ##書き出し
def adjustDate(id,s:str):
    if(type(s) != str): return
    # print(s,("月" in s or "/" in s ),id)
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