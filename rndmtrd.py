import datetime
import numpy as np
import os
import pandas as pd
import random

from configurations import setup_logger, basic_parameters as bp
from multiprocessing import Pool, cpu_count

logger = setup_logger('read_csvs')

names = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']



#----- Lists of files 

csv_dir = '../big_dataframes/binance/spot/daily/klines/BTCUSDT/1s/'
theOrderBookFiles = sorted(os.listdir(csv_dir))

def read_csv_inparalel(file):
    return np.loadtxt(csv_dir+file, delimiter=",", dtype=np.float64, usecols=[0, 1, 2, 3, 4])
    

logger.info('start read csvs')
with Pool(cpu_count()) as p:
    #files = p.map(read_csv_inparalel, theOrderBookFiles)
    files = p.map(read_csv_inparalel, theOrderBookFiles[-3:]) # TEST 3 files
logger.info('finish read csvs')


big_arr = np.concatenate(files, axis=0)

#df['time UTC'] = pd.to_datetime(df['Open time'], unit='ms', origin='unix')

logger.info(big_arr.shape)
#logger.info(big_arr)

# # check order of rows in array
# for i, row in enumerate(big_arr):
#     if (i > 0) & (row[0] < big_arr[i-1][0]):
#         logger.error(f'timestamp error. Current {row[0]} is smaller than {big_arr[i-1][0]}')



random_trades = random.sample(range(big_arr.shape[0]-(big_arr.shape[0]*3)//10), 1000)
random_trades.sort()
#logger.info(random_trades)


profits = 0
losses = 0
trade_exit = 0
not_finished_trades = 0

logger.info('start loop')

for rand in random_trades:
    if rand > trade_exit:
        for i, big_arr_i in enumerate(big_arr):
            if i < trade_exit:
                continue # skip until the end of a trade

            if i == rand: # start random trade
                #logger.info(f'time_of_signal: {datetime.datetime.utcfromtimestamp(big_arr_i[0]/1000)}')

                buy_price = big_arr_i[1]
                max_high = big_arr_i[2]
                max_low = big_arr_i[3]
                loss = 0
                profit = 0
                
                for m, big_arr_m in enumerate(big_arr[(i+1):]):
                
                    profit_percent = 0.1
                    loss_percent = 0.02

                    if big_arr_m[2] > max_high:
                        max_high = big_arr_m[2]
                        profit = (max_high - buy_price) * 100 / buy_price

                    if big_arr_m[3] < max_low:
                        max_low = big_arr_m[3]
                        loss = (buy_price - max_low) * 100 / buy_price

                    if profit >= profit_percent:
                        profits += 1

                    if loss >= loss_percent:
                        losses += 1

                    if profit >= profit_percent or loss >= loss_percent:
                    #if profit >= profit_percent:
                        #print(f'buy_price: {buy_price}')
                        #print(f'profit: {profit} || loss: {loss}')
                        #print(f'max_high: {max_high} || max_low: {max_low}')
                        #print(f'time of the end a trade: {datetime.datetime.utcfromtimestamp(big_arr_m[0]/1000)}')

                        trade_exit = (i+1)+(m+1)

                        break
                else:
                    not_finished_trades += 1

                
                break




        #if i % 30_000 == 0:
        #    logger.info(f'profits: {profits} || loss: {losses} || {datetime.datetime.utcfromtimestamp(big_arr_i[0]/1000)}')

logger.info(f'profitable trades: {profits} - {profits*profit_percent} \n\
lose trades: {losses} - {losses*loss_percent} \n\
not_finished_trades: {not_finished_trades} \n\
profit_percent: {profit_percent} || loss_percent: {loss_percent} \n\
total_profit: {(profits*profit_percent)-(losses*loss_percent)}')

logger.info('finish')
        