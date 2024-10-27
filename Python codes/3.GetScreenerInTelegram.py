'''
Title: Get screener results in python

Step 1 : Fetch screener result using Python
Step 2 : Send the fetched screener result to Telegram

'''

################### Code for fetching screener result ###################

# mandatory  library
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pandas import DataFrame

#Get telegram autnetication tokens
import Credentials

url = "https://chartink.com/screener/process"

# Get CIS stocks list
condition = {"scan_clause": "( {cash} ( weekly close > weekly sma( weekly close , 21 ) and weekly close > weekly sma( weekly close , 63 ) and weekly rsi( 14 ) > 60 and 1 week ago rsi( 14 ) < 60 and market cap < 200000000000 and latest open > 200 and latest volume > 5000 ) )"} 

# Get Cash / Nifty 500 stocks with daily RSI below 30
#condition = {"scan_clause":"( {57960} ( latest volume > latest sma( volume,10 ) * 1.5 and latest close > 200 and latest rsi( 14 ) < 30 and 1 day ago  rsi( 14 ) >= 30 ) ) "}

import asyncio
import telegram

#Token for 
TOKEN = Credentials.token
chat_id = Credentials.chatId


# Channel ID Sample: -1001829542722
bot = telegram.Bot(token=TOKEN)

async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)
        

async def main():
    
    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        
        #get CSRF token from browser for Chartink Validation
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]
        header = {"x-csrf-token" : meta}
        
        #make POST call to API
        data = s.post(url, headers=header, data=condition).json()
        screenerStockList = pd.DataFrame(data["data"])  
        #print(screenerStockList) 
        
        #Remove unwanted columns
        screenerStockList = screenerStockList.drop(columns=['sr', 'bsecode','volume'])
        screenerStockList = screenerStockList.filter(['close','nsecode','name','per_chg'])
        screenerStockList.rename(columns={'nsecode': 'StockCode', 'name': 'StockName','per_chg':'Percentage','close':'Price'}, inplace=True)
  

        #screenerStockList = screenerStockList.drop(screenerStockList.columns[[,4,5,6,7]], axis=1)
        #Print final stock list
        print("Stocks from Screener : ")
        print(screenerStockList) 
        
        # Sending a message
        #CurrentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        MessageToBeSent = 'CIS Screener result '+datetime.now().strftime('%Y-%m-%d %H:%M:%S' )+ '\n' +'\n' + screenerStockList.to_string()
        await send_message(text=MessageToBeSent, chat_id=chat_id)
        #screenerStockList = screenerStockList.to_string()
        #await send_message(text=screenerStockList, chat_id=chat_id)


if __name__ == '__main__':
    asyncio.run(main())