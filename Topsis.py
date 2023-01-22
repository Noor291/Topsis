import numpy as np
import pandas as pd
import sys
import os
  

def topsis(data,w,impacts):
    data1=pd.read_csv(data)
    df=data1.copy(deep=True)
    output=data1.copy(deep=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    ncol=len(df.columns)
    n=np.size(df)
    nrow=int(n/ncol)
    rss=[]
    #root of sum of squares
    for j in range(0,ncol):
        ans=0
        for i in range(0,nrow):
            h=df.iloc[i][j]
            ans=ans+np.square(h)
        rss.append(np.sqrt(ans))
    #dividing these
    for i in range(0,nrow):
        for j in range(0,ncol):
            df.iloc[i][j]=float(df.iloc[i][j])/float(rss[j]) 
    #assigning weights
    for i in range(0,nrow):
        for j in range(0,ncol):
            df.iloc[i][j]=float(df.iloc[i][j])*float(w[j])
    
    #max min values
    max_val=df.max().values
    min_val=df.min().values
    
    #arranging with impacts
    for i in range(0,ncol):
        if impacts[i]=='-':
            max_val[i],min_val[i]=min_val[i],max_val[i]
    #calculating euclidean dist
    sp=[]
    sn=[]
    for i in range(0,nrow):
        sum1=0
        sum2=0
        for j in range(0,ncol):
            sum1=sum1+np.square(df.iloc[i][j]-max_val[j])
            sum2=sum2+np.square(df.iloc[i][j]-min_val[j])
        sp.append(np.sqrt(sum1))
        sn.append(np.sqrt(sum2))
    
    #performance measure
    p=[]
    for i in range(0,nrow):
        p.append(float(sn[i])/float(sn[i]+sp[i]))

    output['Score']=p
    output['Rank']=output['Score'].rank(ascending=False).astype(int)
    return output

