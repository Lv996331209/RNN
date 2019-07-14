#import keras
import pandas as pd
import numpy as np
# from keras.models import load_model
# from keras.models import Sequential
# from keras.layers import Activation, Dense
# from keras.layers import LSTM
# from keras.layers import Dropout
from matplotlib.font_manager import FontManager, FontProperties
def getChineseFont():
    return FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
def cal_rr(y0, y):#计算拟合优度
    sstot = 0
    ave = np.mean(y)
    for i in y:
        sstot = sstot + (i - ave) ** 2
    ssreg = 0
    for i in y0:
        ssreg = ssreg + (i - ave) ** 2
    ssres = 0
    for i in range(len(y0)):
        ssres = ssres + (y[i] - y0[i]) ** 2
    r2 = 1 - ssres / sstot
    return r2
# model = load_model("model.h5")
real=pd.read_csv('real.csv')
predict=pd.read_csv('pred.csv')
real=list(real.iloc[:,1])
predict=list(predict.iloc[:,1])

import matplotlib.pyplot as plt
plt.plot(real,color='#4169E1')#绘制测试集实际曲线
plt.plot(predict,color='#FA8072')#绘制测试集拟合曲线

r2=cal_rr(real,predict)#计算拟合优度
plt.xlabel('Dates')#X轴为日期
plt.ylabel('Price')#Y轴为当天股票价格
plt.title('Stock Price Prediction on Test Set ',fontsize=16)#绘制图表标题
#输出拟合优度数值即准确率
plt.text(-2,105,s='准确率'+str(round(r2,3)),fontproperties=getChineseFont())
plt.legend(['Actual', 'Predicted'])#绘制图例
plt.grid(color='grey', linestyle=':', linewidth=1,alpha=0.3)#绘制背景网格
plt.show()#绘制图表



