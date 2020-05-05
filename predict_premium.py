import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log , exp , pi , sqrt
from scipy.stats import norm
import collections
from datetime import date

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
    
def numOfDays(date1, date2):
    return (date2-date1).days
    
    
    
#spot price = 2700 ; change in spot price = 200 ; expiry date = 28-05-2020
# current date = 07-05-2020 (we will have to display for different current dates)
def calculate_t(current_date, expiry_date):
	dat1 = current_date
	dat2 = expiry_date

	dat1_day = dat1[0]+dat1[1]
	dat1_mon = dat1[3:5]
	dat1_yr = int(dat1[6:10])

	dat2_day = dat2[0]+dat2[1]
	dat2_mon = dat2[3:5]
	dat2_yr = int(dat2[6:10])

	date1 = date(int(dat1_yr), int(dat1_mon), int(dat1_day))
	date2 = date(int(dat2_yr), int(dat2_mon), int(dat2_day))
	t = numOfDays(date1, date2)
	return(t)




'''delta = c_delta(spot_price,int(float(strike_price)),t,0.51,0.07)
print("Delta is " , delta)
vega = c_vega(spot_price,int(float(strike_price)),t,0.51,0.07)
print("Vega is " , vega)
theta = c_theta(spot_price,int(float(strike_price)),t,0.51,0.07)
print("Theta is " , theta)
gamma = c_gamma(spot_price,int(float(strike_price)),t,0.51,0.07)
print("Gamma is " , gamma)'''

def process_files(fname, spot_price, change_in_spot_price):
	
	rows = [] 
	fields = []

	with open(fname, 'r') as csvfile: 
		# creating a csv reader object 
		csvreader = csv.reader(csvfile) 
	
		# extracting field names through first row 
		fields = next(csvreader) 

		# extracting each data row one by one 
		for row in csvreader: 
			rows.append(row) 
			print(row)
			strike_price = row[0]
			old_premium = row[1]
			current_date = row[2]
			expiry_date = row[3]
			moneyness = row[4]
		
			t = calculate_t(current_date, expiry_date)
			orig_t = t
			t = t/365
			print("No. of days till expiry are " , orig_t)
			gamma = c_gamma(spot_price,int(float(strike_price)),t,0.51,0.07)
			print("Gamma is " , gamma)
			old_delta = c_delta(spot_price,int(float(strike_price)),t,0.51,0.07)
			print("Old Delta is " , old_delta) 
			new_delta = old_delta + gamma*change_in_spot_price
			print("New Delta is " , new_delta)
			theta = c_theta(spot_price,int(float(strike_price)),t,0.51,0.07)
			print("Theta is " , theta)
			new_premium = int(float(old_premium)) + new_delta*change_in_spot_price
			print("Old premium is " , old_premium)
			print("(After Gamma effect) New premium is " , new_premium)
			new_premium = new_premium + orig_t*theta*0.01 #addition cuz theta already has a negative value
			#theta is coming 2 digits hence I think it must be divided by 100
			print("(After Theta effect) New premium is " , new_premium)
			print()
	
process_files("file1.csv",9700,200);
print()
print("******************************************************************************************************")
print()
process_files("file2.csv",9700,200);
