#%%
import robin_stocks.robinhood as r
import pandas as pd
import pyotp  # Library to generate TOTP

from dotenv import load_dotenv

load_dotenv()  # load .env
#%%
# Replace these with your Robinhood credentials and TOTP secret key
RH_user = os.getenv('RH_user')
RH_pwd = os.getenv('RH_pwd')
AuthCode = os.getenv('AuthCode')
totp = pyotp.TOTP(AuthCode).now()

print(totp)
#%%

def getPortfolio():
    # GET ALL OPEN POSITIONS ON ROBINHOOD
    positions_data = r.get_open_stock_positions()

    ## Note: This for loop adds the stock ticker to every order, since Robinhood
    ## does not provide that information in the stock orders.
    ## This process is very slow since it is making a GET request for each order.
    for item in positions_data:
        item['symbol'] = r.get_symbol_by_url(item['instrument'])

    # CONVERT PORTFOLIO TO PANDAS + REMOVE USELES COLUMNS
    portfolioDf = pd.DataFrame(positions_data)
    portfolioDfdrop = portfolioDf.drop(
        ['url', 
        'instrument',
        'account', 
        'account_number', 
        'pending_average_buy_price', 
        'intraday_average_buy_price', 
        'intraday_quantity', 
        'shares_held_for_buys', 
        #'shares_held_for_sells', 
        'shares_held_for_stock_grants', 
        'shares_held_for_options_collateral', 
        'shares_held_for_options_events', 
        'shares_pending_from_options_events',
        'shares_available_for_closing_short_position',
        'updated_at',
        'created_at',
        'instrument_id',
        'brokerage_account_type',
        'average_buy_price',
        'quantity',
        'shares_available_for_exercise',
        'shares_available_for_sells',
        'shares_held_for_sells',
        'ipo_allocated_quantity',
        'ipo_dsp_allocated_quantity',
        'avg_cost_affected',
        'avg_cost_affected_reason',
        'is_primary_account',
        'instrument_is_halted',
        'clearing_cost_basis',
        'clearing_running_quantity',
        'clearing_intraday_cost_basis',
        'clearing_intraday_running_quantity',
        'custom_tax_lot_selection_eligible',
        'has_selectable_lots',
        'fetch_tax_lot_related_info',
        ],
        axis=1) 
    
    return portfolioDfdrop
# %%
if __name__ == "__main__":

    # Login
    totp = pyotp.TOTP(AuthCode).now()
    login = r.login(RH_user, RH_pwd, mfa_code=totp)
    print('loggin in')
    print(login)
    listStocks = getPortfolio()
    print(listStocks)
    listStocks = listStocks.sort_values(by="symbol")  # Sort alphabetically
    listStocks.to_csv('stocks.txt', index=False)

# %%

# %%
