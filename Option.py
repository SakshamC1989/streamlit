import pandas as pd
import yfinance as yf
import datetime
import streamlit as st

from math import log, sqrt, exp
from scipy import stats

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

class put_option:
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