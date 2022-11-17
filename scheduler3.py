#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 00:38:16 2022

@author: chris
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 22:46:05 2022

@author: chris
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 01:09:34 2022

@author: chris
"""

# Schedule Library imported
import schedule
import time
import os
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import pyttsx3
from datetime import datetime
import logging 


 
# Functions setup
def sudo_placement():
    #BTC price

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("The Current Time is", current_time)   
    current_time_log = "The Current Time is: " + current_time + "\n"
    f = open("demofile2.txt", "a")
    f.write(current_time_log)
    f.close()    


    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = float(btc_price['price'])
    print("The Current Price of Bitcoin is:", btc_price )
    btc_price_string = str(btc_price)
    btcpricelog = "The Price of Bitcoin is: " + btc_price_string + "\n"
    f = open("demofile2.txt", "a")
    f.write(btcpricelog)
    f.close()



   # print(stopPrice)
   # print(side)
    
    #btc_price_buy = None
    btc_price_sell = None
    #buy_limit_price = None
    #sell_limit_price = None
    btc_price_cancel_buy = None
    btc_price_cancel_sell = None
    
    
    #Cancel Threshold
    cancel_threshold = 0.005
    buy_cancel = 1- cancel_threshold
    sell_cancel = 1 + cancel_threshold
    
    
    #Stop Limit
    buy_stop_factor = 1.0025
    sell_stop_factor = 0.995
    
    
    
    orders = client.get_open_orders(symbol='BTCUSD')
    orderPlaced = len(orders)
    if orderPlaced > 0:
        stopPrice = orders[0]['stopPrice']
        stopPrice = stopPrice
        side = orders[0]['side']
        #print(stopPrice)
        #print(side)
        if side == 'BUY':
            btc_price_buy = round(float(stopPrice) / buy_stop_factor)
            btc_price_cancel_buy = btc_price_buy * buy_cancel
            #sell_amount = orders[0]['origQty']
            print("Cancel buy if BTC falls below: $" , round(btc_price_cancel_buy, 2))
            btc_price_cancel_buy_str = str(btc_price_cancel_buy)
            btc_cancel_buy_log = "Cancel buy if BTC falls below: " +btc_price_cancel_buy_str
            f = open("demofile2.txt", "a")
            f.write(btc_cancel_buy_log)
            f.close()
            print("Order will buy if BTC rises above $" + stopPrice)  
            stopPrice_string = str(stopPrice)
            stopPrice_log = "Order will sell if BTC falls below " + stopPrice_string + "\n \n"
            f = open("demofile2.txt", "a")
            f.write(stopPrice_log)
            f.close()            
            MyorderId = orders[0]['orderId']  
        if side == 'SELL':
            btc_price_sell = round(float(stopPrice) / sell_stop_factor)
            btc_price_cancel_sell = btc_price_sell * sell_cancel
            #sell_amount = orders[0]['origQty']
            print("Cancel sell if BTC rises above: $" , round(btc_price_cancel_sell, 2))
            btc_price_cancel_sell_str = str(btc_price_cancel_sell)
            btc_cancel_sell_log = "Cancel sell if BTC falls below: " +btc_price_cancel_sell_str + "\n"
            f = open("demofile2.txt", "a")
            f.write(btc_cancel_sell_log)
            f.close()
            print("Order will sell if BTC falls below $" + stopPrice)
            stopPrice_string = str(stopPrice)
            stopPrice_log = "Order will sell if BTC falls below " + stopPrice_string + "\n \n"
            f = open("demofile2.txt", "a")
            f.write(stopPrice_log)
            f.close()
            MyorderId = orders[0]['orderId']  
    


    
    #USD Balance
    usd_balance = client.get_asset_balance(asset='USD')
    usd_balance_free = float(usd_balance['free'])
    #print("Available USD Balance:" , usd_balance_free)
    #usd_balance_locked = float(usd_balance['locked'])   
    #print("USD Balance on Orders:" , usd_balance_locked)
    
    #BTC Balance
    btc_balance = client.get_asset_balance(asset='BTC')
    btc_balance_free = float(btc_balance['free'])
    #print("Available Bitcoin Balance" , btc_balance_free)
    #btc_balance_locked = float(btc_balance['locked'])   
    #print("BTC Balance on Orders:" , btc_balance_locked)    
    

    
    #Bitcoin Buy
    if usd_balance_free > 10:
        buy_target_low = round(btc_price * .95, 2)
        # print(buy_target_high)
        buy_limit = round(btc_price * 1.01, 2)
        buy_stop = round(btc_price * buy_stop_factor, 2)
        buy_amount = round(usd_balance_free * .999 / buy_limit, 6)
        # print(amount)
        #btc_price_buy = btc_price
        #btc_buy_voice = round(btc_price_buy,0)

        try:
            order = client.create_oco_order(
                symbol='BTCUSD',
                side='BUY',
                quantity=buy_amount,
                price=buy_target_low,
                stopPrice=buy_stop,
                stopLimitPrice=buy_limit,
                stopLimitTimeInForce='GTC')
        
        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
        #print(order)

       #buy_limit_price = (order['orderReports'][0]['price'])
        #print(MyorderId)
        buysay = pyttsx3.init()
        buysay.say("Bitcoin buy order placed")
        buysay.runAndWait()
        orders = client.get_open_orders(symbol='BTCUSD')     
        stopPrice = orders[0]['stopPrice']
        btc_price_buy = round(float(stopPrice) / buy_stop_factor)        
        print("")
        print("Buy Order Placed at" , btc_price_buy)
        print("Stop Price is" , stopPrice)        
        print("")        


   
        

        
    #Bitcoin Sell    
    if btc_balance_free > .01:
        sell_target_high = round(btc_price * 1.05, 2)
        sell_limit = round(btc_price * .98, 2)
        sell_stop = round(btc_price * sell_stop_factor, 2)
        #sell_amount = round(btc_balance_free * .999,6)
        btc_price_sell = btc_price 
       
        closed_orders = client.get_all_orders(symbol='BTCUSD')
        sell_amount = closed_orders[499]['origQty'] 
        try:
            order = client.create_oco_order(
                symbol='BTCUSD',
                side='SELL',
                quantity=sell_amount,
                price=sell_target_high,
                stopPrice=sell_stop,
                stopLimitPrice=sell_limit,
                stopLimitTimeInForce='GTC')
      

        
        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

        #print(order)
        # buy = pyttsx3.init()
        # buy.say("Bitcoin Sell order placed")
        # buy.runAndWait()        
        #MyorderId = order['orders'][1]['orderId']
        #sell_limit_price = (order['orderReports'][0]['price'])    
        #btc_price_cancel_buy = 0
        #print(MyorderId)
        orders = client.get_open_orders(symbol='BTCUSD')     
        stopPrice = orders[0]['stopPrice']
        btc_price_sell = round(float(stopPrice) / sell_stop_factor)        
        print("")
        print("Sell Order Placed at" , btc_price_sell)
        print("Stop Price is" , stopPrice)        
        print("")
        buysay = pyttsx3.init()
        buysay.say("Bitcoin sell order placed")
        buysay.runAndWait()        
    
    if orderPlaced > 0:       
        if btc_price_cancel_sell is not None:
            if btc_price  > btc_price_cancel_sell and side == 'SELL':
                #cancel order    
                cancel = client.cancel_order(symbol='BTCUSD', orderId=MyorderId)
                print("")
                print("ORDER CANCELLED")
                print("")
                buy = pyttsx3.init()
                buy.say("Sell Cancelled")
                buy.runAndWait()        
        if btc_price_cancel_buy is not None:
            if btc_price < btc_price_cancel_buy and side == 'BUY':
                print(btc_price)
                print(btc_price_cancel_buy)
                #cancel order    
                cancel = client.cancel_order(symbol='BTCUSD', orderId=MyorderId)
                print("")
                print("ORDER CANCELLED")        
                print("")
                buy = pyttsx3.init()
                buy.say("Buy Cancelled")
                buy.runAndWait() 
        

        


    print("")

    #time.sleep(10)
 
# def good_luck():
#     print("Good Luck for Test")
 
# def work():
#     print("Study and work hard")
 
# def bedtime():
#     print("It is bed time go rest")
     
# def geeks():
#     print("Shaurya says Geeksforgeeks")
 
# # Task scheduling
# # After every 10mins geeks() is called.
# schedule.every(15).minutes.do(geeks)
 
# # After every hour geeks() is called.
# schedule.every().hour.do(geeks)
 
# # Every day at 12am or 00:00 time bedtime() is called.
# schedule.every().day.at("00:00").do(bedtime)
 
# # After every 5 to 10mins in between run work()
# schedule.every(5).to(10).minutes.do(work)
 
# # Every monday good_luck() is called
# schedule.every().monday.do(good_luck)
 
# Every tuesday at 18:00 sudo_placement() is called
schedule.every(15).seconds.do(sudo_placement)
 
# Loop so that the scheduling task
# keeps on running all time.
while True:
 
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(10)
