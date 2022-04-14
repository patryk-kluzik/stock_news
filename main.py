NASDAQ = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
import requests
from datetime import datetime, timedelta
import os

api_key_alphavantage = os.environ.get("API_KEY_ALPHAVANTAGE")
api_call_alphavantage = 'https://www.alphavantage.co/query'

params = {
    "function": 'TIME_SERIES_DAILY',
    "symbol": NASDAQ,
    "outputsize": "compact",
    "apikey": api_key_alphavantage
}

response = requests.get(url=api_call_alphavantage, params=params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']  # get the daily data

yesterday_dt = datetime.today() - timedelta(days=1)  # get yesterday's datetime
yesterday_str = str(yesterday_dt).split(" ")[0]  # get only the date as str

day_before_yesterday_dt = yesterday_dt - timedelta(days=1)  # get day before yesterday's datetime
day_before_yesterday_str = str(day_before_yesterday_dt).split(" ")[0]  # get only the date as str

yesterday_close = float(data[yesterday_str]["4. close"])  # get the closing price for yesterday
day_before_yesterday_close = float(data[day_before_yesterday_str]["4. close"])  # get the closing price for day before

price_difference = round((yesterday_close - day_before_yesterday_close), 4)  # get price difference to 4 dp
percentage_change = round(price_difference / day_before_yesterday_close * 100, 3)  # get percentage change to 3dp

# get the percentage change as string
if percentage_change < 0:
    change_str = f"🔻{percentage_change}%"
else:
    change_str = f"🔺{percentage_change}%"


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def get_news():
    api_endpoint_newsapi = 'https://newsapi.org/v2/everything'
    api_key_newsapi = os.environ.get("API_KEY_NEWSAPI")
    params_news = {
        "apiKey": api_key_newsapi,
        "from": yesterday_str,
        "langauge": "en",
        "sortBy": "popularity",
        "q": COMPANY_NAME
    }

    response_news = requests.get(url=api_endpoint_newsapi, params=params_news)
    news_data = response_news.json()

    top_3_news = news_data["articles"][:3]  # get first 3 articles

    top_3_news_formatted = []

    # create dictionary with title and description and append to list
    # creating list of top 3 new
    for news in top_3_news:
        top_3_news_dict = {"title": news["title"], "description": news["description"]}
        top_3_news_formatted.append(top_3_news_dict)

    return format_message(top_3_news_formatted)


def format_message(news_list: list) -> list:
    return [f"{NASDAQ}: {change_str}\n "
            f"Headline: {news_item['title']}\n "
            f"Brief: {news_item['description']}"
            for news_item in news_list]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


def send_sms(news_list: list):
    from twilio.rest import Client

    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    my_phone_num = os.environ.get('MY_NUMBER')
    client = Client(account_sid, auth_token)

    for news_item in news_list:
        message = client.messages.create(
            body=news_item,
            from_='+12183001930',
            to=my_phone_num
        )
        print(message.status)


# if the price shifts by 5% or more, get news
if -3 >= percentage_change or percentage_change >= 3:
    news = get_news()
    send_sms(news_list=news)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
