#%%
import yfinance as yf
import schedule
import time
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
from datetime import datetime

#%%
# Email setup (replace with your own email details)
EMAIL_ADDRESS = 'daniele@worldluxuryhome.com'
EMAIL_PASSWORD = 'BlackWhite9900!'
TO_EMAIL = 'danielesala1986@gmail.com'
SMTP_SERVER = 'pro.turbo-smtp.com'
SMTP_PORT = 587



# Function to fetch current stock price
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    current_price = data['Close'].iloc[-1]
    return current_price

# Function to send email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to load stocks to monitor from a CSV file
def load_stocks_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    stocks = []

    for index, row in df.iterrows():
        stock = {
            "ticker": row['stock'],
            "low": row['SL'],
            "high": row['TP1']
        }
        stocks.append(stock)

    return stocks

# Function to check if the market is open
def is_market_open():
    # Define the market's timezone
    market_timezone = pytz.timezone('US/Eastern')
    now = datetime.now(market_timezone)

    # Check if today is a weekday (Monday=0, Sunday=6)
    if now.weekday() >= 5:  # Saturday and Sunday
        return False

    # Define market open and close times
    market_open_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)

    # Check if current time is within market hours
    if market_open_time <= now <= market_close_time:
        return True
    else:
        return False

# Function to check the stock prices
def check_stocks(stocks_to_monitor):
    if not is_market_open():
        print("Market is closed. Skipping stock check.")
        return  # Exit the function if the market is closed

    alerts = []  # List to store alerts

    for stock in stocks_to_monitor:
        ticker = stock['ticker']
        low = stock['low']
        high = stock['high']

        current_price = get_stock_price(ticker)
        print(f"Current price of {ticker}: {current_price}")

        if current_price < low:
            alert = f"Alert: {ticker} price below {low}. Current price: {current_price}"
            print(alert)
            alerts.append(alert)
        elif current_price > high:
            alert = f"Alert: {ticker} price above {high}. Current price: {current_price}"
            print(alert)
            alerts.append(alert)
        else:
            print(f"{ticker} is within the range {low}-{high}.")

    # Send a single email if there are any alerts
    if alerts:
        subject = "Stock Price Alerts"
        body = "\n\n".join(alerts)
        print("Sending email with the following alerts:")
        print(body)
        send_email(subject, body)

# Load stocks to monitor from CSV
stocks_to_monitor = load_stocks_from_csv('stocks.csv')

# Run the check_stocks function as a one-time thing
check_stocks(stocks_to_monitor)

# %%
