import csv
import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log , exp , pi , sqrt
from scipy.stats import norm
import collections
from datetime import date
from recordtype import recordtype
from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.pyplot as plt
import pprint
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
    return (-t1 - t2 )/365.0

def c_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def c_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per CDay or Per TDay
    
def numOfDays(date1, date2):
    return (date2-date1).days
    

#Put Greeks
def p_delta(S, K, T, sig, r):
    return norm.cdf(d1(S, K, T, sig, r)) - 1

def p_theta(S, K, T, sig, r):
    t1 = (S*norm.pdf(d1(S, K, T, sig, r))*sig)/(2*sqrt(T))
    t2 = r*K*exp(-r*T)*norm.cdf(d2(S, K, T, sig, r))
    return (-t1 + t2 )/365.0

def p_gamma(S, K, T, sig, r):
    return norm.pdf(d1(S, K, T, sig, r))/(S*sig*sqrt(T))

def p_vega(S, K, T, sig, r):
    return (S*norm.pdf(d1(S, K, T, sig, r))*sqrt(T))
    #Per Cday or per Tday
###############
    
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

def plot_output(file_name):
	
    f = file_name[2:-4]
    fname = f + ".csv"
    df=pd.read_csv(fname, sep=',',header=None, skiprows=1)
    numpy_matrix = df.as_matrix()
    
    x = numpy_matrix[:,1]
    y = numpy_matrix[:,0]
    print(x)
    print(y)
    plt.plot(y , x)
    #fig.suptitle(f, fontsize=16)
    plt.xlabel('strike price', fontsize=14)
    plt.ylabel('new premium', fontsize=14)
    #fig.savefig(f + '.jpg')
    plt.show()


def call_greeks(database , fname):
    strike_list = []
    new_premium_list = []
    print("CALL OPTIONS USING GREEKS") 
    change_in_spot_price = float(input("Enter Change in the Estimated change in Spot Price of Underlying"))
    change_in_volatility = float(input("Enter Change  in Volatility"))
    for d in database:
        num_remaining_days = d.num_remaining_days
        t = d.t
        spot_price = d.spot_price
        
        gamma = c_gamma(spot_price,int(float(d.strike_price)),t,0.51,0.07)
        d.gamma = gamma
        print("Gamma is " , gamma)
		
        old_delta = c_delta(spot_price,int(float(d.strike_price)),t,0.51,0.07)
        d.old_delta = old_delta
        print("Old Delta is " , old_delta) 
		
        new_delta = old_delta + gamma*change_in_spot_price
        print("New Delta is " , new_delta)
        d.new_delta = new_delta
		
        theta = c_theta(spot_price,int(float(d.strike_price)),t,0.51,0.07)
        print("Theta is " , theta)
        d.theta = theta
		
        new_premium = int(float(d.old_premium)) + new_delta*change_in_spot_price
        print("Old premium is " , d.old_premium)
        print("(After Gamma effect) New premium is " , new_premium)
        new_premium = new_premium + num_remaining_days*theta #addition cuz theta already has a negative value
		#theta is coming 2 digits hence I think it must be divided by 100
        print("(After Theta effect) New premium is " , new_premium)
        d.new_premium = new_premium
        
        strike_list.append(d.strike_price)
        new_premium_list.append(d.new_premium)
        print(d)
        print()
    
    df = pd.DataFrame(data={"strike_price": strike_list, "premium": new_premium_list})
    fname1 = fname[0:-4]
    file_name = "./" + fname1 + "_output.csv"
    df.to_csv(file_name, sep=',',index=False)
    plot_output(file_name)


def put_greeks(database, num_remaining_days, t, spot_price, change_in_spot_price, fname):
	
	strike_list = []
	new_premium_list = []
	
	print("PUT OPTIONS USING GREEKS") 
	for d in database:
		
		gamma = p_gamma(spot_price,int(float(d.strike_price)),t,0.51,0.07)
		d.gamma = gamma
		print("Gamma is " , gamma)
		
		old_delta = p_delta(spot_price,int(float(d.strike_price)),t,0.51,0.07)
		d.old_delta = old_delta
		print("Old Delta is " , old_delta) 
		
		new_delta = old_delta + gamma*change_in_spot_price
		print("New Delta is " , new_delta)
		d.new_delta = new_delta
		
		theta = p_theta(spot_price,int(float(d.strike_price)),t,0.51,0.07)
		print("Theta is " , theta)
		d.theta = theta
		
		new_premium = int(float(d.old_premium)) + new_delta*change_in_spot_price
		print("Old premium is " , d.old_premium)
		print("(After Gamma effect) New premium is " , new_premium)
		new_premium = new_premium + num_remaining_days*theta #addition cuz theta already has a negative value
		#theta is coming 2 digits hence I think it must be divided by 100
		print("(After Theta effect) New premium is " , new_premium)
		d.new_premium = new_premium
		
		strike_list.append(d.strike_price)
		new_premium_list.append(d.new_premium)
		print(d)
		print()
	
	df = pd.DataFrame(data={"strike_price": strike_list, "premium": new_premium_list})
	fname1 = fname[0:-4]
	file_name = "./" + fname1 + "_output.csv"
	df.to_csv(file_name, sep=',',index=False)
	plot_output(file_name)


def process_options(fname , init_spot):
    rows = [] 
    fields = []
    MyStruct = recordtype("MyStruct", "spot_price num_remaining_days t strike_price old_premium current_date expiry_date moneyness gamma old_delta new_delta theta new_premium")
    database = []
    print("-------------------------------------------------------------------------------------------------------")
    print("FOR FILE ", fname)
    print("-------------------------------------------------------------------------------------------------------")
    with open(fname, 'r') as csvfile:  
        csvreader = csv.reader(csvfile) 
        fields = next(csvreader)
        for row in csvreader: 
            rows.append(row) #print(row)
            strike_price = row[0]
            old_premium = row[1]
            current_date = row[2]
            expiry_date = row[3]
            moneyness = row[4]
            
            t = calculate_t(current_date, expiry_date)
            num_remaining_days = t
            t = t/365
            
            Node = MyStruct(init_spot,num_remaining_days,t,strike_price, old_premium, current_date, expiry_date, moneyness, "", "", "", "", "")
            database.append(Node)
            
            #print("No. of days till expiry are " , num_remaining_days)
            
        #print(database)
        return database
        
        
		#print(*database, sep="\n")
	



if __name__ == "__main__":

    fname1 = "file3_call_options.csv"
    spot_price = float(input("Enter Initial Spot Price"))
    db3c = process_options(fname1,spot_price)
    print(db3c)
    
    steps = int(input("Enter Number of Iterations"))
    it = 0    
    while it < steps :
        call_greeks( db3c , fname1)
        it += 1 
    print()
    print("******************************************************************************************************")
    print()
    """fname2 = "file3_put_options.csv"
    db3f = process_options(fname2 ,9095,10,"put")
    put_greeks(db3f , fname2)
    
    print("******************************************************************************************************")
    print("******************************************************************************************************")
    
    #process_options("file1_put_options.csv",9700,200,"put");
    print()
    print("******************************************************************************************************")
    print()
    #process_options("file2_put_options.csv",9700,200,"put");"""






















