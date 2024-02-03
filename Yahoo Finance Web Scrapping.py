import requests
from bs4 import BeautifulSoup
import json
import os

print(os.getcwd()) # print the location of the scrapped stock file 

#Make custom header
#A user agent is a string of text that identifies the software and device making a request over a network. 
#In the context of web browsing, the user agent is sent along with HTTP requests to servers, allowing the server to tailor its response based on the capabilities and specifications of the client device and software.
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'} #{} is symbol-object

mystocks = ['AAPL', 'TSLA', 'AMZN', 'META'] #loop through this list
#then save to a new list
stockdata =[]

#add fetch sp500  with same code format but with SP500 link and webpage 

def fetch_stock_data(symbol):
    url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch' #change to SP500 list if want to fetch all stocks in SP500
    data = requests.get(url)

    if data.status_code == 200:
        html = data.content
    
        # Parse the HTML content
        soup = BeautifulSoup(data.text, 'html.parser')

        # Find the HTML element containing the stock price
        html = soup.find('div', {'class': 'D(ib) Mend(20px)'})
        # Extract the stock price text
        if html:
            stock = {
                'symbol' : symbol,
                'stock_price' : html.find_all('fin-streamer')[0].text,
                'price_Change' : html.find_all('fin-streamer')[1].text
            }
            return stock
        else:
            print("Stock price not found")
    else:
        print("Failed to fetch the webpage. Status code:", data.status_code)

#create a FOR loop to loop mystock list
for i in mystocks:
    print('getting:', i)
    stockdata.append(fetch_stock_data(i)) #append each stock (i) to the list and put (i) into fetch_ fuction
print(stockdata)

with open('stockdata.json', 'w') as f: #open file and write, if read use "r"
    json.dump(stockdata, f)

print("File 'stockdata.json' created successfully.")
