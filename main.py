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

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

data = response.json()
if not isinstance(data, dict):
    raise ValueError("Alpha Vantage returned an invalid response.")

days = data.get("Time Series (Daily)")
if not isinstance(days, dict) or len(days) < 2:
    raise ValueError("Alpha Vantage did not return two trading days of stock prices.")

# Use the latest two dates explicitly, irrespective of JSON field ordering.
latest_dates = sorted(days, reverse=True)[:2]
try:
    new_closed_price = float(days[latest_dates[0]]["4. close"])
    old_closed_price = float(days[latest_dates[1]]["4. close"])
except (KeyError, TypeError, ValueError) as exc:
    raise ValueError("Alpha Vantage returned invalid closing-price data.") from exc

if old_closed_price <= 0 or new_closed_price <= 0:
    raise ValueError("Alpha Vantage returned a non-positive closing price.")
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

    response2 = requests.get(url2, params=params2, timeout=15)
    response2.raise_for_status()

    news_data = response2.json()
    if not isinstance(news_data, dict) or not isinstance(news_data.get("articles"), list):
        raise ValueError("NewsAPI did not return a valid list of articles.")

    news3 = [
        article for article in news_data["articles"]
        if isinstance(article, dict) and isinstance(article.get("title"), str)
    ][:3]

    receiver = os.environ.get("TEMP_PHONE_NUMBER")
    messaging_sid = os.environ.get("MESSAGING_SERVICE_SID")

    for event in news3:
        message = client.messages.create(
            messaging_service_sid=messaging_sid,
            body=f"{STOCK}: {up_down}{floor(percentage100)}%\n{event['title']}\n{event.get('description') or ''}",
            to=receiver
        )
        print(message.status)
