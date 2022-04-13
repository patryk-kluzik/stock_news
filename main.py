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
    "apikey": "asdasdasd"#api_key_alphavantage
}

response = requests.get(url=api_call_alphavantage, params=params)
response.raise_for_status()
data = response.json()['Time Series (Daily)']

yesterday_dt = datetime.today() - timedelta(days=1)
yesterday_str = str(yesterday_dt).split(" ")[0]

day_before_yesterday_dt = yesterday_dt - timedelta(days=1)
day_before_yesterday_str = str(day_before_yesterday_dt).split(" ")[0]

print(data[yesterday_str])
print(data[day_before_yesterday_str])

yesterday_close = float(data[yesterday_str]["4. close"])
day_before_yesterday_close = float(data[day_before_yesterday_str]["4. close"])

price_difference = round((yesterday_close - day_before_yesterday_close), 4)
percentage_change = round(price_difference / day_before_yesterday_close * 100,3)

if -5 > percentage_change or percentage_change > 5:
    print("Get News")
elif percentage_change < 0:
    print(f"Price only decreased by {percentage_change}%")
else:
    print(f"Price only increased by {percentage_change}%")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

