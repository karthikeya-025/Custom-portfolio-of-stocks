import yfinance as yf
import pandas as pd
import datetime as dt
# from src.exception import CustomException


class Stock:
    def __init__(self,stock_symbols:list) -> None:
        self.stock_symbols = stock_symbols
        
    def stock_history(self,start=None,end=dt.datetime.now().strftime('%Y-%m-%d'),interval='1d'):
        stock_data = yf.download(self.stock_symbols,start=start,end=end,interval=interval)
        return stock_data
    def CurPrice(self,curDate):
        try:
            stock_data = self.stock_history(start=curDate)
            data = stock_data[stock_data.index == curDate]['Close']
            return data
        except Exception as e:
            raise (e)
    def NdayRet(self,N,currDate):
        try:
            start = pd.to_datetime(currDate) - pd.DateOffset(N+1)
            start = start.strftime("%Y-%m-%d")
            end = pd.to_datetime(currDate)+ pd.DateOffset(days=1)
            end = end.strftime('%Y-%m-%d')
            stocks = self.stock_history(start=start,end=end)
            stocks = stocks['Adj Close']
            day_1 = stocks.iloc[0]
            day_n = stocks.iloc[-1]
            returns = (day_n/day_1) - 1
            return returns
        except Exception as e:
            raise (e)
    def DailyRet(self,currDate):
        try:
            start = pd.to_datetime(currDate)-pd.DateOffset(days=4)
            start = start.strftime('%Y-%m-%d')
            end = pd.to_datetime(currDate) + pd.DateOffset(days=1)
            end = end.strftime('%Y-%m-%d')
            stocks = self.stock_history(start=start,end=end)
            stocks = stocks['Adj Close']
            yesterday = stocks.iloc[-2]
            today = stocks.iloc[-1]
            returns = (today/yesterday)-1
            return returns
        except Exception as e:
            raise (e)
    def Last30daysPrice(self,currDate):
        try:
            start = pd.to_datetime(currDate) - pd.DateOffset(31)
            start = start.strftime("%Y-%m-%d")
            end = pd.to_datetime(currDate) + pd.DateOffset(days=1)
            end = end.strftime('%Y-%m-%d')
            stocks = self.stock_history(start=start,end=end)

            if stocks[stocks.index==currDate].empty == False:
                return stocks
            else:
                return None
        except Exception as e:
            raise (e)
