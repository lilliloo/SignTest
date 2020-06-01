# -*- coding: utf-8 -*-
"""
Created on Sat May 30 22:34:44 2020

@author: lilliloo
"""

#------------------------------ #
#符号検定
# ----------------------------- #
import numpy as np
import pandas as pd
# ----------------------------- #
 
# ------ Function ------ #

#logデータの読み込み
#符号付け
#z値の計算

def Add_sign(table):
    sign = []
    #+:1 -:0
    for i in range(len(table)):
        if   (int(table.iloc[i, 0]) > int(table.iloc[i, 1])):
            sign.append("+")
        elif (int(table.iloc[i, 0]) < int(table.iloc[i, 1])):
            sign.append("-")
        elif (int(table.iloc[i, 0]) == int(table.iloc[i, 1])):
            sign.append("0")
    table = pd.concat([table, pd.Series(sign)], axis = 1)
    table = table.rename(columns = {6:"Proposer", 7:"Responder", 0:"sign"})
    return table

def Count(table):
    n_posi, n_nega = 0, 0
    for i in range(len(table)):
        if (table.iloc[i, 2] == "+"):
            n_posi += 1
        elif(table.iloc[i, 2] == "-"):
            n_nega += 1
    n_n = n_posi + n_nega
    return [n_n, n_posi, n_nega]

def get_p(z):
    z = str(z)
    z_row = float(z[0] + z[1] + z[2])
    z_column = float("0.0" + z[3])
    z_distribution = pd.read_csv(path_z + "z_distribution.csv", header = None)
    
    for i in range(len(z_distribution)):
        if(z_distribution.iloc[i,0] == z_row):
            index_row = i
    for j in range(len(z_distribution.columns)):
        if(z_distribution.iloc[0,j] == z_column):
            index_column = j
    p = z_distribution.iloc[index_row, index_column]  * 2
    return p

def Result(stat):
    print("N : " + str(stat[0]),"r : " + str(stat[1]), 
          "Ur : " + str(stat[2]), "σr : " + str(stat[3]),
          "z-value : " + str(stat[4]),
          "p-value : " + str(stat[5]),sep = "\n")


#------------------------------ #

path_z = "C:/Users/lilliloo/Documents/Laboratry/Hyperscanning/Behavior/SignTest/"
path_input="C:/Users/lilliloo/Documents/Laboratry/Hyperscanning/Behavior/Analysis_Data/"
##FB
#dyad_list=['MYOMYF191028','FMGFHT191028','MSTMYA191108',
#           'MSMMHM191111','MKOMYO191113','MKYMTO191111','MROMTF191212']
#FF
dyad_list=['MRNMDU191019','MNTMTW191026','MSOMKK191104',
           'MYKMTA191104','FTIFMT191113','MYTMYF191109','FRSFSY191113']

# -------------------------------- #
#各ペアごとの符号データ
sign_data = pd.DataFrame(index = [], columns = ["N", "n+", "n-"])
#
#
## -------------------------------- #

# 全ペアのデータを符号付け
for i in range(len(dyad_list)):
    df = pd.read_csv(path_input+dyad_list[i]+".csv",header=None)
    # 獲得金額の列を抽出
    table = df.iloc[1:,6:]
    table = table.reset_index(drop = True)
    # Add sign
    table_sign = Add_sign(table)
    # Add each dyad sign-data
    record = pd.Series(Count(table_sign), index = sign_data.columns)
    sign_data = sign_data.append(record, ignore_index=True)
dyad = pd.Series(["Dyad1","Dyad2","Dyad3","Dyad4","Dyad5","Dyad6","Dyad7"])
sign_data = pd.concat([dyad,sign_data], axis = 1)
sign_data = sign_data.set_index(0)
# 符号検定
sum_n_n = sum(sign_data.iloc[:, 0])    
sum_n_posi = sum(sign_data.iloc[:, 1])    
sum_n_nega = sum(sign_data.iloc[:, 2])
if sum_n_posi > sum_n_nega:
    r = sum_n_nega
else:
    r = sum_n_posi
U_r = sum_n_n / 2
lamda_r = np.sqrt(sum_n_n) / 2
z = abs((r + 0.5 - U_r) / lamda_r)
#標準正規分布表からp値
p = get_p(z)
#結果の表示
stat_data = [sum_n_n, r, U_r, lamda_r, z, p]
Result(stat_data)
