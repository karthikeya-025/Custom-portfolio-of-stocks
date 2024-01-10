import yfinance as yf
import pandas as pd
from .stock import Stock
from .nifty50 import Nifty50
import numpy as np
import datetime


now = datetime.datetime.now().strftime('%Y-%m-%d')

nf50 = Nifty50()


class Benchmark:
    def __init__(self):
        self.stock_names = nf50.nifty_50_tickers()
        self.stocks = Stock(self.stock_names)
    def benchmark(self,start,end=now,n=1):
        '''
        Returns 2 things:
        1.dictionary - which contains adj close of every month
        2.dailyRet - daily return of the nifty50 stocks
        '''
        try:
            start = pd.to_datetime(start) - pd.DateOffset(1)
            stocks = self.stocks.stock_history(start=start,end=end)['Adj Close']
            dailyRet = stocks.pct_change(n)
            mtly = (stocks+1).resample('BM').last()
            mtly = mtly.transpose()
            print(mtly)
            dictionary = {}
            for i in mtly:
                summed = np.sum(mtly[i])
                dictionary[i] = summed
            return dictionary,dailyRet
        except Exception as e:
            raise (e)

# if __name__ == '__main__':
#     m = Benchmark()
#     print(m.benchmark('2019-01-01',init_eq=10000))