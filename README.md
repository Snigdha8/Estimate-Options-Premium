## Options-Pricing
There are call options with different strike price and their corresponding premium and moneyness for different time intervals
from the current date till the expiry date. Similarly, there are put options. 

- **Inputs:**
1. _User inputs:_<br/>
Initial Volaitilty %<br/>
Initial Spot Price<br/>
Estimated CHANGE in Spot Price of Underlying<br/>
Change in % Volatility(+/-)<br/>
Number of days before or till expiry for which user wants to know the option premium<br/>
2. _File inputs:_<br/>
strike_price	<br/>
premium	<br/>
current_date	<br/>
expiry_date	<br/>
option_type<br/>

- **Outputs:**
1. _File outputs:_<br/>
strike_price & new_premium in csv file<br/>
2. _Graph ouputs:_<br/>
Multiple curves of call and put options with new premium in a single plot<br/>
Separate plots for call and put options for different expiry dates<br/>
<br/>
<br/>
From the Black-Scholes-Merton Model, values of greeks are calculated for call and put options.<br/>
Initial spot price and volatility are updated according to user's view of change in spot price and volatility.<br/>
For call and put options both the following sequence of the effect of greeks is followed to calculate new premium:<br/>
1: 'spot price' and 'volatility' are updated according to their respective changes<br/>
2: 'gamma' is calculated from options greeks formulae<br/>
3: 'old delta' is calculated from options greeks formulae and using the calculated 'gamma', 'new delta' is calculated<br/>
4: 'theta' for options is calculated from options greeks formulae<br/>
5: 'vega' for options is calculated from options greeks formulae and 'vega effect' is calculated using this 'vega' and 'change in volatility'<br/>
6: 'new premium' is calculated initially by effect of 'new delta' followed by effect of 'theta' and 'vega'<br/>
<br/>
Thus, 'gamma' is used to calculate 'new delta', and further 'new premium' is calculated with the effect of 'new delta', 'theta' and 'vega'.<br/>

The new premium for all strike prices are stored in the output csv file.<br/>
Graphs for call options and put options together plotted so as to compare the 'new premium' for different expiry dates for both options.<br/>
Graphs for call options and put options are plotted separately and for each expiry date individually to observe the difference between old premium and new premium.<br/>
