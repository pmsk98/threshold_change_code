# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:21:57 2021

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:51:26 2021

@author: user
"""

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    


for i in range(0,73):
    print(test_2019[i]['pred_voting'].value_counts())

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        


for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()




#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)



gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})


gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
            
            
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2018
result2 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2019
result3 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)


gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2020
result4 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_decsion.csv',encoding='euc-kr')


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_decsion.csv',encoding='euc-kr')


# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:51:26 2021

@author: user
"""

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()



#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_gbm.csv',encoding='euc-kr')



test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_gbm.csv',encoding='euc-kr')


# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:51:26 2021

@author: user
"""

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()



#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_knn.csv',encoding='euc-kr')




test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_knn.csv',encoding='euc-kr')



test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]
#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()



#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_logistic.csv',encoding='euc-kr')


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})


#2017_2
result5 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_logistic.csv',encoding='euc-kr')




test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()




#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_naive.csv',encoding='euc-kr')


# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:11:10 2021

@author: user
"""

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_naive.csv',encoding='euc-kr')



test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]
#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()




#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]
s
for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_neural.csv',encoding='euc-kr')



# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:11:10 2021

@author: user
"""

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]


#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)


gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass




win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_neural.csv',encoding='euc-kr')




test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()




#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)



gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]
#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_randomforest.csv',encoding='euc-kr')



test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass
win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_randomforest.csv',encoding='euc-kr')




test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2016')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred[i]
    test_2019[i]['pred_decision']=pred_decision[i]
    test_2019[i]['pred_naive']=pred_naive[i]
    test_2019[i]['pred_randomforest']=pred_randomforest[i]
    test_2019[i]['pred_svm']=pred_svm[i]
    test_2019[i]['pred_knn']=pred_knn[i]
    test_2019[i]['pred_neural']=pred_neural[i]
    test_2019[i]['pred_voting']=pred_voting[i]
    test_2019[i]['pred_gbm']=pred_gbm[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        else:
            print(i)

        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
 
    
#키움증권 수수료 적용 0.015%
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        



for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()




#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2016')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})


gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2016
result =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


##############################################################2017
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_1[i]
    test_2019[i]['pred_decision']=pred_decision_1[i]
    test_2019[i]['pred_naive']=pred_naive_1[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_1[i]
    test_2019[i]['pred_svm']=pred_svm_1[i]
    test_2019[i]['pred_knn']=pred_knn_1[i]
    test_2019[i]['pred_neural']=pred_neural_1[i]
    test_2019[i]['pred_voting']=pred_voting_1[i]
    test_2019[i]['pred_gbm']=pred_gbm_1[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017
result1 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



#######################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_2[i]
    test_2019[i]['pred_decision']=pred_decision_2[i]
    test_2019[i]['pred_naive']=pred_naive_2[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_2[i]
    test_2019[i]['pred_svm']=pred_svm_2[i]
    test_2019[i]['pred_knn']=pred_knn_2[i]
    test_2019[i]['pred_neural']=pred_neural_2[i]
    test_2019[i]['pred_voting']=pred_voting_2[i]
    test_2019[i]['pred_gbm']=pred_gbm_2[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})


gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018
result2 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)




###################################2019

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_3[i]
    test_2019[i]['pred_decision']=pred_decision_3[i]
    test_2019[i]['pred_naive']=pred_naive_3[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_3[i]
    test_2019[i]['pred_svm']=pred_svm_3[i]
    test_2019[i]['pred_knn']=pred_knn_3[i]
    test_2019[i]['pred_neural']=pred_neural_3[i]
    test_2019[i]['pred_voting']=pred_voting_3[i]
    test_2019[i]['pred_gbm']=pred_gbm_3[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019
result3 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


############################2020
test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_4[i]
    test_2019[i]['pred_decision']=pred_decision_4[i]
    test_2019[i]['pred_naive']=pred_naive_4[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_4[i]
    test_2019[i]['pred_svm']=pred_svm_4[i]
    test_2019[i]['pred_knn']=pred_knn_4[i]
    test_2019[i]['pred_neural']=pred_neural_4[i]
    test_2019[i]['pred_voting']=pred_voting_4[i]
    test_2019[i]['pred_gbm']=pred_gbm_4[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    

profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020
result4 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)



final_result=pd.concat([result,result1,result2,result3,result4])


final_result.to_csv('kr_stock_ratio_method1_voting.csv',encoding='euc-kr')




test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2017')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_5[i]
    test_2019[i]['pred_decision']=pred_decision_5[i]
    test_2019[i]['pred_naive']=pred_naive_5[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_5[i]
    test_2019[i]['pred_svm']=pred_svm_5[i]
    test_2019[i]['pred_knn']=pred_knn_5[i]
    test_2019[i]['pred_neural']=pred_neural_5[i]
    test_2019[i]['pred_voting']=pred_voting_5[i]
    test_2019[i]['pred_gbm']=pred_gbm_5[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    
## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass


win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2017')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2017_2
result5 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

##############################################2018

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2018')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_6[i]
    test_2019[i]['pred_decision']=pred_decision_6[i]
    test_2019[i]['pred_naive']=pred_naive_6[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_6[i]
    test_2019[i]['pred_svm']=pred_svm_6[i]
    test_2019[i]['pred_knn']=pred_knn_6[i]
    test_2019[i]['pred_neural']=pred_neural_6[i]
    test_2019[i]['pred_voting']=pred_voting_6[i]
    test_2019[i]['pred_gbm']=pred_gbm_6[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2018')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2018_2
result6 = pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


#################################################2019


test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2019')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_7[i]
    test_2019[i]['pred_decision']=pred_decision_7[i]
    test_2019[i]['pred_naive']=pred_naive_7[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_7[i]
    test_2019[i]['pred_svm']=pred_svm_7[i]
    test_2019[i]['pred_knn']=pred_knn_7[i]
    test_2019[i]['pred_neural']=pred_neural_7[i]
    test_2019[i]['pred_voting']=pred_voting_7[i]
    test_2019[i]['pred_gbm']=pred_gbm_7[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)

gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass



win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2019')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})

gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2019_2
result7 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)

#######################################################2020

test_2019=[]

for i in range(0,73):    
    test_19=df[i]['Date'].str.contains('2020')
    test_2019.append(df[i][test_19])
    


for i in range(0,73):
    test_2019[i]['pred']=pred_8[i]
    test_2019[i]['pred_decision']=pred_decision_8[i]
    test_2019[i]['pred_naive']=pred_naive_8[i]
    test_2019[i]['pred_randomforest']=pred_randomforest_8[i]
    test_2019[i]['pred_svm']=pred_svm_8[i]
    test_2019[i]['pred_knn']=pred_knn_8[i]
    test_2019[i]['pred_neural']=pred_neural_8[i]
    test_2019[i]['pred_voting']=pred_voting_8[i]
    test_2019[i]['pred_gbm']=pred_gbm_8[i]
    

#pred 자료형 변경
for i in range(0,73):
    test_2019[i]['pred']=test_2019[i]['pred'].astype('float')
    test_2019[i]['pred_decision']=test_2019[i]['pred_decision'].astype('float')
    test_2019[i]['pred_naive']=test_2019[i]['pred_naive'].astype('float')
    test_2019[i]['pred_randomforest']=test_2019[i]['pred_randomforest'].astype('float')
    test_2019[i]['pred_svm']=test_2019[i]['pred_svm'].astype('float')
    test_2019[i]['pred_knn']=test_2019[i]['pred_knn'].astype('float')
    test_2019[i]['pred_neural']=test_2019[i]['pred_neural'].astype('float')
    test_2019[i]['pred_voting']=test_2019[i]['pred_voting'].astype('float')
    test_2019[i]['pred_gbm']=test_2019[i]['pred_gbm'].astype('float')
    
    

## new position
position = []
for e in range(0,73):
    for i, p in enumerate(test_2019[e]['pred']):
        if i == 0:
            position.append('buy')
        else:
            if (position[-1] == 'buy' or position[-1] == 'holding'):
                if p != -1:
                    position.append('holding')
                else:
                    position.append('sell')
            elif p == 1:
                position.append('buy')
            else:
                position.append('no action')


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

position = list_chunk(position, 246)


for i in range(0,73):
    test_2019[i]['position']=None


for i in range(0,73):
    test_2019[i]['position']=position[i]

#첫날 position이 holding일 경우 buy로 변경
for i in range(0,73):
    if test_2019[i]['position'][test_2019[i].index[1]]=='holding':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    elif test_2019[i]['position'][test_2019[i].index[1]]=='sell':
        test_2019[i]['position'][test_2019[i].index[1]]='buy'
    else:
        print(i)


#강제 청산
for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='holding':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='buy':
            test_2019[i]['position'][e]='sell'
        elif test_2019[i]['position'][e]=='no action':
            test_2019[i]['position'][e]='sell'
        else:
            print(i)



for i in range(0,73):
    test_2019[i]['profit']=None
    
#다음날 수정 종가를 가져오게 생성
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            elif test_2019[i]['position'][e]=='sell':
                test_2019[i]['profit'][e]=test_2019[i]['Close'][e+1]
            else:
                print(i)
        except:
            pass



for i in range(0,73):
    for e in test_2019[i].index[-1:]:
        if test_2019[i]['position'][e]=='sell':
            test_2019[i]['profit'][e]=test_2019[i]['Close'][e]
        
####

buy_label=[]
for i in range(0,73):
    buy_position=test_2019[i]['position']=='buy'
    buy_label.append(test_2019[i][buy_position])
    
sell_label=[]
for i in range(0,73):
    sell_position=test_2019[i]['position']=='sell'
    sell_label.append(test_2019[i][sell_position])    


buy=[]
sell=[]
for i in range(0,73):
    buy.append(buy_label[i]['Close'].reset_index(drop=True))
    sell.append(sell_label[i]['Close'].reset_index(drop=True))
    
  
profit_2=[]    
for i in range(0,73):
    profit_2.append((sell[i]-(0.0015*sell[i]))-buy[i])
  

for i in range(0,73):
    test_2019[i]['profit_2']=None
    

#profit 결측치 처리
for i in range(0,73):
    profit_2[i]=profit_2[i].dropna()
    
    
#profit_2 sell에 해당하는 행에 값 넣기
for tb, pf in zip(test_2019, profit_2):
    total_idx = tb[tb['position'] == 'sell'].index
    total_pf_idx = pf.index
    for idx, pf_idx in zip(total_idx, total_pf_idx):
        tb.loc[idx, 'profit_2'] = pf[pf_idx]
        

for i in range(0,73):
    test_2019[i]['profit_cumsum']=None
    
    
    

#profit 누적 합 
for i in range(0,73):
    for e in test_2019[i].index:
        try:
            if test_2019[i]['position'][e]=='holding':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='no action':
                test_2019[i]['profit_2'][e]=0
            elif test_2019[i]['position'][e]=='buy':
                test_2019[i]['profit_2'][e]=0
            else:
                print(i)
        except:
            pass


#새로운 청산 기준 누적합

for i in range(0,73):
    test_2019[i]['profit_cumsum2']=None    
    
    
for i in range(0,73):
    test_2019[i]['profit_cumsum']=test_2019[i]['profit_2'].cumsum()


#############################ratio 작성

#ratio 작성
for i in range(0,73):
    profit_2[i]=pd.DataFrame(profit_2[i])

#거래횟수
trade= []

for i in range(0,73):
    trade.append(len(profit_2[i]))
    
#승률


for i in range(0,73):
    profit_2[i]['average']=None

   
for i in range(0,73):
    for e in range(len(profit_2[i])):      
        if profit_2[i]['Close'][e] > 0:
            profit_2[i]['average'][e]='gain'
        else:
            profit_2[i]['average'][e]='loss'
            
for i in range(0,73):
    for e in range(len(profit_2[i])):
        if profit_2[i]['Close'][e] < 0:
            profit_2[i]['Close'][e]=profit_2[i]['Close'][e] * -1
        else:
            print(i)
gain_no=[]
loss_no=[]
gain_cumsum=[]
loss_cumsum=[]



for i in range(0,73):
    try:
        gain_no.append(profit_2[i].groupby('average').size()[0])
        loss_no.append(profit_2[i].groupby('average').size()[1])
        gain_cumsum.append(profit_2[i].groupby('average').sum()['Close'][0])
        loss_cumsum.append(profit_2[i].groupby('average').sum()['Close'][1])
    except:
        pass




win=[]
for i in range(0,73):
    try:
        win.append(profit_2[i].groupby('average').size()[0]/len(profit_2[i]))
    except:
        win.append('0')
    
#평균 수익

gain=[]

for i in range(0,73):
    gain.append(profit_2[i].groupby('average').mean())
    

real_gain=[]

for i in range(0,73):
    try:
        real_gain.append(gain[i]['Close'][0])
    except:
        real_gain.append('0')



#평균 손실
loss=[]

for i in range(0,73):
    try:
        loss.append(gain[i]['Close'][1])
    except:
        loss.append('0')

    
loss
#payoff ratio
payoff=[]

for i in range(0,73):
    try:
        payoff.append(gain[i]['Close'][0]/gain[i]['Close'][1])
    except:
        payoff.append('inf')
    
#profit factor

factor_sum=[]

len(factor_sum)
for i in range(0,73):
    factor_sum.append(profit_2[i].groupby('average').sum())

factor=[]

for i in range(0,73):
    try:
        factor.append(factor_sum[i]['Close'][0]/factor_sum[i]['Close'][1])
    except:
        factor.append('0')

#year
year=[]

for i in range(0,73):
    year.append('2020')

#최종 결과물 파일 작성
stock_name=pd.DataFrame({'stock_name':file_list})

stock_name=stock_name.replace('.csv','',regex=True)

year=pd.DataFrame({'year':year})

trade=pd.DataFrame({'No.trades':trade})

win=pd.DataFrame({'Win%':win})

real_gain=pd.DataFrame({'Average gain($)':real_gain})

loss=pd.DataFrame({'Average loss($)':loss})

payoff=pd.DataFrame({'Payoff ratio':payoff})

factor=pd.DataFrame({'Profit factor':factor})
gain_number=pd.DataFrame({'gain_no':gain_no})

loss_number=pd.DataFrame({'loss_no':loss_no})

total_gain =pd.DataFrame({'total_gain':gain_cumsum})

total_loss=pd.DataFrame({'total_loss':loss_cumsum})

#2020_2
result8 =pd.concat([year,stock_name,trade,win,real_gain,loss,payoff,factor,gain_number,loss_number,total_gain,total_loss],axis=1)


final_result2=pd.concat([result,result5,result6,result7,result8])


final_result2.to_csv('kr_stock_ratio_method2_voting.csv',encoding='euc-kr')





























