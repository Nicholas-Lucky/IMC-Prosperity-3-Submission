from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

def string_to_dictionary(s):
    s = s.strip("{}")
    s = s.split("]")

    newList = []
    for entry in s:
        if entry != "":
            newList.append((entry + "]").strip(", "))

    d = {}
    for item in newList:
        key_value_pair = item.split(":")
        key = key_value_pair[0].strip(" '")
        
        values = key_value_pair[1].strip(" []").split(",")
        
        for index, value in enumerate(values):
            values[index] = int(value.strip())
        
        d[key] = values
    
    return d

def get_average(prices):
    return sum(prices) / len(prices)

def get_lowest_sell_order(sell_orders):
    lowest_price = 0
    associated_amount = 0

    for index, sell_order in enumerate(sell_orders):
        if index == 0:
            lowest_price = sell_order[0]
            associated_amount = sell_order[1]
            continue
        
        if sell_order[0] < lowest_price:
            lowest_price = sell_order[0]
            associated_amount = sell_order[1]
    
    return (lowest_price, associated_amount)

def get_highest_buy_order(buy_orders):
    highest_price = 0
    associated_amount = 0

    for index, buy_order in enumerate(buy_orders):
        if index == 0:
            highest_price = buy_order[0]
            associated_amount = buy_order[1]
            continue
        
        if buy_order[0] > highest_price:
            highest_price = buy_order[0]
            associated_amount = buy_order[1]
    
    return (highest_price, associated_amount)

# Kelp sell orders goes from 2029-2034

# Rainforest resin sell orders go from 9998-10005

# Squid Ink sell orders goes from 1942-1987
# ^^ first quarter half was 1970-180
# ^^ last quarter was 1960-1970

class Trader:
    
    def run(self, state: TradingState):
        """
        POSITION_LIMITS = {"RAINFOREST_RESIN": 50,
                           "SQUID_INK": 50,
                           "KELP": 50}        

        current_positions = {"RAINFOREST_RESIN": 0,
                             "SQUID_INK": 0,
                             "KELP": 0}
        
        if state.position.get("RAINFOREST_RESIN") is not None:
            current_positions["RAINFOREST_RESIN"] = state.position["RAINFOREST_RESIN"]
        
        if state.position.get("SQUID_INK") is not None:
            current_positions["SQUID_INK"] = state.position["SQUID_INK"]
        
        if state.position.get("KELP") is not None:
            current_positions["KELP"] = state.position["KELP"]
        """

        # Nothing so far (we need to make this I guess?)
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

		# Orders to be placed on exchange matching engine
        result = {}

        sell_order_history = {}
        if state.traderData != "":
            sell_order_history = string_to_dictionary(state.traderData)

        # state.order_depths:
        # keys = products, values = OrderDepth instances

        # Go through each product, for each product
        for product in state.order_depths:
            print(f"Current product: {product}")
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

            """
            # Set to "RAINFOREST_RESIN" price by default
            acceptable_buy_price = 9998.5  # Participant should calculate this value
            acceptable_sell_price = 10002  # Participant should calculate this value

            if product == "SQUID_INK":
                acceptable_buy_price = 1949.5
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2029.5
                acceptable_sell_price = 2032
            """

            # Set to "RAINFOREST_RESIN" price by default
            acceptable_buy_price = 9999  # Participant should calculate this value
            acceptable_sell_price = 10002  # Participant should calculate this value

            if product == "SQUID_INK":
                acceptable_buy_price = 1949.5
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2029.5
                acceptable_sell_price = 2032
            
            if sell_order_history.get(product) is not None:
                acceptable_buy_price = get_average(sell_order_history[product]) - 2
                acceptable_sell_price = get_average(sell_order_history[product]) + 3

            print(f"Acceptable buy price: {acceptable_buy_price}")
            print(f"Acceptable sell price: {acceptable_sell_price}")

            # I guess... how many buy and sell orders?
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # If there are sell orders that exist (if bots are selling)
            if len(order_depth.sell_orders) != 0:
                # Get the price and quantity of the first sell?
                # best_ask = price
                # best_ask_amount = quantity
                best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))
                print(f"Sell orders: {list(order_depth.sell_orders.items())}")

                if sell_order_history.get(product) is None:
                    sell_order_history[product] = [best_ask]
                else:
                    sell_order_history[product].append(best_ask)
                
                # If the bot is selling for less than we expect (wahoo)
                if int(best_ask) < acceptable_buy_price:
                    # Buy some of that I guess
                    print(f"BUY {(-1 * best_ask_amount)} x {best_ask}")
                    orders.append(Order(product, best_ask, -1 * best_ask_amount))

            # If there are buy orders that exist (if bots are buying)
            if len(order_depth.buy_orders) != 0:
                # Get the price and quantity of the first buy?
                # best_bid = price
                # best_bid_amount = quantity
                best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                print(f"Buy orders: {list(order_depth.buy_orders.items())}")

                # If the bot is buying for more than we expect (wahoo)
                if int(best_bid) > acceptable_sell_price:
                    # Sell some of that I guess
                    print(f"SELL {best_bid_amount} x {best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_amount))
                
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = str(sell_order_history)

        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
