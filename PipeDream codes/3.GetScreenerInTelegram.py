'''
Title: Get screener results in python

Step 1 : Fetch screener result using Python
Step 2 : Send the fetched screener result to Telegram

@Change log
@V1 - 29-10-2024 - Paranthaman - Base changes
'''

################### Code for fetching screener result ###################

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pandas import DataFrame
import pytz
import asyncio
import telegram

#Get IST timezone
IST = pytz.timezone('Asia/Kolkata') 

#Data import
data = {
  "Category": ["Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "Sky", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star", "5 star"],
  "OkBom": ["504605", "505299", "506879", "522101", "523411", "526367", "531201", "532783", "534618", "538734", "540900", "542460", "522195", "531112", "531431", "532553", "538567", "540737", "543230", "500245", "505160", "523606", "526775", "530475", "533179", "540125", "543547", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
  "OkNse": ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "SKYGOLD", "JASH", "ANANDRATHI", "VBL", "ZENTEC", "INDRAMEDCO", "APARINDS", "PGEL", "ICEMAKE", "BANCOINDIA", "SHRIPISTON", "BLS", "REFEX", "SENCO", "WONDERLA", "KEI", "ELECON", "VENUSPIPES", "KPITTECH", "KIRLOSENG", "DSSL", "VOLTAMP", "ACE", "MAZDOCK", "KPIGREEN", "RVNL", "JWL", "BCONCEPTS", "TIPSMUSIC", "CDSL", "WINDLAS", "SARDAEN", "PITTIENG", "MOTILALOFS", "DEEPINDS", "SALZERELEC", "GANECOS", "VPRPL", "GRWRHITECH", "GENUSPOWER", "PGIL", "PREMIERPOL", "MARKSANS", "RPGLIFE", "KFINTECH", "EMSLIMITED", "BECTORFOOD", "ITDCEM", "RADHIKAJWE", "HBLPOWER", "DLINKINDIA", "TPLPLASTEH", "HPL", "MACPOWER", "TIINDIA", "POLYMED", "JBCHEPHARM", "USHAMART", "KAYNES", "PENIND", "BALUFORGE", "POLYCAB", "CAPLIPOINT", "RKFORGE", "IONEXCHANG", "LINCOLN", "SAFARI", "ETHOSLTD", "LINDEINDIA", "AVG", "MANINFRA", "JTLIND", "SONATSOFTW", "SUPREMEIND", "KDDL", "KSOLVES", "CSLFINANCE", "ZODIAC"]
}

#Store existing stock data into data frame
existingStocksList = pd.DataFrame(data)

url = "https://chartink.com/screener/process"

# Get CIS stocks list
condition = {"scan_clause": "( {cash} ( weekly close > weekly sma( weekly close , 21 ) and weekly close > weekly sma( weekly close , 63 ) and weekly rsi( 14 ) > 60 and 1 week ago rsi( 14 ) < 60 and market cap < 200000000000 and latest open > 200 and latest volume > 5000 ) )"} 

# Get Cash / Nifty 500 stocks with daily RSI below 30
#condition = {"scan_clause":"( {57960} ( latest volume > latest sma( volume,10 ) * 1.5 and latest close > 200 and latest rsi( 14 ) < 30 and 1 day ago  rsi( 14 ) >= 30 ) ) "}


#Replace tokens in credentials.py file (or) hardcode the token here
TOKEN = 'REPLACE_TOKEN'
chat_id = 'REPLACE_CHATID'

# Channel ID Sample: -1001829542722
bot = telegram.Bot(token=TOKEN)

#Telegram - Send message
async def send_message(text, chat_id):
    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)

#Telegram - Send document
async def send_document(document, chat_id):
    async with bot:
        await bot.send_document(document=document, chat_id=chat_id)
 
async def main():
    
    with requests.session() as s:
        r_data = s.get(url)
        #soup = bs(r_data.content, "lxml")
        soup = bs(r_data.content,  "html.parser")
        
        #get CSRF token from browser for Chartink Validation
        meta = soup.find("meta", {"name" : "csrf-token"})["content"]
        header = {"x-csrf-token" : meta}
        
        #make POST call to API
        data = s.post(url, headers=header, data=condition).json()
        screenerStockList = pd.DataFrame(data["data"])
        # raw screener result
        #print(screenerStockList) 
        
        #Find and send ok stocks with Momentum
        # Combine screenerStockList , existingStocksList data frames if any of the BOM code matches and then drop empty rows
        bseCombinedStockList = pd.merge(screenerStockList, existingStocksList, how='left', left_on='bsecode', right_on='OkBom')
        bseCombinedStockList.dropna(subset=['OkBom'], inplace=True)
        #print("OK stocks matching BSE code "+ '\n' +'\n' +bseCombinedStockList)

        # Combine screenerStockList , existingStocksList data frames if any of the NSE code matches and then drop empty rows
        nseCombinedStockList = pd.merge(screenerStockList, existingStocksList, how='left', left_on='nsecode', right_on='OkNse')
        nseCombinedStockList.dropna(subset=['OkNse'], inplace=True)
        #print("OK stocks matching NSE code " + '\n' +'\n' +nseCombinedStockList)
        
        okStockList = pd.concat([bseCombinedStockList, nseCombinedStockList], ignore_index=True, sort=False)
        #remove unwanted columns from result
        okStockList = okStockList.drop(columns=['sr', 'bsecode','volume','name','OkBom','OkNse'])
        okStockList = okStockList.filter(['close','nsecode','per_chg'])
        okStockList.rename(columns={'nsecode': 'StockCode','per_chg':'Percentage','close':'Price'}, inplace=True)
        #print("Ok Stocks with Momentum " + '\n' +'\n' +okStockList)

        ''' Send Screener result to user  '''
        #add date column 
        screenerStockList['date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
        #sort result in descending by percentage increase
        screenerStockList = screenerStockList.sort_values(by='per_chg',ascending=False)
        csvFileName = 'CIS Screener Result ' +datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S') + '.csv'
        screenerStockList.to_csv(csvFileName)
        
        #Remove unwanted columns
        screenerStockList = screenerStockList.drop(columns=['sr', 'bsecode','volume','name','date'])
        screenerStockList = screenerStockList.filter(['close','nsecode','per_chg'])
        screenerStockList.rename(columns={'nsecode': 'StockCode','per_chg':'Percentage','close':'Price'}, inplace=True)
        #print("Stocks from Screener formatted :  " + '\n' +'\n' +screenerStockList)
        
        # Sending a message
        MessageToBeSent = 'Ok stocks with CIS momentum '+datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S' )+ '\n' +'\n' + okStockList.to_string() + '\n' +'\n' +   'CIS Screener result '+datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S' )+ '\n' +'\n' +screenerStockList.to_string() 
        print(MessageToBeSent)
        await send_message(text=MessageToBeSent, chat_id=chat_id)
        await send_document(document=open(csvFileName, 'rb'), chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())