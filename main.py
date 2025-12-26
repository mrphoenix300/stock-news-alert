from math import floor
import os
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)

url = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": os.environ.get("API_KEY1"),
}

response = requests.get(url, params)
response.raise_for_status()

data = response.json()

days = data["Time Series (Daily)"]

last_two_days = []
i = 0
for day in days.values():
    if i == 2:
        break
    last_two_days.append(day)
    i += 1

new_closed_price = float(last_two_days[0]["4. close"])
old_closed_price = float(last_two_days[1]["4. close"])
percentage100 = ((new_closed_price - old_closed_price) / old_closed_price) * 100
print(percentage100)

up_down = None
if percentage100 > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(percentage100) >= 5:
    api_key = os.environ.get("API_KEY2")
    url2 = "https://newsapi.org/v2/top-headlines"

    params2 = {
        "q": COMPANY_NAME,
        "country": "us",
        "apiKey": api_key,
        "category": "business",
    }

    response2 = requests.get(url2, params2)
    response2.raise_for_status()

    news = response2.json()["articles"]

    news3 = news[:3]

    receiver = os.environ.get("TEMP_PHONE_NUMBER")

    for event in news3:
        message = client.messages.create(
            messaging_service_sid='MG61833003253135bfefe2edc065b5f6bc',
            body=f"{STOCK}: {up_down}{floor(percentage100)}%\n{event['title']}\n{event['description']}",
            to=receiver
        )
        print(message.status)
