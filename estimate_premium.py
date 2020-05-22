import csv
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
from math import log, exp, pi, sqrt
from scipy.stats import norm
import collections
from datetime import date
from recordtype import recordtype
from scipy.interpolate import make_interp_spline, BSpline
import matplotlib.pyplot as plt


###############

def get_files(folder):
    path = os.getcwd()  + "\\" + folder
    files = os.listdir(path) 
    return files

volatility = float(input("Initial Volaitilty %")) / 100.0
spotp = float(input("Initial Spot Price\n"))
#print(spotp)


###############
def d1(S, K, T, sig, r):
        t1 = log(S / K)
        t2 = (sig ** 2) * T / 2.0
        t3 = sig * sqrt(T)
        return (t1 + t2) / t3

def d2(S, K, T, sig, r):
        t1 = log(S / K)
        t2 = (sig ** 2) * T / 2.0
        t3 = sig * sqrt(T)
        return (t1 - t2) / t3

def CallPrice(S, K, T, sig, r):
        t1 = S * norm.cdf(d1(S, K, T, sig, r))
        t2 = K * norm.cdf(d2(S, K, T, sig, r))
        return exp(-r * T) * (t1 - t2)

def PutPrice(S, K, T, sig, r):
	t1 = K * norm.cdf(-1 * d2(S, K, T, sig, r))
	t2 = S * norm.cdf(-1 * d1(S, K, T, sig, r))
	return exp(-r * T)(t1 - t2)



# Call Greeks formulae
def c_delta(S, K, T, sig, r):
        return norm.cdf(d1(S, K, T, sig, r))

def c_theta(S, K, T, sig, r):
        t1 = (S * norm.pdf(d1(S, K, T, sig, r)) * sig) / (2 * sqrt(T))
        t2 = r * K * exp(-r * T) * norm.cdf(d2(S, K, T, sig, r))
        return (-t1 - t2) / 365.0

def c_gamma(S, K, T, sig, r):
        return norm.pdf(d1(S, K, T, sig, r)) / (S * sig * sqrt(T))

def c_vega(S, K, T, sig, r):
        return (S * norm.pdf(d1(S, K, T, sig, r)) * sqrt(T))# Per CDay or Per TDay

def numOfDays(date1, date2):
        return (date2 - date1).days

# Put Greeks formulae
def p_delta(S, K, T, sig, r):
        return norm.cdf(d1(S, K, T, sig, r)) - 1

def p_theta(S, K, T, sig, r):
        t1 = (S * norm.pdf(d1(S, K, T, sig, r)) * sig) / (2 * sqrt(T))
        t2 = r * K * exp(-r * T) * norm.cdf(d2(S, K, T, sig, r))
        return (-t1 + t2) / 365.0

def p_gamma(S, K, T, sig, r):
        return norm.pdf(d1(S, K, T, sig, r)) / (S * sig * sqrt(T))

def p_vega(S, K, T, sig, r):
        return (S * norm.pdf(d1(S, K, T, sig, r)) * sqrt(T))# Per Cday or per Tday###############

# calculate number of days from current date till expiry date
def calculate_t(current_date, expiry_date):
        dat1 = current_date
        dat2 = expiry_date
        
        dat1_day = dat1[0] + dat1[1]
        dat1_mon = dat1[3: 5]
       	dat1_yr = int(dat1[6: 10])
       	
       	dat2_day = dat2[0] + dat2[1]
       	dat2_mon = dat2[3: 5]
       	dat2_yr = int(dat2[6: 10])
       	
       	date1 = date(int(dat1_yr), int(dat1_mon), int(dat1_day))
       	date2 = date(int(dat2_yr), int(dat2_mon), int(dat2_day))
       	t = numOfDays(date1, date2)
       	return (t)

# Plot graphs for call options and put options separately and for each expiry date separately to observe the difference between old premium and new premium
def plot_init_final(files):
    spot_price = spotp
    processed_files = get_files("Graph")
    for pf in processed_files:
        #print(pf[-4:])
        if pf[-4:] == ".jpg":
            processed_files.remove(pf)
	
     
    for f,pf in zip(files , processed_files):
		# Old premium values
        df = pd.read_csv('Data//'+f ,sep = ',', header = None, skiprows = 1)
        before_matrix = df.as_matrix()
        ix = before_matrix[:,0] # Strike Price
        iy = before_matrix[:,1] #Premium
        
        # Estimated 'new premium' values
        df = pd.read_csv('Graph//'+pf ,sep = ',', header = None, skiprows = 1)
        after_matrix = df.as_matrix()
        fx = after_matrix[:,0] # Strike Price
        fy = after_matrix[:,1] #Premium
        
		# Plot for call and put options separately
        # For call options for each expiry date plot initial and final curve together:
        if pf[5] == "c":
            fig = plt.figure()
            plt.plot([spot_price , spot_price ] , [0 , 2000] , 'b' )
			# plotting initial curve
            for x1, x2, y1, y2 in zip(ix, ix[1: ], iy, iy[1: ]):
            	if x1 > spot_price:
            		plt.plot([x1, x2], [y1, y2], 'y', linestyle = '--')
            	elif x1 < spot_price:
            		plt.plot([x1, x2], [y1, y2], 'c' , linestyle = '--' )
            	else:
            		plt.plot([x1, x2], [y1, y2], 'b', marker = '.' )
					
            # plotting final curve
            for x1, x2, y1, y2 in zip(fx, fx[1: ], fy, fy[1: ]):
            	if x1 > spot_price:
            		plt.plot([x1, x2], [y1, y2], 'r', linestyle = '-')
            	elif x1 < spot_price:
            		plt.plot([x1, x2], [y1, y2], 'g' , linestyle = '-' )
            	else:
            		plt.plot([x1, x2], [y1, y2], 'b', marker = '.' )
            fig.suptitle(f, fontsize=16)
            plt.xlabel('strike price', fontsize = 14)
            plt.ylabel('new premium', fontsize = 14)
            fig.savefig('Graph//'+f[0:-4] +'-Before-After' + '.jpg')
        
        else:   # For put options for each expiry date plot initial and final curve together:
            fig = plt.figure()
			# plotting initial curve
            plt.plot([spot_price , spot_price ] , [0 , 2000] , 'b' )
            for x1, x2, y1, y2 in zip(ix, ix[1: ], iy, iy[1: ]):
                if x1 > spot_price:
                    plt.plot([x1, x2], [y1, y2], 'c',linestyle = '--')
                elif x1 < spot_price:
                    plt.plot([x1, x2], [y1, y2], 'y',linestyle = '--')
                else:
                    plt.plot([x1, x2], [y1, y2], 'b', marker = 'o')
            
			# plotting final curve
            for x1, x2, y1, y2 in zip(fx, fx[1: ], fy, fy[1: ]):
                if x1 > spot_price:
                    plt.plot([x1, x2], [y1, y2], 'g',linestyle = '-')
                elif x1 < spot_price:
                    plt.plot([x1, x2], [y1, y2], 'r',linestyle = '-')
                else:
                    plt.plot([x1, x2], [y1, y2], 'b', marker = 'o')
                    
            fig.suptitle(f, fontsize=16)
            plt.xlabel('strike price', fontsize = 14)
            plt.ylabel('new premium', fontsize = 14)
            fig.savefig('Graph//'+f[:-4] +'-Before-After' + '.jpg')
        
        
        
# Plot graphs for call options and put options together so as to compare the 'new premium' for different expiry dates for both options
def plot_multiple(files):
    
    processed_files =  get_files("Graph")
    spot_price = spotp
    graph_data = []
    for pfiles in processed_files:
        pf = pfiles[0:-4]
        pfname = "Graph//" + pf + ".csv"
        
        df = pd.read_csv(pfname ,sep = ',', header = None, skiprows = 1)
        numpy_matrix = df.as_matrix()
        x = numpy_matrix[:,0] # Strike Price
        y = numpy_matrix[:,1] #Premium
        
        graph_data.append([x,y])
        #fig = plt.figure()
        #print(spot_price)
        plt.suptitle("Changes in All Graphs")
        if pf[5] == "c":      	#call options output
            plt.plot([spot_price , spot_price ] , [0 , 2500] , 'b' )
            for x1, x2, y1, y2 in zip(x, x[1: ], y, y[1: ]):
            	if x1 > spot_price:
            		plt.plot([x1, x2], [y1, y2], 'r', linestyle = '--')
            	elif x1 < spot_price:
            		plt.plot([x1, x2], [y1, y2], 'g' , linestyle = '--' )
            	else:
            		plt.plot([x1, x2], [y1, y2], 'b', marker = '.' )
        else:					#put options output	
            plt.plot([spot_price , spot_price ] , [0 , 2000] , 'b' )
            for x1, x2, y1, y2 in zip(x, x[1: ], y, y[1: ]):
                if x1 > spot_price:
                    plt.plot([x1, x2], [y1, y2], 'c',linestyle = '-')
                elif x1 < spot_price:
                    plt.plot([x1, x2], [y1, y2], 'y',linestyle = '-')
                else:
                    plt.plot([x1, x2], [y1, y2], 'b', marker = 'o')
                    
        plt.xlabel('strike price', fontsize = 14)
        plt.ylabel('new premium', fontsize = 14)
        plt.savefig('Graph//'+pf + '.jpg')
        
            
        

'''def plot_output(file_name, option_type):
        spot_price = 9100
        f = file_name[2: -4]
        print(file_name)
        print(f)
        fname = f + ".csv"
        df = pd.read_csv(fname, sep = ',', header = None, skiprows = 1)
        numpy_matrix = df.as_matrix()
        
        y = numpy_matrix[: , 1]# Strike Price
        x = numpy_matrix[: , 0]# Premium
        
        fig = plt.figure()
        if option_type == "call": 
        	for x1, x2, y1, y2 in zip(x, x[1: ], y, y[1: ]):
        		if x1 > spot_price:
        			plt.plot([x1, x2], [y1, y2], 'g')
        		elif x1 < spot_price:
        			plt.plot([x1, x2], [y1, y2], 'r')
        		else:
        			plt.plot([x1, x2], [y1, y2], 'b', marker = '.')
        else:
        	for x1, x2, y1, y2 in zip(x, x[1: ], y, y[1: ]):
        		if x1 > spot_price:
        			plt.plot([x1, x2], [y1, y2], 'r')
        		elif x1 < spot_price:
        			plt.plot([x1, x2], [y1, y2], 'g')
        		else:
        			plt.plot([x1, x2], [y1, y2], 'b', marker = 'o')
        
        fig.suptitle(f, fontsize=16)
        plt.xlabel('strike price', fontsize = 14)
        plt.ylabel('new premium', fontsize = 14)
        fig.savefig(f + '.jpg')
        plt.show()   '''


def call_greeks(database, fname , change_in_spot_price , change_in_volatility , user_date):
        strike_list = []
        new_premium_list = []
        old_premium_list = []
        change_list = []
        curr_date_list = []
        user_date_list = []
        expiry_date_list = []
        
        v = volatility
        
		# All greeks are calculated using greeks formulae for call options.
		# The new premium is calculated as a cascading effect of the greeks as follows:
		# Step 1: 'spot price' and 'volatility' are updated according to their respective changes
		# Step 2: 'gamma' for call options is calculated
		# Step 3: 'old delta' is calculated and using the calculated 'gamma', 'new delta' is calculated
		# Step 4: 'theta' for call options is calculated
		# Step 5: 'vega' for call options is calculated and 'vega effect' is calculated using this 'vega' and 'change in volatility'
        # Step 6: 'new premium' is calculated initially by effect of 'new delta' followed by effect of 'theta' and 'vega'
		# Thus, 'gamma' is used to calculate 'new delta', and further 'new premium' is calculated with the effect of 'new delta', 'theta' and 'vega'
        print("CALL OPTIONS USING GREEKS")
        for d in database:
            num_remaining_days = d.num_remaining_days
            if user_date != "":
                num_day = calculate_t(d.current_date, user_date)
            else:
                num_day = num_remaining_days
            t = d.t
			# Step 1:
            d.spot_price = d.spot_price + change_in_spot_price
            spot_price = d.spot_price
            v = v + change_in_volatility
            
            old_premium_list.append(d.old_premium)
            
            # Step 2:
            gamma = c_gamma(spot_price, int(float(d.strike_price)), t, v, 0.07)
            d.gamma = gamma# print("Gamma is ", gamma)
        	# Step 3:
            old_delta = c_delta(spot_price, int(float(d.strike_price)), t, v, 0.07)
            d.old_delta = old_delta# print("Old Delta is ", old_delta)
            new_delta = old_delta + gamma * change_in_spot_price# print("New Delta is ", new_delta)
            d.new_delta = new_delta
        	# Step 4:
            theta = c_theta(spot_price, int(float(d.strike_price)), t, v, 0.07)# print("Theta is ", theta)
            d.theta = theta
        	# Step 5:
            vega = c_vega(spot_price, int(float(d.strike_price)), t, v, 0.07)
            vega_effect = vega * change_in_volatility
        	# Step 6:
            #print("In Theta, Numday = ",num_day)
            new_premium = int(float(d.old_premium)) + ((old_delta + new_delta) / 2.0) * change_in_spot_price# print("Old premium is ", d.old_premium)# print("(After Gamma effect) New premium is ", new_premium)
            new_premium = new_premium + num_day * theta + vega_effect# addition cuz theta already has a negative value
            if new_premium < 0:
                new_premium = 0
        	
            d.new_premium = new_premium
        	
			# remaining values are added to the database
            strike_list.append(d.strike_price)
            new_premium_list.append(d.new_premium)
            curr_date_list.append(d.current_date)
            user_date_list.append(user_date)
            change = float(d.new_premium)-float(d.old_premium)  
            change_list.append(change)
            expiry_date_list.append(d.expiry_date)
        
		# generate the ouput file for call opions with 'strike price' and its corresponding 'new premium','old premium' , 'net change' , 'current date' , 'date of new premium',  'expiry_date'.
        df = pd.DataFrame(data = {"strike_price": strike_list, "new_premium": new_premium_list ,"Old Premium":old_premium_list ,"Change":change_list , "current_date":curr_date_list , "Date of New Premium":user_date_list , "Expiry Date":expiry_date_list })
        fname1 = fname[0: -4]
        file_name =  "./"+fname1 + "_output.csv"
        df.to_csv(r'Graph//'+file_name, sep = ',', index = False)
        

def put_greeks(database, fname , change_in_spot_price , change_in_volatility , user_date):

        strike_list = []
        new_premium_list = []
        old_premium_list = []
        change_list = []
        curr_date_list = []
        user_date_list = []
        expiry_date_list = []
        
        v = volatility
        
        print("PUT OPTIONS USING GREEKS")
        # Follow the same steps of 'call_greeks' to calculate new premium for put options. 
		# But here the Greeks are calculated using greeks formulae for put options.
        for d in database:
            num_remaining_days = d.num_remaining_days
            if user_date != "":
                num_day = calculate_t(d.current_date, user_date)
            else:
                num_day = num_remaining_days
            t = d.t
			# Step 1:
            d.spot_price = d.spot_price + change_in_spot_price
            spot_price = d.spot_price
            v = v + change_in_volatility
            
            old_premium_list.append(d.old_premium)
        	# Step 2:
            gamma = p_gamma(spot_price, int(float(d.strike_price)), t, v, 0.07)
            d.gamma = gamma
			# Step 3:
            old_delta = p_delta(spot_price, int(float(d.strike_price)), t, v, 0.07)
            d.old_delta = old_delta
            new_delta = old_delta + gamma * change_in_spot_price
            d.new_delta = new_delta
        	# Step 4:
            theta = p_theta(spot_price, int(float(d.strike_price)), t, v, 0.07)# print("Theta is ", theta)
            d.theta = theta
        	# Step 5:
            vega = c_vega(spot_price, int(float(d.strike_price)), t, v, 0.07)
            vega_effect = vega * change_in_volatility
        	# Step 6:
            new_premium = int(float(d.old_premium)) + ((old_delta + new_delta) / 2.0) * change_in_spot_price
            new_premium = new_premium + num_day * theta + vega_effect# addition cuz theta already has a negative value
        	
            if new_premium < 0:
                new_premium = 0
            
            d.new_premium = new_premium
			# remaining values are added to the database
            strike_list.append(d.strike_price)
            new_premium_list.append(d.new_premium)
            curr_date_list.append(d.current_date)
            user_date_list.append(user_date)
            change = float(d.new_premium)-float(d.old_premium)  
            change_list.append(change)
            expiry_date_list.append(d.expiry_date)
        
        
		# generate the ouput file for put options with 'strike price' and its corresponding 'new premium','old premium' , 'net change' , 'current date' , 'date of new premium',  'expiry_date'.
        df = pd.DataFrame(data = {"strike_price": strike_list, "new_premium": new_premium_list ,"Old Premium":old_premium_list ,"Change":change_list , "current_date":curr_date_list , "Date of New Premium":user_date_list , "Expiry Date":expiry_date_list })
        fname1 = fname[0: -4]
        file_name = "./" + fname1 + "_output.csv"
        df.to_csv(r'Graph//'+file_name, sep = ',', index = False)
		

#This function stores all data from the file in a variable called 'database' and returns this 'database'
def process_options(fname, init_spot):
	rows = []
	fields = []
	#MyStruct stores the information for each row in the input file(i.e. values of all columns for each row) and remaining values are filled later
	MyStruct = recordtype("MyStruct", "option_type spot_price num_remaining_days t strike_price old_premium current_date expiry_date moneyness gamma old_delta new_delta theta vega new_premium")
	
	#database stores the information of all the rows in the file
	database = []
	fname =  "Data\\" + fname
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)# print(row)
			strike_price = row[0]
			old_premium = row[1]
			current_date = row[2]
			expiry_date = row[3]
			moneyness = row[4]
			option_type = row[5]
			t = calculate_t(current_date, expiry_date)
			num_remaining_days = t
			#Life of the option(t) = number of days till option maturity/number of trading days(252)
			t = t / 252
			# this 't' is used in calculating greeks
			
			Node = MyStruct(option_type , init_spot, num_remaining_days, t, strike_price, old_premium, current_date, expiry_date, moneyness, "", "", "", "","", "")
			database.append(Node)
			
	return database,option_type


if __name__ == "__main__":
	#read all files from the 'Data' folder
    files = []
    files = get_files("Data")
    print(files)
	
	#'databases' stores the data of all the files
    databases = []
	
	# Each row in the file is either a call or a put option
    for file in files:
        db,otype = process_options(file , spotp)
        databases.append(db)
    
    change_in_spot_price = float(input("Enter the Estimated CHANGE in Spot Price of Underlying\n"))
    change_in_volatility = float(input("Enter Change in % Volatility(+/-)\n")) / 100.0
    
    #Updating the golbal Spot Price and Volatility values 	
    spotp += change_in_spot_price
    volatility += change_in_volatility
    
	# Choice 1: User can go for expiry date if he wants to know the premium on the date of expiry
    # Or Choice 2: The user can enter a date before the expiry date to know the price of the premium 
    rem_flag = int(input("Enter your choice : \n(1)-Expiry day \n(2)-Some Other day\n" ))
    if rem_flag == 2:
        user_date = input("Enter the date for which you want to know the price of premium\nCurrent Date is (20-05-2020)\n")
    else:
        user_date = ""

	#estimating 'new premium' for call and put options
    for d,f in zip(databases,files):
        if f[5] == "c":
            call_greeks(d , f , change_in_spot_price , change_in_volatility , user_date )
        else:
            put_greeks(d , f  , change_in_spot_price , change_in_volatility , user_date )
    
    
    # Plot the output graphs for call and put options together('new premium' vs 'strike price')
    plot_multiple(files)
	# Plot graphs for each output file for a comparison between initial curve and final curve of 'new premium' vs 'strike price'
    plot_init_final(files)
	
	
	
	
	
