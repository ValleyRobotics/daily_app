import requests
import pandas as pd
import datetime
import yfinance as yf
from rich import print
from rich import inspect
from rich.color import Color
from rich.console import Console
console = Console()



class NewsFeed:
    """Multiple news title and links as a single string based on interest
    """
    base_url = "http://newsapi.org/v2/"
    api_info = pd.read_excel('/Users/paulsprouse/Desktop/API_info/API_List.xlsx')
    api_key = api_info[api_info['API_Name'] == 'newsapi.org']['API_number'][0]

    def __init__(self,
                 interest,
                 from_date,
                 to_date,
                 source_type='everything',
                 country='us',
                 q="qInTitle",
                 language='en',
                 sort_by="sortBy=publishedAT"):
        self.source_type = source_type
        self.country = country
        self.q = q
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language
        self.sort_by = sort_by

    def get(self):
        url = self._build_url()

        articles, content = self._get_articles(url)

        email_body = f"Query: {self.interest} \n" \
                     f"Date From: {self.from_date} \n" \
                     f"Date To: {self.to_date} \n" \
                     f"Total Count: {content['totalResults']}\n\n"

        for article in articles:
            email_body = (email_body +
                          (article['title'] if article['title'] else "") +
                          "\n" + (article['url'] if article['url'] else "") +
                          "\n" + (article['description'] if article['description'] else "") + "\n\n")

        return email_body

    def _get_articles(self, url):
        response = requests.get(url)
        content = response.json()
        articles = content['articles']
        return articles, content

    def _build_url(self):
        url = f"{self.base_url}{self.source_type}?{self.q}={self.interest}&from={self.from_date}&" \
              f"to={self.to_date}&language={self.language}&{self.sort_by}&{self.api_key}"
        return url


class WeatherFeed:
    """Gets Current Weather for the zip code that is sent (5 digits)
    """
    api_info = pd.read_excel('/Users/paulsprouse/Desktop/API_info/API_List.xlsx')
    weather_api = api_info[api_info['API_Name'] == 'openweathermap.org']['API_number'][1]
    url = f'http://api.openweathermap.org/data/2.5/weather?'

    def __init__(self,
                 zip_code,
                 units='imperial'):
        self.zip_code = zip_code
        self.units = units

    def get_weather(self):

        url = f"{self.url}zip={self.zip_code}&units={self.units}&appid={self.weather_api}"
        response = requests.get(url).json()
        ret = f"{response['name']} Weather: {response['weather'][0]['main']} - {response['weather'][0]['description']} " \
              f"\nTemp: {response['main']['temp']} Humidity: {response['main']['humidity']} " \
              f"\nWind Speed: {response['wind']['speed']} Gusts: {response['wind']['gust']} " \
              f"Deg: {response['wind']['deg']} \nVisibility: {response['visibility']} " \
              f"\nSunrise: {datetime.datetime.fromtimestamp(response['sys']['sunrise'])} " \
              f"\nSunset: {datetime.datetime.fromtimestamp(response['sys']['sunset'])}"
        return ret

    def get_quake(self):
        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
        response = requests.get(url).json()
        ret = ""
        for k in response['features']:
            if k.get('properties')['place'].split(' ')[-1] == 'Washington':  # [-2:]=='':
                ret = f"{ret}{k.get('properties')['title']:<60} {str(datetime.datetime.fromtimestamp(k.get('properties')['time'] / 1000)):>30} \n"
                ret1 = (ret + k.get('properties')['title'] + ' ' +
                       str(datetime.datetime.fromtimestamp(k.get('properties')['time'] / 1000)) + '\n')
        return ret


class Stock:
    def __init__(self,
                 symbol):
        self.symbol = symbol

    def get_price(self):
        ticker_data = yf.Ticker(self.symbol)
        ticker_df = ticker_data.history(period='1d')
        return f"SYMBOL: {self.symbol:>5}:    " \
               f"OPEN: ${round(ticker_df['Open'][0], 2):>10}    " \
               f"CURRENT: ${round(ticker_df['Close'][0], 2):>10}    " \
               f"PERCENT CHANGE: %{round(((ticker_df['Close'][0] - ticker_df['Open'][0]) / ticker_df['Open'][0] * 100), 2):>6}"


class Jobs:

    def __init__(self, search, location):
        self.search = search
        self.location = location  # austin%2C+tx
        self.url = "https://api.indeed.com/ads/apisearch?publisher=123412341234123" \
                   "&q={self.search}&l={self.location}" \
                   "&limit=100&v=2&userip=1.2.3.4" \
                   "&useragent=Mozilla/%2F4.0%28Firefox%29&v=2"

    def get_jobs(self):
        response = requests.get(self.url).json()
        return response


if __name__ == '__main__':
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    last_week = ((datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'))
    yesterday = ((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    for val in ['solar energy', 'power plants', 'NASA', 'Seattle', 'MMA']:
        news_feed = NewsFeed(interest=val, from_date=yesterday, to_date=today, q='q', language='en')
        console.rule(f"[bold red]In the News {val}:")
        console.print(news_feed.get())
    weather = WeatherFeed('98045')
    console.rule("[bold red]Weather")
    console.print(weather.get_weather())
    quake = weather.get_quake()
    console.rule("[bold red]Recent Quakes:")
    #console.print('Recent Quakes:')
    console.print(quake)
    console.rule("[bold red]Stocks:")
    stocks = ['^IXIC', '^DJI', 'ITOCY', 'MSFT', 'BA', 'CREG', 'ORA', 'NEP', 'HTOO', 'AY']
    for stock in stocks:
        stock = Stock(symbol=stock)
        console.print(stock.get_price(), style="white")
