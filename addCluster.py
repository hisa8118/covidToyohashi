# %% Excel
import pandas as pd

cl1 = "環境部収集業務課"
cl2 = "高齢者施設"
cl3 = "市内医療機関"

df = pd.read_csv('ClusterInfo.csv')
df2= pd.read_excel('dist/dataAll.xls')

# 列の値を比較
#  = (df2["患者例"] == df[cl1])
df2[cl1] = df2["患者例"].isin(df[cl1])
df2[cl2] = df2["患者例"].isin(df[cl2])
df2[cl3] = df2["患者例"].isin(df[cl3])
df2.to_excel('dist/dataAll.xls', index=False)