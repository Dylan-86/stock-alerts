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
import sortalphabetical
import os
from dotenv import load_dotenv

load_dotenv()  # load .env

#%%
# Sort the CSV alphabetically - Specify the input and output CSV files and the column to sort
input_file = 'stocks.csv'
output_file = 'stocks.csv'
sort_column = 'symbol'

# Call the sort_csv function
sortalphabetical.sort_csv(input_file, output_file, sort_column)

#%%
# Load variables
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))  # Default 587 


def get_stock_price(ticker, retries=4, delay=1):
    for attempt in range(retries):
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            return data['Close'].iloc[-1]
        print(f"Attempt {attempt + 1} failed for {ticker}. Retrying...")
        time.sleep(delay)
    print(f"{ticker}: No data found after {retries} attempts.")
    return 0

# Function to get P/E ratio
def get_pe_ratio(ticker):
    stock = yf.Ticker(ticker)
    try:
        pe_ratio = stock.info.get('trailingPE', None)
        return pe_ratio if pe_ratio else "N/A"
    except Exception as e:
        print(f"Error retrieving P/E ratio for {ticker}: {e}")
        return "N/A"

# Function to send email
def send_email(subject, body_html):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    # Attach HTML body
    msg.attach(MIMEText(body_html, 'html'))

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
            "ticker": str(row['symbol']).replace(".", "-"),  # Ensure "." is replaced with "-"
            "low": row['SL'],
            "high": row['TP1']
        }
        #print(stock)  # Debugging print
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




def check_stocks(stocks_to_monitor):
    if not is_market_open():
        print("Market is closed. Skipping stock check.")
        return  # Exit the function if the market is closed

    data = []  # List to store table rows

    for stock in stocks_to_monitor:
        ticker = stock['ticker']
        low = stock['low']
        high = stock['high']
        current_price = round(get_stock_price(ticker), 2)
        pe_ratio = round(get_pe_ratio(ticker), 2) if get_pe_ratio(ticker) != "N/A" else "N/A"
        print(f"Current price of {ticker}: {current_price}, P/E Ratio: {pe_ratio}")

        # Determine status
        if current_price < low:
            status = f"<span style='color: red;'>⬇️ Below SL ({low})</span>"
            data.append([ticker, current_price, status, pe_ratio])  # Only add stocks below SL
        elif current_price > high:
            status = f"<span style='color: green;'>⬆️ Above TP ({high})</span>"
            data.append([ticker, current_price, status, pe_ratio])  # Only add stocks above TP

    # If no alerts, do not send an email
    if not data:
        print("No alerts to send.")
        return

    # Generate an HTML table
    table_html = """
    <html>
    <head>
        <style>
            table {border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;}
            th, td {border: 1px solid black; padding: 8px; text-align: center;}
            th {background-color: #f2f2f2;}
        </style>
    </head>
    <body>
        <h2>📈 Stock Price Alerts</h2>
        <table>
            <tr>
                <th>Ticker</th>
                <th>Current Price</th>
                <th>Status</th>
                <th>Current P/E</th>
            </tr>
    """

    for row in data:
        table_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
            </tr>
        """

    table_html += """
        </table>
    </body>
    </html>
    """

    print("Sending email with the alerts:")
    print(data)
    send_email("Stock Price Alerts", table_html)



# Load stocks to monitor from CSV
stocks_to_monitor = load_stocks_from_csv('stocks.csv')

# Run the check_stocks function as a one-time thing
check_stocks(stocks_to_monitor)

# %%
