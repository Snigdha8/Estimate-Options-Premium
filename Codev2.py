import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log , exp , pi , sqrt 
from scipy.stats import norm
from collections import defaultdict
from datetime import date

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

###############
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
###############

def numOfDays(date1, date2):
    return (date2-date1).days

columns = defaultdict(list) # each value in each column is appended to a list

with open('MW-FO-nse50_opt-12-Mar-2020.csv', encoding="utf8", errors='ignore') as file:
    reader = csv.DictReader(x.replace('\0', '') for x in file) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

#print(columns['Turnover in Lacs'])
print("\n")
print(columns['Date'])

dat1 = "12-Mar-2020"
dat2 = columns['EXPIRY DATE'][0]

dat1_day = dat1[0]+dat1[1]
print(int(dat1_day))
dat1_mon = dat1[3:6]
print(dat1_mon)
dat1_yr = int(dat1[7:11])
print(dat1_yr)
#print(dat1 + " " + dat2)

dat2_day = dat2[0]+dat2[1]
print(int(dat2_day))
dat2_mon = dat2[3:6]
print(dat2_mon)
dat2_yr = int(dat2[7:11])
print(dat2_yr)

date1 = date(int(dat1_yr), month_converter(dat1_mon), int(dat1_day))
date2 = date(int(dat2_yr), month_converter(dat2_mon), int(dat2_day))
t = numOfDays(date1, date2)
print(t, "days")
t = t/31

strike_price = columns['STRIKE PRICE'][0]
#print(int(strike_price))
stock_price = int(input('Enter Stock Price'))
ans = d1(10000,int(strike_price),t,56.87,7)
print(ans)
print("is d1")
ans = d2(10000,int(strike_price),t,56.87,7)
print(ans)
print("is d2")
