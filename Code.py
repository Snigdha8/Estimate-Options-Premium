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

def Ndash(x):
    return 1/sqrt(2*pi)*exp(-x**2/2)

#Call Greeks
def c_delta(S, K, T, sig, r):
    return norm.cdf(d1(S, K, T, sig, r))

def c_theta(S, K, T, sig, r):
    t1 = (S*norm.pdf(d1(S, K, T, sig, r))*sig)/(2*sqrt(T))
    t2 = r*K*exp(-r*T)*norm.cdf(d2(S, K, T, sig, r))
    return (-t1 - t2 )/254.0

def c_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def c_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per CDay or Per TDay


#Put Greeks
def p_delta(S, K, T, sig, r):
    return norm.cdf(-d1(S, K, T, sig, r)) - 1

def p_theta(S, K, T, sig, r):
    t1 = (S*norm.pdf(d1(S, K, T, sig, r))*sig)/(2*sqrt(T))
    t2 = r*K*exp(-r*T)*norm.cdf(d2(S, K, T, sig, r))
    return (-t1 + t2 )/254.0

def p_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def p_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per Cday or per Tday


