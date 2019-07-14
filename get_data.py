import pandas as pd
import DateTime
import  time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def get_market_data(market, tag=True):
  """
market: the full name of the cryptocurrency as spelled on coinmarketcap.com.
eg.: 'bitcoin'
tag: eg.: 'btc', if provided it will add a tag to the name of every column.
  returns: panda DataFrame
This function will use the coinmarketcap.com url for provided coin/token
page.
Reads the OHLCV and Market Cap. Converts the date format to be readable.
Makes sure that the data is consistant by converting non_numeric values to
a number very close to 0. And finally tags each columns if provided.
  """
  market_data = pd.read_html("https://coinmarketcap.com/currencies/" +
  market + "/historical-data/?start=20130428&end="+time.strftime("%Y%m%d"),
flavor='html5lib')[0]
  market_data = market_data.assign(Date=pd.to_datetime(market_data['Date']))
  market_data['Volume'] = (pd.to_numeric(market_data['Volume'],
errors='coerce').fillna(0))
  if tag:
    market_data.columns = [market_data.columns[0]] + [tag + '_' + i for i in
market_data.columns[1:]]
  return market_data

#btc_data = get_market_data("bitcoin", tag='BTC')
#last_date = btc_data.iloc[0, 0]
#print(type(last_date))
btc_data=pd.read_csv('data3.0.csv')
btc_data['Date']=pd.to_datetime(btc_data['Date'])
print(type(btc_data['Date'][0]))
#btc_data.to_csv('data.csv')