from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

def get_orders(s):
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

def get_positions(s):
    s = s.strip("{}")
    s = s.split(",")
    
    newList = []
    for entry in s:
        if entry != "":
            newList.append((entry).strip())

    d = {}
    for item in newList:
        key_value_pair = item.split(":")
        key = key_value_pair[0].strip("'")
        
        value = int(key_value_pair[1].strip())
        d[key] = value
    
    return d

def convert_trading_data(s):
    s = s.strip("[]")
    s = s.split("}")

    dList = []
    for entry in s:
        if entry != "":
            dList.append((entry + "}").strip(", "))
    
    sell_orders = get_orders(dList[0])
    buy_orders = get_orders(dList[1])
    positions = get_positions(dList[2])

    dList[0] = sell_orders
    dList[1] = buy_orders
    dList[2] = positions
    
    return dList

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

def buy_to_bot(orders, current_position, position_limit, product, best_ask, best_ask_amount):
    if current_position - best_ask_amount <= position_limit:
        orders.append(Order(product, best_ask, -1 * best_ask_amount))

def sell_to_bot(orders, current_position, position_limit, product, best_bid, best_bid_amount):
    if current_position - best_bid_amount >= (-1 * position_limit):
        orders.append(Order(product, best_bid, -1 * best_bid_amount))

class Trader:
    def run(self, state: TradingState):
        POSITION_LIMITS = {
            "RAINFOREST_RESIN": 50,
            "KELP": 50,
            "SQUID_INK": 50,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60,
            "PICNIC_BASKET1": 60,
            "PICNIC_BASKET2": 100,
        }

        #print("traderData: " + state.traderData)
        #print("Observations: " + str(state.observations))
        #print(f"Own trades: {state.own_trades}")

		# Orders to be placed on exchange matching engine
        result = {}

        sell_order_history = {}
        buy_order_history = {}
        current_positions = {}
        if state.traderData != "":
            order_histories = convert_trading_data(state.traderData)
            sell_order_history = order_histories[0]
            buy_order_history = order_histories[1]
            current_positions = order_histories[2]
        
        # state.order_depths:
        # keys = products, values = OrderDepth instances

        # Go through each product, for each product
        for product in state.order_depths:
            print(f"Current product: {product}")
            
            position = 0
            if current_positions.get(product) is not None:
                position = current_positions[product]
            else:
                current_positions[product] = 0
                
            print(f"Current position: {current_positions[product]}")
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

            if product == "RAINFOREST_RESIN":
                acceptable_buy_price = 9999
                acceptable_sell_price = 10001

            elif product == "SQUID_INK":
                acceptable_buy_price = 1950
                acceptable_sell_price = 1970
            
            elif product == "KELP":
                acceptable_buy_price = 2030
                acceptable_sell_price = 2032

            elif product == "CROISSANTS":
                acceptable_buy_price = 4015
                acceptable_sell_price = 4024

            elif product == "DJEMBES":
                acceptable_buy_price = 13450
                acceptable_sell_price = 13485

            elif product == "JAMS":
                acceptable_buy_price = 6625
                acceptable_sell_price = 6638

            elif product == "PICNIC_BASKET1":
                acceptable_buy_price = 59000
                acceptable_sell_price = 59010
            
            elif product == "PICNIC_BASKET2":
                acceptable_buy_price = 59000
                acceptable_sell_price = 59010
            
            if sell_order_history.get(product) is not None:
                index_one = 0
                index_two = 99
                if len(sell_order_history[product]) < 100:
                    index_two = len(sell_order_history[product]) - 1
                
                sell_offset = (sell_order_history[product][index_one] - sell_order_history[product][index_two]) / 6
                if sell_offset < 0:
                    sell_offset *= -1

                if product == "RAINFOREST_RESIN":
                    acceptable_buy_price = get_average(sell_order_history[product]) - 1
                    acceptable_sell_price = get_average(sell_order_history[product]) + 1
                
                if product == "KELP":
                    acceptable_buy_price = get_average(sell_order_history[product])
                    acceptable_sell_price = get_average(sell_order_history[product]) + 3

                if product == "SQUID_INK":
                    sell_order_ave = get_average(sell_order_history[product])
                    buy_order_ave = get_average(buy_order_history[product])

                    acceptable_buy_price = sell_order_ave - 1
                    acceptable_sell_price = sell_order_ave + sell_offset

                if product == "CROISSANTS":
                    acceptable_buy_price = get_average(sell_order_history[product]) - 4
                    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
                
                if product == "DJEMBES":
                    acceptable_buy_price = get_average(sell_order_history[product]) - 4
                    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
                
                if product == "JAMS":
                    acceptable_buy_price = get_average(sell_order_history[product]) - 4
                    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
                
                if product == "PICNIC_BASKET1":
                    croissants = (get_average(sell_order_history["CROISSANTS"])) * 6
                    jams = (get_average(sell_order_history["JAMS"])) * 3
                    djembe = get_average(sell_order_history["DJEMBES"])

                    acceptable_buy_price = croissants + jams + djembe - 5
                    acceptable_sell_price = acceptable_buy_price + sell_offset

                if product == "PICNIC_BASKET2":
                    croissants = (get_average(sell_order_history["CROISSANTS"])) * 4
                    jams = (get_average(sell_order_history["JAMS"])) * 2

                    acceptable_buy_price = croissants + jams - 5
                    acceptable_sell_price = acceptable_buy_price + sell_offset

            print(f"Acceptable buy price: {acceptable_buy_price}")
            print(f"Acceptable sell price: {acceptable_sell_price}")

            # I guess... how many buy and sell orders?
            print(f"Buy Order depth: {len(order_depth.buy_orders)}, Sell order depth: {len(order_depth.sell_orders)}")

            # Make conditions (for a crash or not) in which we would want to sell everything
            best_ask, best_ask_amount = get_lowest_sell_order(list(order_depth.sell_orders.items()))

            # Condition 1: Sell order is a slightly higher than a recent average (small-dip checker)
            # Condition 2: Sell order is a too high above the historical average (big-dip checker)
            # Condition 3: Sell order of PICNIC_BASKET1 and PICNIC_BASKET2 is a slightly higher than a recent average (small-dip checker)
            # Condition 4: Sell order of DJEMBES is a slightly higher than a recent average (small-dip checker)
            # Condition 5: Sell order is too low vs 5 sell orders ago
            # Either needs to be true for us to sell everything
            condition_one = False
            condition_two = False
            condition_three = False
            condition_four = False
            condition_five = False

            # Set the condition values
            if sell_order_history.get(product) is not None:
                # Condition 1 (small-dip checker)
                recents = sell_order_history[product]
                if len(recents) > 20:
                    recents = recents[0:20]
                
                recents_average = get_average(recents) 
                print(f"recents_average: {recents_average}")

                condition_one = best_ask > (recents_average * 1.001)
                
                # Condition 2 (big-dip checker)
                historical_average = get_average(sell_order_history[product]) 
                condition_two = best_ask > (historical_average * 1.001)

                # Condition 3 (baskets small-dip checker)
                if product == "PICNIC_BASKET1" or product == "PICNIC_BASKET2":
                    recents = sell_order_history[product]
                    if len(recents) > 10:
                        recents = recents[0:10]
                    
                    recents_average = get_average(recents) 
                    print(f"recents_average: {recents_average}")

                    condition_three = best_ask > (recents_average * 1.001)

                # Condition 4 (djembes small-dip checker)
                if product == "DJEMBES":
                    recents = sell_order_history[product]
                    if len(recents) > 40:
                        recents = recents[-40:]
                    
                    recents_average = get_average(recents) 
                    print(f"recents_average: {recents_average}")

                    condition_four = best_ask > (recents_average * 1.001)

                # Condition 4
                if len(sell_order_history[product]) >= 5:
                    fifth_previous_sell_order = sell_order_history[product][-5]
                    #condition_five = best_ask < (fifth_previous_sell_order * 0.98)

            if ((condition_one or condition_two or condition_three or condition_four or condition_five) and (sell_order_history.get(product) is not None)):
                print("CRASHING... CRASHING!!!")
                sell_order_history[product].append(best_ask)

                # Sell everything (sell to all buy orders until position <= 0)
                for buy_order in list(order_depth.buy_orders.items()):
                    bid, bid_amount = buy_order
                    if position <= 0:
                        break
                    
                    # In case I guess (ideally I would think that we sell everything until our position is back to 0)
                    if position - bid_amount <= 0:
                        orders.append(Order(product, bid, -1 * position))

                    else:
                        orders.append(Order(product, bid, -1 * bid_amount))
                    
                    position -= bid_amount

            # If there is no crazy decrease, resume!
            else:
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
                        # Default: Keep the past 150 orders
                        if len(sell_order_history[product]) > 150:
                            sell_order_history[product].pop(0)
                        
                        # or best_ask < (sell_order_history[product][-5] * 0.92)

                        # Previously: Big jumps: Keep the past 35 orders
                        # Big jumps: Keep the past 80 orders
                        # TODO: Maybe make the multiplier 1.001?

                        # If there are more than 75 sell orders in the sell order history (max is 150)
                        if len(sell_order_history[product]) > 75:
                            # If the current sell order price is 0.5% above the 10th most recent sell order price
                            if best_ask > (sell_order_history[product][-10] * 1.005):
                                print("BIG JUMP!!!")

                                # Reduce the sell order history by 70 (remove the 70 oldest)
                                for i in range(70, len(sell_order_history[product])):
                                    sell_order_history[product].pop(0)

                        sell_order_history[product].append(best_ask)
                    
                    # If the bot is selling for less than we expect (wahoo)
                    if int(best_ask) < acceptable_buy_price:
                        # Buy some of that I guess
                        print(f"BUY {(-1 * best_ask_amount)} x {best_ask}")
                        buy_to_bot(orders, position, POSITION_LIMITS[product], product, best_ask, best_ask_amount)
                        #orders.append(Order(product, best_ask, -1 * best_ask_amount))
                        position += best_ask_amount

                # If there are buy orders that exist (if bots are buying)
                if len(order_depth.buy_orders) != 0:
                    # Get the price and quantity of the first buy?
                    # best_bid = price
                    # best_bid_amount = quantity
                    best_bid, best_bid_amount = get_highest_buy_order(list(order_depth.buy_orders.items()))
                    print(f"Buy orders: {list(order_depth.buy_orders.items())}")
                    
                    # TODO: Could allow for all products to have a buy order in case
                    if product == "SQUID_INK":
                        if buy_order_history.get(product) is None:
                            buy_order_history[product] = [best_bid]
                        else:
                            buy_order_history[product].append(best_bid)

                    # If the bot is buying for more than we expect (wahoo)
                    if int(best_bid) > acceptable_sell_price:
                        # Sell some of that I guess
                        print(f"SELL {best_bid_amount} x {best_bid}")
                        #sell_to_bot(orders, position, POSITION_LIMITS[product], product, best_bid, best_bid_amount)
                        orders.append(Order(product, best_bid, -1 * best_bid_amount))
                        position -= best_bid_amount
                
            # This is still in the "for product in state.order_depths" for loop
            # After we make our orders, put those orders in result for that respective product
            result[product] = orders
            current_positions[product] = position

        newData = []
        newData.append(sell_order_history)
        newData.append(buy_order_history)
        newData.append(current_positions)

        # String value holding Trader state data required. 
        # It will be delivered as TradingState.traderData on next execution.
        traderData = str(newData)

        # Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
