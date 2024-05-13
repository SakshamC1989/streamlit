import pandas as pd
import yfinance as yf
import datetime
from math import log, sqrt, exp
from scipy import stats

import streamlit as st

class call_option(object):
    ''' Class for European call options in BSM model.

    Attributes
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term

    Methods
    =======
    value : float
        return present value of call option
    vega : float
        return Vega of call option
    imp_vol: float
        return implied volatility given option quote
    delta : float
        return delta of call option
    theta : float
        return theta of call option
    gamma : float
        return gamma of call option
    rho : float
        return rho of call option
    '''

    def __init__(self, S0, K, T, r, sigma):
        self.S0 = float(S0)
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def value(self):
        ''' Returns option value. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        value = (self.S0 * stats.norm.cdf(d1, 0.0, 1.0)
            - self.K * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0, 1.0))
        return value

    def vega(self):
        pass
        # ''' Returns Vega of ...

class put_option(object):
    ''' Class for European put options in BSM model.

        Attributes
        ==========
        S0 : float
            initial stock/index level
        K : float
            strike price
        T : float
            maturity (in year fractions)
        r : float
            constant risk-free short rate
        sigma : float
            volatility factor in diffusion term

        Methods
        =======
        value : float
            return present value of put option
        vega : float
            return Vega of put option
        imp_vol: float
            return implied volatility given option quote
        delta : float
            return delta of put option
        theta : float
            return theta of put option
        gamma : float
            return gamma of put option
        rho : float
            return rho of put option
        '''

    def __init__(self, S0, K, T, r, sigma):
        self.S0 = float(S0)
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def value(self):
        ''' Returns option value. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        value = (-self.S0 * stats.norm.cdf(-d1, 0.0, 1.0)
            + self.K * exp(-self.r * self.T) * stats.norm.cdf(-d2, 0.0, 1.0))
        return value

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

expiry = st.date_input("Enter Expiry", datetime.date(2024, 12, 31))
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
        price = call_option(S0=stock, K=strike, T=dte, r=rate, sigma=vol)
    else:
        price = put_option(S0=stock, K=strike, T=dte, r=rate, sigma=vol)
    st.write("The ", type , " option price should be ", round(price.value(), 3))
# else:
#     st.write("Input again")

pass