# Stock Price Alert System

This project is a Python-based script that monitors stock prices using the `yfinance` library and sends email alerts when prices cross specified thresholds. It is designed to help traders and investors keep track of critical price movements during market hours.

## Features

- Retrieves real-time stock prices using the [yfinance](https://github.com/ranaroussi/yfinance) library.
- Sends email alerts if a stock's price goes below a specified support level (SL) or above a target price (TP1).
- Reads stock information (ticker, SL, TP1) from a CSV file.
- Checks stock prices only during US market hours (9:30 AM to 4:00 PM ET).
- Handles retries for fetching stock data to ensure reliability.
- Simple email notifications using `smtplib`.

## Prerequisites

1. Python 3.8 or higher.
2. Install the required Python libraries:
   ```bash
   pip install yfinance pandas schedule pytz

Setup
Clone this repository:

bash
Copia codice
git clone https://github.com/your-username/stock-price-alert.git
cd stock-price-alert
Create a stocks.csv file in the following format:

csv
Copia codice
stock,SL,TP1
AAPL,140,160
MSFT,250,280
GOOGL,2700,3000
stock: Stock ticker symbol (e.g., AAPL for Apple, MSFT for Microsoft).
SL: Support level (price below which you want to get alerted).
TP1: Target price (price above which you want to get alerted).
Update the email configuration in the script:

python
Copia codice
EMAIL_ADDRESS = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
TO_EMAIL = 'recipient-email@example.com'
SMTP_SERVER = 'smtp.your-email-provider.com'
SMTP_PORT = 587
Replace the placeholders with your actual email details.

Usage
Run the script manually:

bash
Copia codice
python stock_alert.py
The script will check stock prices and send an email alert if any price thresholds are breached.

To run the script at regular intervals, consider using a task scheduler (e.g., cron on Unix-based systems or Task Scheduler on Windows).

How It Works
Loading Stocks: The script reads stock tickers and thresholds from the stocks.csv file.
Market Hours Check: Prices are checked only during US stock market hours.
Price Fetching: Uses the yfinance library to fetch the latest closing price of each stock.
Alert Triggering: Compares the price with SL and TP1 thresholds and logs alerts.
Email Notifications: Sends a consolidated email with all alerts.
Customization
Modify the market hours logic in is_market_open() if needed.
Adjust the retry logic or delay in get_stock_price() as per your requirements.
Add new alert conditions based on other metrics (e.g., volume, percentage change).
Example Output
Console Log
sql
Copia codice
Current price of AAPL: 150.0
AAPL is within the range 140-160.
Current price of MSFT: 240.0
Alert: MSFT price below 250. Current price: 240.0
Email
makefile
Copia codice
Subject: Stock Price Alerts

Alert: MSFT price below 250. Current price: 240.0
Security
Avoid Hardcoding Credentials: Store sensitive information in environment variables or a .env file.
SMTP Configuration: Use secure SMTP servers and enable two-factor authentication (if supported).
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributions
Contributions, issues, and feature requests are welcome! Feel free to open a pull request or an issue in this repository.

Disclaimer
This script is for educational purposes only. It does not constitute financial advice or guarantee accuracy of stock price data.
