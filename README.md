## Options-Pricing
There are call options with different strike price and their corresponding premium and moneynes for different time intervals
from the current date till the expiry date. Similarly, there are put options. 

- **Inputs:**
1. _User inputs:_
 - Initial Volaitilty %
 - Initial Spot Price
 - Estimated CHANGE in Spot Price of Underlying
 - Change in % Volatility(+/-)
2. _File inputs:_
- strike_price	
- premium	
- current_date	
- expiry_date	
- option_type

**Outputs:**
_File outputs:_
strike_price
new_premium
_Graph ouputs:_
Multiple curves of call and put options with new premium in a single plot
Separate plots for call and put options for different expiry dates
