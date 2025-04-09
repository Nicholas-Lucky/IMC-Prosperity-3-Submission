# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 09:37:47 2025

@author: Mark Brezina
"""

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    def run(self, state: TradingState):
        # Nothing so far (we need to make this I guess?)
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))


	# Orders to be placed on exchange matching engine
        result = {}

        # state.order_depths:
        # keys = products, values = OrderDepth instances

        # Go through each product, for each product
        for product in state.order_depths:
            print(f"HI {product}")
            """
            OrderDepth contains the collection of all outstanding buy and sell orders
            (or “quotes”) that were sent by the trading bots for a certain symbol

            buy_orders and sell_orders dictionaries:
            Key = price associated with the order
            Value = total volume on that price level
            """
            order_depth: OrderDepth = state.order_depths[product]

            # Make a list of orders
            orders: List[Order] = []

            acceptable_price = 10  # Participant should calculate this value

            print(f"Acceptable price: {acceptable_price}")

            # I guess... how many buy and sell orders?
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # If there are sell orders that exist (if bots are selling)
            if len(order_depth.sell_orders) != 0:
                # Get the price and quantity of the first sell?
                # best_ask = price
                # best_ask_amount = quantity
                best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                
                # If the bot is selling for less than we expect (wahoo)
                if int(best_ask) < acceptable_price:
                    # Buy some of that I guess
                    print(f"BUY {(-1 * best_ask_amount)} x {best_ask}")
                    orders.append(Order(product, best_ask, -1 * best_ask_amount))

            # If there are buy orders that exist (if bots are buying)
            if len(order_depth.buy_orders) != 0:
                # Get the price and quantity of the first buy?
                # best_bid = price
                # best_bid_amount = quantity
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]

                # If the bot is buying for more than we expect (wahoo)
                if int(best_bid) > acceptable_price:
                    # Sell some of that I guess
                    print(f"SELL {best_bid_amount} x {best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_amount))
            
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders

		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
