import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
StockAPIkey = "LSOPXBC2FRAE0WY4"
NewsAPIkey = "699ccb29b29843ada7453c0128026fcf"

#
account_sid = "yourapi"
auth_token = "yourauth"
client = Client(account_sid, auth_token)

# Initialize three_articles as an empty list
three_articles = []



#Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": StockAPIkey
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data  =  data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


#Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))



# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = round(difference / float(yesterday_closing_price)) * 100
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
if diff_percent > 0:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NewsAPIkey
    }
    news = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news.json()
    news_articles = news_data["articles"]
    three_articles = news_articles[:3]
    print(three_articles)

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"Headline: {article["title"]}, {up_down}{diff_percent}%\nBrief: {article["description"]}" for article in three_articles]
print(formatted_articles)

#TODO 9. - Send each article as a separate message via Twilio.
for article in formatted_articles:
    message = client.messages.create(
        body=f"{STOCK_NAME}: 🔺{diff_percent}%\n{formatted_articles[0]}",
        from_="+435345345334534",
        to="+34353445345",
    )
    print(message.status)

#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
orcr
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
