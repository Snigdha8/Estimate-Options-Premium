import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log , exp , pi , sqrt 
from scipy.stats import norm

"""
Notations
S : Stock Price
K : Strike Price
T : Time
sig : Volatility
r : risk free interest rate
"""
#Functions
def d1(S, K, T, sig, r ):
    t1 = log(S/K)
    t2 = (r + sig**2/2.0)*T
    t3 = sig * sqrt(T)
    return (t1+t2)/t3

def d2(S, K, T, sig, r):
    t1 = log(S/K)
    t2 = (r - sig**2/2.0)*T
    t3 = sig * sqrt(T)
    return (t1 + t2)/t3

def CallPrice(S, K, T, sig, r):
    t1 = S*norm.cdf(d1(S, K, T, sig, r))
    t2 = K*exp(-r*T)*norm.cdf(d2(S ,K ,T, sig, r))
    return t1 - t2

def PutPrice(S , K, T, sig, r):
    t1 = K*exp(-r*T)
    t2 = S
    t3 = CallPrice(S, K, T, sig , r)
    return t1-t2+t3 
    
#Call Greeks
def c_delta(S,K,T,r,sigma):
    return norm.cdf(d1(S,K,T,r,sigma))

def c_gamma(S,K,T,r,sigma):
    return norm.pdf(d1(S,K,T,r,sigma))/(S*sigma*sqrt(T))

def c_vega(S,K,T,r,sigma):
    return 0.01*(S*norm.pdf(d1(S,K,T,r,sigma))*sqrt(T))

def c_theta(S,K,T,r,sigma):
    return 0.01*(-(S*norm.pdf(d1(S,K,T,r,sigma))*sigma)/(2*sqrt(T)) - r*K*exp(-r*T)*norm.cdf(d2(S,K,T,r,sigma)))


#Put Greeks


