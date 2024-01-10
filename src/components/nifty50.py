import pandas as pd
import yfinance as yf
# from src.exception import CustomException
nifty_50_names_url  = 'https://en.wikipedia.org/wiki/NIFTY_50#Constituents'



class Nifty50:
    def __init__(self):
        self.url = nifty_50_names_url
    def nifty_50_tickers(self):
        '''
        Gathers all the nifty50 tickers
        
        '''
        try:
            stocks = pd.read_html(self.url)[2]
            stocks['Symbol'] = stocks['Symbol'] + '.NS'
            stock_symbols = stocks['Symbol'].tolist()
            return stock_symbols
        except Exception as e:
            raise (e)
    
