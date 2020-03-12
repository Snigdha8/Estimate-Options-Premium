import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log , exp , pi , sqrt
from scipy.stats import norm
import collections
from datetime import date

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

###############
def d1(S, K, T, sig, r ):
    t1 = log(S/K)
    t2 = (sig**2)*T/2.0
    t3 = sig * sqrt(T)
    return (t1+t2)/t3

def d2(S, K, T, sig, r):
    t1 = log(S/K)
    t2 =  (sig**2)*T/2.0
    t3 = sig * sqrt(T)
    return (t1 - t2)/t3

def CallPrice(S, K, T, sig, r):
    t1 = S*norm.cdf(d1(S, K, T, sig, r))
    t2 = K*norm.cdf(d2(S ,K ,T, sig, r))
    return exp(-r*T)*(t1 - t2)

def PutPrice(S , K, T, sig, r):
    t1 = K*norm.cdf(-1*d2(S, K, T, sig, r))
    t2 = S*norm.cdf(-1*d1(S, K, T, sig, r))
    return exp(-r*T)(t1-t2)

def Ndash(x):
    return 1/sqrt(2*pi)*exp(-x**2/2)

#Call Greeks
def c_delta(S, K, T, sig, r):
    return norm.cdf(d1(S, K, T, sig, r))

def c_theta(S, K, T, sig, r):
    t1 = (S*norm.pdf(d1(S, K, T, sig, r))*sig)/(2*sqrt(T))
    t2 = r*K*exp(-r*T)*norm.cdf(d2(S, K, T, sig, r))
    return (-t1 - t2 )/252.0

def c_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def c_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per CDay or Per TDay


#Put Greeks
def p_delta(S, K, T, sig, r):
    return norm.cdf(d1(S, K, T, sig, r)) - 1

def p_theta(S, K, T, sig, r):
    t1 = (S*norm.pdf(d1(S, K, T, sig, r))*sig)/(2*sqrt(T))
    t2 = r*K*exp(-r*T)*norm.cdf(d2(S, K, T, sig, r))
    return (-t1 + t2 )/252.0

def p_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def p_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per Cday or per Tday
###############

def numOfDays(date1, date2):
    return (date2-date1).days


#columns = defaultdict(list) # each value in each column is appended to a list

columns = collections.defaultdict(list)
with open('MW-FO-nse50_opt-12-Mar-2020.csv', 'rU') as f:
    reader = csv.reader(f)
    # skip field names
    next(reader)
    for row in csv.reader(f):
        for col, value in enumerate(row):
            columns[col].append(value)

col_index = 2  # for example
print(columns[col_index])



dat1 = "12-03-2020"
dat2 = columns[2][1]

dat1_day = dat1[0]+dat1[1]
print(int(dat1_day))
dat1_mon = dat1[3:5]
print(int(dat1_mon))
dat1_yr = int(dat1[6:10])
print(dat1_yr)
#print(dat1 + " " + dat2)

dat2_day = dat2[0]+dat2[1]
print(int(dat2_day))
dat2_mon = dat2[3:5]
print(int(dat2_mon))
dat2_yr = int(dat2[6:10])
print(dat2_yr)

date1 = date(int(dat1_yr), int(dat1_mon), int(dat1_day))
date2 = date(int(dat2_yr), int(dat2_mon), int(dat2_day))
t = numOfDays(date1, date2)

t = t/365
print(t, " days")
strike_price = columns[4][1]

print(strike_price)
print(type(int(float(strike_price))))
stock_price = int(input('Enter Stock Price '))   #s1
print("stock price is " , stock_price)
ans = d1(stock_price,int(float(strike_price)),t,0.31,0.07)
print(ans)
print("is d1")
ans = d2(10000,int(float(strike_price)),t,0.31,0.07)
print(ans)
print("is d2")

#DELTA
delta = c_delta(stock_price,int(float(strike_price)),t,0.31,0.07)
print("Delta is " , delta)
vega = c_vega(stock_price,int(float(strike_price)),t,0.31,0.07)
print("Vega is " , vega)
theta = c_theta(stock_price,int(float(strike_price)),t,0.31,0.07)
print("Theta is " , theta)

stock_price2 = int(input('Enter the Stock Price s2'))   #s2
print("stock price 2 is " , stock_price2)
old_c_option_price = CallPrice(stock_price,int(float(strike_price)),t,0.31,0.07)

change_in_prem = (stock_price2 - stock_price)*delta
print("change in premium is " , change_in_prem)