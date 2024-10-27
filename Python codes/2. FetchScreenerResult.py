'''
Fetch screener result using Python - 

Technical - Data comes from a POST request. 
You simply need to pick up 
    (a) one cookie (ci_session - which can be done using Session object to hold cookies from initial landing page request to pass on with subsequent POST),
    (b) and one token (X-CSRF-TOKEN - which can be pulled from a meta tag in the initial request response):
    
Steps:
    (1) Get the screener URL and load it with Inspect element
    (2) Open Network tab & find "process" 
    (3) Load Payload table and copy the scan_clause. Example below
        ( {cash} ( weekly close > weekly sma( weekly close , 21 ) and weekly close > weekly sma( weekly close , 63 ) and weekly rsi( 14 ) > 60 and 1 week ago rsi( 14 ) < 60 and market cap < 200000000000 and latest open > 200 and latest volume > 5000 ) ) 
    (4) Update the condition in below script
'''

# mandatory  library
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
#from datetime import datetime


url = "https://chartink.com/screener/process"

condition = {"scan_clause": "( {cash} ( weekly close > weekly sma( weekly close , 21 ) and weekly close > weekly sma( weekly close , 63 ) and weekly rsi( 14 ) > 60 and 1 week ago rsi( 14 ) < 60 and market cap < 200000000000 and latest open > 200 and latest volume > 5000 ) )"} 
#condition = {"scan_clause" : "( {cash} ( latest rsi( 9 ) > latest wma( latest rsi( 9 ) , 21 ) and 1 day ago  rsi( 9 ) <= 1 day ago  wma( latest rsi( 9 ) , 21 ) and latest rsi( 9 ) > 70 and market cap > 1500 ) ) "}

with requests.session() as s:
    r_data = s.get(url)
    soup = bs(r_data.content, "lxml")
    
    #get CSRF token from browser for Chartink Validation
    meta = soup.find("meta", {"name" : "csrf-token"})["content"]
    header = {"x-csrf-token" : meta}
    
    #make POST call to API
    data = s.post(url, headers=header, data=condition).json()
    screenerStockList = pd.DataFrame(data["data"])  
    #add current date to data column
    screenerStockList['date'] = pd.Timestamp.today().strftime('%Y-%m-%d') 
    #Print final stock list
    print("Stocks from Screener : ")
    print(screenerStockList) 
    