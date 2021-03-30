import yagmail
import pandas as pd
from news import NewsFeed, WeatherFeed
import datetime
import time


def send_email():
    api_info = pd.read_excel('/Users/paulsprouse/Desktop/API_info/API_List.xlsx')
    email_password = api_info[api_info['API_Name'] == 'newsapi.org']['email_address'][0]
    password = api_info[api_info['API_Name'] == 'newsapi.org']['password'][0]
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = ((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
    news_feed = NewsFeed(interest=row['interest'],
                         from_date=yesterday,
                         to_date=today,
                         q=row['search'])
    weather_feed = WeatherFeed(zip_code=str(row['zip']))
    email = yagmail.SMTP(user=email_password, password=password)
    email.send(to=row['email'],
               subject=f"Your {row['interest']} news for today!",
               contents=f"Hello {row['name']}\n In the news today. \nFrom Paul Sprouse "
                        f"\n {weather_feed.get_weather()}"
                        f"\n {weather_feed.get_quake()}"
                        f"\n {news_feed.get()}")


while True:
    now_ = datetime.datetime.now()
    if now_.hour == 8 and now_.minute == 23:
        print("Sending the Emails")
        df = pd.read_excel('people_email_list.xlsx')
        for index, row in df.iterrows():
            if row['name'] == "DONE":
                break
            send_email()
    time.sleep(60) # waits a minute to prevent multiple sends in first hour

