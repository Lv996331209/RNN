import gc
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ssl

import keras
from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
from keras.layers import Dropout


#tanh作激活函数
activation_function = 'tanh'
#MSE作损失函数，
loss = 'mse'
#'adam'作优化器
optimizer = "adam"
#失活率0.25，防止过拟合
dropout = 0.25
#批处理参数12
batch_size = 12
#迭代次数
epochs = 50
#输入窗口值
window_len = 7
#训练样本占比
training_size = 0.8
#起始时间
merge_date = '2016-01-01'

#数据读取
btc_data=pd.read_csv('data1.0.csv')
btc_data['Date']=pd.to_datetime(btc_data['Date'])

def create_model_data(data):#数据预处理
  data = data[['Date']+[coin+metric for coin in ['APPLE_'] for metric in ['Close','Volume']]]
  data = data.sort_values(by='Date')
  #只保留股票信息的"日期"、"收盘价格"和"成交量"
  return data

#训练集、测试集数据切分
def split_data(data, training_size=0.8):
  #按照8：2的比例将原数据集切分为训练集和测试集
  return data[:int(training_size*len(data))],data[int(training_size*len(data)):]

#创建输入样本
def create_inputs(data, coins=['APPLE'], window_len=window_len):
  #定义一个窗口长度，将输入样本在0和1之间进行归一化
  norm_cols = [coin + metric for coin in coins for metric in ['_Close','_Volume']]
  inputs = []
  for i in range(len(data) - window_len):
    temp_set = data[i:(i + window_len)].copy()
    inputs.append(temp_set)
    for col in norm_cols:
      inputs[i].loc[:, col] = inputs[i].loc[:, col] / inputs[i].loc[:, col].iloc[0] - 1
  return inputs

#创建输出样本
def create_outputs(data, coin, window_len):
  #定义一个窗口长度，将训练集和测试集的目标输出归一化到0~1之间
  return (data[coin + '_Close'][window_len:].values / data[coin + '_Close'][:-window_len].values) - 1

#list转np.array格式
def to_array(data):
  x = [np.array(data[i]) for i in range (len(data))]
  return np.array(x)

#日期与时间戳处理
def date_labels():
    last_date = btc_data.iloc[0, 0]
    date_list = [last_date - datetime.timedelta(days=x) for x in range(len(X_test))]
    return [date.strftime('%m/%d/%Y') for date in date_list][::-1]

#构建LSTM-RNN模型
def build_model(inputs, output_size, neurons, activ_func=activation_function,dropout=dropout, loss=loss, optimizer=optimizer):
  """
  模型中使用3层LSTM，每层512个神经元，然后在每个LSTM层之后有个0.25概率的Dropout层，
  以防止过度拟合（over-fitting）并且每隔一个Dense层产生我们的输出
  """
  model = Sequential()
  model.add(LSTM(neurons, return_sequences=True,input_shape=(inputs.shape[1], inputs.shape[2]), activation=activ_func))
  model.add(Dropout(dropout))
  model.add(LSTM(neurons, return_sequences=True, activation=activ_func))
  model.add(Dropout(dropout))
  model.add(LSTM(neurons, activation=activ_func))
  model.add(Dropout(dropout))
  model.add(Dense(units=output_size))
  model.add(Activation(activ_func))
  model.compile(loss=loss, optimizer=optimizer, metrics=['mae'])
  model.summary()
  return model

if __name__ == '__main__':
    #训练集、测试集划分
    train_set,test_set=split_data(btc_data)
    #训练集、测试集去除索引
    train_set = train_set.drop('Date', 1)
    test_set = test_set.drop('Date', 1)
    #训练集初始化
    X_train = create_inputs(train_set)
    Y_train = create_outputs(train_set, coin='APPLE',window_len=7)
    #测试集初始化
    X_test = create_inputs(test_set)
    Y_test = create_outputs(test_set, coin='APPLE',window_len=7)
    #测试集训练集转为np矩阵
    X_train, X_test = to_array(X_train), to_array(X_test)
    #定义每层512个神经元
    neurons = 512
    #LSTM Memory Cell 初始化
    gc.collect()
    #随机种子初始化
    np.random.seed(202)
    #初始化模型架构
    apple_model = build_model(X_train, output_size=1, neurons=neurons)
    #模型训练
    history = apple_model.fit(X_train, Y_train, epochs=epochs,
                              batch_size=batch_size, verbose=1, validation_data=(X_test, Y_test_btc),
                              shuffle=False)
    #模型训练存储
    apple_model.save('model.h5')



