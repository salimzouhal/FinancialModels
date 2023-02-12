import requests
import json

class DataScraper:
    def __init__(self, api_key, ticker):
        self.api_key = api_key
        self.ticker = ticker

    def get_quote(self):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.ticker}&apikey={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data['Global Quote']

    def get_financials(self):
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={self.ticker}&apikey={self.api_key}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

apikey = 'TGQVZHVO92AP5GWD'

if __name__ == "__main__":
    aapl = DataScraper(apikey,'AAPL')
    financials = aapl.get_quote()
    for key, value in financials.items() :
        print(f'{key}: {value}')