import requests
from datetime import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_KEY = '3WTW6LH5EL82TVCC'
STOCK_API = 'https://www.alphavantage.co/query'
NEWS_KEY = '925885cd8509428fb29edb0ea0195049'
NEWS_API = "https://newsapi.org/v2/everything"

# ******************** STOCKS *****************************************************************************************
stock_param = {
	'function': 'TIME_SERIES_DAILY_ADJUSTED',
	'symbol': STOCK,
	'apikey': STOCK_KEY,
	'language': 'en'
}
response = requests.get(url=STOCK_API, params=stock_param)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]

yesterday_closing_price = data_list[0]['4. close']
day_before_closing_price = data_list[1]['4. close']

d = float(yesterday_closing_price) - float(day_before_closing_price)
diff = abs(d)
per_diff = (diff / float(yesterday_closing_price)) * 100

# ******** NEWS *******************************************************************************************************
if per_diff > 4:
	news_param = {
		'qInTitle': COMPANY_NAME,
		'apiKey': NEWS_KEY
	}
	response1 = requests.get(url=NEWS_API, params=news_param)
	data1 = response1.json()
	three_articles = data1['articles'][:3]

	lisst = [f"Headline: {article['title']}.\n Content: {article['content']}" for article in three_articles]

	# ******** TWILIO *************************************************************************************************
	# using twilio to send sms
	logo = ''
	if d > 0:
		logo = '🔺'
	else:
		logo = '🔻'

	account_sid = 'AC854966fe60da150fd380f701c16c330f'
	auth_token = 'bafdea80381231cffbd84b8e930409c2'
	NUM = '+18336910767'

	# Send a separate message with the percentage change and each article's title and description to phone number

	client = Client(account_sid, auth_token)

	for article in lisst:
		message = client.messages.create(
			body=f"{STOCK}: {logo} {round(per_diff, 2)}%\n{article}",
			from_='+18336910767',
			to='+16097858775'
		)
		print(message.status)
