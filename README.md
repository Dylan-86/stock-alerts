## Setup

1.  **Clone this repository**:

    ` git clone https://github.com/your-username/stock-price-alert.git` 
    
    ` cd stock-price-alert` 
    
2.  **Install dependencies with Poetry**: Run the following command to install all required dependencies in a virtual environment:
    

    `poetry install` 
    
3.  **Create a `.env` file**: Add your email configuration and other sensitive data in a `.env` file in the root directory. Example:
    
    
    `EMAIL_ADDRESS=your-email@example.com
    EMAIL_PASSWORD=your-email-password
    TO_EMAIL=recipient-email@example.com
    SMTP_SERVER=smtp.your-email-provider.com
    SMTP_PORT=587` 
    
    
4.  **Prepare the `stocks.csv` file**: Create a `stocks.csv` file in the following format:
    
    
    `stock,SL,TP1
    AAPL,140,160
    MSFT,250,280
    GOOGL,2700,3000` 
    

-   **stock**: Stock ticker symbol (e.g., AAPL for Apple, MSFT for Microsoft).
-   **SL**: Support level (price below which you want to get alerted).
-   **TP1**: Target price (price above which you want to get alerted).

## Usage

1.  **Run the script manually**: Use Poetry to run the script within the virtual environment:
    
    
    `poetry run python stock_alert.py` 
    
2.  **Schedule regular checks**: To run the script at regular intervals, consider using a task scheduler:
    
    -   **Unix-based systems**: Use `cron`.
    -   **Windows**: Use Task Scheduler.

## How It Works

1.  **Loading Stocks**: The script reads stock tickers and thresholds from the `stocks.csv` file.
2.  **Market Hours Check**: Prices are checked only during US stock market hours.
3.  **Price Fetching**: Uses the `yfinance` library to fetch the latest closing price of each stock.
4.  **Alert Triggering**: Compares the price with SL and TP1 thresholds and logs alerts.
5.  **Email Notifications**: Sends a consolidated email with all alerts.

## Example Output

### Console Log


    Current price of AAPL: 150.0
    AAPL is within the range 140-160.
    Current price of MSFT: 240.0
    Alert: MSFT price below 250. Current price: 240.0

### Email



    `Subject: Stock Price Alerts
    
    Alert: MSFT price below 250. Current price: 240.0` 

## Customization

-   Modify the market hours logic in `is_market_open()` if needed.
-   Adjust the retry logic or delay in `get_stock_price()` as per your requirements.
-   Add new alert conditions based on other metrics (e.g., volume, percentage change).

## Security

-   **Avoid Hardcoding Credentials**: Use environment variables or a `.env` file for sensitive data.
-   **SMTP Configuration**: Use secure SMTP servers,

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributions

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or an issue in this repository.

## Disclaimer

This script is for educational purposes only. It does not constitute financial advice or guarantee accuracy of stock price data.

Last update 12/12/2024.
