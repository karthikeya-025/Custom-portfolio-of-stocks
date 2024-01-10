import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.components.stock import Stock
from stockPickingStrat import MomentStrat
from src.components.benchmark import Benchmark
from src.components.summary import Summary

bm = Benchmark()
cust = MomentStrat()
summary = Summary()

st.sidebar.title("Custom Portfolio out of Nifty50 stocks")
initial_date = st.sidebar.date_input('Simulation Start date',format='YYYY-MM-DD')
no_of_days = st.sidebar.number_input('Number of days for measurement')
initial_equity = st.sidebar.number_input('Initial Equity')
submit_button = st.sidebar.button('Simulate')




def benchmark_assesment(custDict,benchmarkDict):
    
    fig,ax = plt.subplots(figsize=(10,10))
    ax.plot(list(custDict.keys())[1:],list(custDict.values())[1:],label='Custom');
    ax.plot(list(benchmarkDict.keys())[1:],list(benchmarkDict.values())[1:],label='Benchmark(Nifty-50-Index)')
    ax.legend(['Custom Strategy','Benchmark(Nifty-50-Index)'],loc='upper left')
    ax.set_xlabel('Years')
    ax.set_ylabel('Equity')
    return fig,ax

if submit_button:
    st.title('Custom Strategy(Momentum) vs Benchmark(Nifty50)')
    benchRet,dailyBenchRet =  bm.benchmark(str(initial_date),n=int(no_of_days))
    selected_stocks,customeRet,dailyCustRet = cust.momentum_strategy(str(initial_date),n=int(no_of_days))
    customeRet,benchRet = cust.equity(customeRet,benchRet,init_eq=float(initial_equity))
    fig,ax = benchmark_assesment(customeRet,benchRet)
    st.pyplot(fig)
    
    #Calculating CAGR ratio
    beginBench = benchRet[list(benchRet.keys())[1]]
    finalBench = benchRet[list(benchRet.keys())[-1]]
    benchYears = int(dailyBenchRet.index.year.nunique())
    
    beginCust = customeRet[list(customeRet.keys())[1]]
    finalCust = customeRet[list(customeRet.keys())[-1]]
    custYears = int(dailyCustRet.index.year.nunique())

    
    custCAGR = np.mean(summary.CAGR(beginCust,finalCust,custYears))

    benchCAGR = np.mean(summary.CAGR(beginBench,finalBench,benchYears))
    
    #Calculating Sharpe Ratio
    cust_sharpe_ratio = np.mean(summary.sharpe_ratio(dailyCustRet))
    bench_sharpe_ratio = np.mean(summary.sharpe_ratio(dailyBenchRet))

    #Calculating Volatality percentage
    cust_vol_perc = np.mean(summary.volatility(dailyCustRet))
    bench_vol_perc =np.mean (summary.volatility(dailyBenchRet))
    
    summary_df = pd.DataFrame( {
        'Custom Strategy':[cust_sharpe_ratio,custCAGR,cust_vol_perc],
        'Benchmark(NIFTY-50)':[bench_sharpe_ratio,benchCAGR,bench_vol_perc]
    },index=['Sharpe','CAGR(in %)','Vol(in %)'])
    st.title('Basic Summary of Custom strategy and Benchmark')
    st.table(summary_df)
    
    st.title('Top Stocks')
    selected = cust.top_stocks(selected_stocks)
    top_stocks = list(map(lambda x:x[0],selected))[0:5]
    for i,stock in enumerate(top_stocks):
        st.text(f'{i+1}.{stock}\n')
    