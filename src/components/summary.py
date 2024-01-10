import numpy as np



class Summary:
    def __init__(self):
        pass
    
    def CAGR(self,final,begin,years):
        '''
        Returns CAGR perc
        '''
        try:
            cagr = (((final/begin)**(1/years))-1)*100
            return cagr
        except Exception as e:
            raise (e)
    def volatility(self,dailyRet):
        '''
        returns volatality perc
        '''
        try:
            vol = (np.sqrt(252)*(np.std(dailyRet)))*100
            return vol
        except Exception as e:
            raise (e)
    def sharpe_ratio(self,dailyRet):
        '''
        returns sharpe ratio
        '''
        try:
            sr = np.sqrt(252)*(np.mean(dailyRet)/np.std(dailyRet))
            return sr
        except Exception as e:
            raise (e)