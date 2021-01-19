
import pandas as pd

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
