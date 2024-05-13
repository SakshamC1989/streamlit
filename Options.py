import pandas as pd
import yfinance as yf
import datetime
import streamlit as st
import Git.streamlit.Option as opt_obj

def options_chain(symbol):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.concat([opt.calls,opt.puts])
        opt['expirationDate'] = e
        options = pd.concat([options,opt], ignore_index=True)

    # Bizarre error in yfinance that gives the wrong expiration date
    # Add 1 day to get the correct expiration date
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days = 1)
    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options

st.set_page_config(
    page_title="Options_Monitor",
    page_icon="🧊",
    layout="wide")
st.markdown("# Options Screener")
ticker = st.text_input("Enter ticker", "GOOG")
df = options_chain(ticker)
st.dataframe(df)

st.markdown("# Options Pricer")

type = st.radio(
    "Option type",
    ["Call", "Put"]
    )

stock = st.text_input("Enter stock price", 0)
stock = float(stock)

strike = st.text_input("Enter strike price", 0)
strike = float(strike)

expiry = st.date_input("Enter Expiry", datetime.date(2019, 7, 6))
dte = expiry - datetime.date.today()
dte = dte.days
dte = dte/365

rate = st.text_input("Enter interest rate", 0.03)
rate = float(rate)

vol = st.text_input("Enter implied volatility", 0.03)
vol = float(vol)

# st.button("Reset", type="primary")
if st.button("Calculate"):
    if type=='Call':
        price = opt_obj.call_option(S0=stock, K=strike, T=dte, r=rate, sigma=vol)
    else:
        price = opt_obj.put_option(S0=stock, K=strike, T=dte, r=rate, sigma=vol)
    st.write("The ", type , " option price should be ", round(price.value(), 3))
# else:
#     st.write("Input again")

pass