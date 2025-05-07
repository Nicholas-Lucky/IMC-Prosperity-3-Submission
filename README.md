# IMC Prosperity 3 (2025) Submission
### Note: This writeup is heavily inspired by the [Alpha Animals](https://github.com/CarterT27/imc-prosperity-3), [CMU Physics](https://github.com/chrispyroberts/imc-prosperity-3), and [Byeongguk Kang, Minwoo Kim, and Uihyung Lee](https://github.com/pe049395/IMC-Prosperity-2024)'s writeups.
---
### Team Name: Salty Seagulls

### Team Members:
1. Tyler Thomas ([LinkedIn](https://www.linkedin.com/in/tyler-b-thomas/), [GitHub](https://github.com/TylerThomas6))
2. Lismarys Cabrales ([LinkedIn](https://www.linkedin.com/in/lismaryscabrales/), [GitHub](https://github.com/ikozmicx))
3. Nicholas Lucky ([LinkedIn](https://www.linkedin.com/in/nicholas-lucky/), [GitHub](https://github.com/Nicholas-Lucky))
---
## Overview
#### [IMC's Prosperity 2025](https://prosperity.imc.com/) is an annual trading challenge that challenges participants to program an algorithm to trade various goods on a virtual trading market — with the goal of gaining as much profit, in the form of SeaShells, as possible. In addition to the algorithm, there are manual trading challenges that allow participants to gain additional seashells. The competition spans five rounds, with each round adding new products for our trading algorithms to consider, and a new manual trading challenge to attempt. This year is the third iteration of the competition (Prosperity 3), and lasted from April 7th, 2025 to April 22nd, 2025. This is our first year in the competition, and we focused on learning and gaining a (at least) general understanding of the competition and the programming and skills required to perform in both the trading algorithm and manual trading challenges.

#### Further details on this year's competition can be found on the [Prosperity 3 Wiki](https://imc-prosperity.notion.site/Prosperity-3-Wiki-19ee8453a09380529731c4e6fb697ea4).
---
## Round 1
### Algorithmic Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/Round-1-19ee8453a09381d18b78cf3c21e5d916), Round 1 introduced us to our first three tradable products: `RAINFOREST_RESIN`, `KELP`, and `SQUID_INK`. These products seem to have varying levels of stability, with `RAINFOREST_RESIN` having relatively stable values, `KELP` having some variation, and `SQUID_INK` having the most volatility of the three products. `RAINFOREST_RESIN` has a position limit of `50`, `KELP` has a position limit of `50`, and `SQUID_INK` has a position limit of `50`.

#### We began with the [IMC_prototype.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/IMC_prototype.py) provided to us by Mark Brezina in the IMC Prosperity Discrod server. After learning the logic of the code, we experimented with different thresholds to buy and sell the tradable products. Realizing that our code needed to be adaptable, we attempted to store and track the sell orders that we encountered in a `sell_order_history` dictionary. We also created a `buy_order_history` dictionary to use alongside `sell_order_history` when calculating buy and sell thresholds for `SQUID_INK`, as suggested by Tyler Thomas. For `sell_order_history`, we would append the lowest sell order of the iteration, while we would append the highest buy order of the iteration to `buy_order_history`. These dictionaries could then be converted into strings to be put in `traderData` and converted back to dictionaries at the start of future iterations.

```python
# In round_1.py

# At the start of the Trader class
sell_order_history = {}
buy_order_history = {}

if state.traderData != "":
    order_histories = string_to_list_of_dictionaries(state.traderData)
    sell_order_history = order_histories[0]
    buy_order_history = order_histories[1]

# ...perform calculations

# At the end of the Trader class
newData = []
newData.append(sell_order_history)
newData.append(buy_order_history)

traderData = str(newData)
```

#### In subsequent iterations, we took the average of the sell orders in `sell_order_history` for each product, and used this average as our threshold for buying and selling. For round 1, we actually ended up not using `buy_order_history` for calculating thresholds for `SQUID_INK`, I think because of time constraints.

```python
# In round_1.py

if product == "KELP":
    #acceptable_buy_price = get_average(sell_order_history[product])
    acceptable_sell_price = get_average(sell_order_history[product]) + 3
```

#### We also attempted to add slight offsets for the buy/sell thresholds for some products, which we hoped would allow us to sell a product at a higher price than what we bought the product for. While most of these offsets were hardcoded based on rough estimates for how volatile each product would be, we added an adaptable offset for `SQUID_INK`, as we felt that such an offset would benefit `SQUID_INK` the most due to the product's high volatility. This adaptable offset was calculated by subtracting the 100th most recent sell order from the most recent sell order, dividing the difference by 6, and taking the absolute value. This result was then added to the threshold to sell, with the idea being that:
1. Quickly rising sell orders should raise our threshold to sell, potentially allowing us to sell `SQUID_INK` at higher prices
2. Stagnating sell orders should maintain our threshold to sell as it is
3. Quickly falling sell orders should also raise our threshold to sell, as we would not want to sell `SQUID_INK` at these prices

```python
# In round_1.py

# In hindsight, index_one and index_two probably should've been switched, but it still be fine given the absolute value 
index_one = 0
index_two = 99
if len(sell_order_history[product]) < 100:
    index_two = len(sell_order_history[product]) - 1

sell_offset = (sell_order_history[product][index_one] - sell_order_history[product][index_two]) / 6
if sell_offset < 0:
    sell_offset *= -1

# ...later in the code...
if product == "SQUID_INK":
    # ...
    acceptable_sell_price = sell_order_ave + sell_offset
```

#### For the first iteration of the `Trader` class, we hardcoded many of the thresholds for all three products. We originally wanted these hardcoded values to only be used in the first iteration, however we found that they provided us with more profit when used in future iterations as well. As a result, assuming that the historical data given would reflect on the final submission data (which we later learned is not the case), we ended up sticking with these hardcoded values for many of our thresholds.

```python
# In round_1.py

# "RAINFOREST_RESIN" price, hardcoded for now
acceptable_buy_price = 9999  # Participant should calculate this value
acceptable_sell_price = 10001  # Participant should calculate this value

if product == "SQUID_INK":
    acceptable_buy_price = 1950
    acceptable_sell_price = 1970

elif product == "KELP":
    acceptable_buy_price = 2030
    acceptable_sell_price = 2032

# ...later in the code; we commented out the lines for calculating thresholds
#if product == "RAINFOREST_RESIN":
#acceptable_buy_price = get_average(sell_order_history[product]) - 2
#acceptable_sell_price = get_average(sell_order_history[product]) + 1
```

#### These are the results of our Round 1 algorithm:

![round_1_algorithm_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_algorithm_results_1.gif)
![round_1_algorithm_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_algorithm_results_2.gif)

#### While we did gain profit from our algorithm, we recognized that some of our buy and sell thresholds were still hardcoded for some of the products. As a result, we attempted to make our thresholds and algorithms more adaptable in future rounds.

### Manual Trading
#### As mentioned in [Round 1 of the wiki](https://imc-prosperity.notion.site/Round-1-19ee8453a09381d18b78cf3c21e5d916), the manual trading challenge for Round 1 was a series of currency trades that we needed to. We began with 500,000 SeaShells, with SeaShells as our starting currency, and we needed to trade this initial amount to different currencies before ending with a trade back to SeaShells. We amount we get from trading to another currency is determined by the multiplier of the trade, as determined by:

| Products/Currencies | Snowballs | Pizzas | Silicon Nuggets | SeaShells |
|:-------------------:|:---------:|:------:|:---------------:|:---------:|
| Snowballs           | 1         | 1.45   | 0.52            | 0.72      |
| Pizzas              | 0.7       | 1      | 0.31            | 0.48      |
| Silicon Nuggets     | 1.95      | 3.1    | 1               | 1.49      |
| SeaShells           | 1.34      | 1.98   | 0.64            | 1         |

#### ^^ For example, if we have 500,000 SeaShells and trade to Pizzas, we will receive 500,000 x 1.98 = 990,000 Pizzas

#### Our goal is to perform 5 trades (with the 5th trade being back to SeaShells) that will ideally net us a profit in SeaShells — the general format is shown below. It is worth noting that we are allowed to trade a currency into the same currency (the resulting multiplier would be 1), and we are allowed to trade into a specific currency more than once.

| Initial Currency | Currency to Trade to |
|:----------------:|:--------------------:|
| SeaShells        | product_1            |
| product_1        | product_2            |
| product_2        | product_3            |
| product_3        | product_4            |
| product_4        | SeaShells            |

#### Our work for this round's manual trading can be viewed in [round_1_manual_trading.py](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/round_1/round_1_manual_trading.py). Assuming that the 5th trade will always be to SeaShells, we would essentially have 4 trades, each of which has 4 possible currencies to choose from. As a result, we assumed there would be a maximum of 4<sup>4</sup> = 256 possible "paths" for this challenge. Hence, we felt that it was possible to use brute force to determine the optimal series of trades that would yield the highest number of SeaShells. After fixing errors identified by Tyler Thomas, our round_1_manual_trading.py yielded the following path:

![round_1_manual_code_output](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_code_output.jpg)

#### ^^ With a revenue of 544,340.16 SeaShells, and an initial amount of 500,000 SeaShells, our profit from this series of trades would be 544,340.16 - 500,000 = 44,340.16 SeaShells

#### These are the results of our Round 1 manual trading challenge:

![round_1_manual_results_1](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_1.gif)
![round_1_manual_results_2](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_2.jpg)
![round_1_manual_results_3](https://github.com/Nicholas-Lucky/IMC-Prosperity-3-Submission/blob/main/readme_embeds/round_1_manual_results_3.jpg)

#### ^^ It seems that the number 1 team in Manual after Round 1, RBQ, also had a profit of 44,340 SeaShells, which supports the claim that we seemed to have submitted the optimal series of trades for Round 1's manual trading challenge.

---
## Round 2
### Algorithmic Trading
#### As mentioned in [Round 2 of the wiki](https://imc-prosperity.notion.site/Round-2-19ee8453a09381a580cdf9c0468e9bc8), Round 2 introduced us to 5 new tradeable products: `CROISSANTS`, `JAMS`, `DJEMBES`, `PICNIC_BASKET1`, and `PICNIC_BASKET2`. `PICNIC_BASKET1` and `PICNIC_BASKET2` are a little different in that they contain multiple products: `PICNIC_BASKET1` contains 6 `CROISSANTS`, 3 `JAMS`, and 1 `DJEMBES`, while `PICNIC_BASKET2` contains 4 `CROISSANTS` and 2 `JAMS`.

#### `CROISSANTS` has a position limit of `250`, `JAMS` has a position limit of `350`, `DJEMBES` has a position limit of `60`, `PICNIC_BASKET1` has a position limit of `60`, and `PICNIC_BASKET2` has a position limit of `100`.

#### We used a similar strategy for the `CROISSANTS`, `JAMS`, and `DJEMBES`, using the average of the `sell_order_history` for our buy and sell offsets alongside some offsets to ideally allow buying at lower prices and selling at higher prices. For the thresholds to sell, we used the same adaptable offset calculations that were used for `SQUID_INK`.

```python
# In round_2.py

if product == "CROISSANTS":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "DJEMBES":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset

if product == "JAMS":
    acceptable_buy_price = get_average(sell_order_history[product]) - 4
    acceptable_sell_price = get_average(sell_order_history[product]) + sell_offset
```

#### We also used a similar strategy for `PICNIC_BASKET1` and `PICNIC_BASKET2`, however, instead of using the `sell_order_history` of `PICNIC_BASKET1` and `PICNIC_BASKET2`, we broke the baskets down into the individual products they contained. The thresholds for `PICNIC_BASKET1` would be calculated by summing the `sell_order_history` average of `CROISSANTS` multiplied by 6, the `sell_order_history` average of `JAMS` multiplied by 3, and the `sell_order_history` average of `DJEMBES`. The thresholds for `PICNIC_BASKET2` would be calculated by summing the `sell_order_history` average of `CROISSANTS` multiplied by 4 and the `sell_order_history` average of `JAMS` multiplied by 2.

```python
# In round_2.py

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
```

#### We also attempted to add "crash detectors" that can be used to warn the algorithm of an incoming crash. We discussed two possible "crash detectors" to implement:
1. If incoming prices for a product are significantly higher than the historical average, be ready to sell everything we have for that product
2. If incoming prices for a product are significantly lower than prices some number of iterations ago (for example, 5 iterations ago), be ready to sell everything we have for that product

#### We decided that our "crash detectors" should follow the first implementation (point 1), as, while recognizing the possibility of missing the potential upsides of continuously rising trends, it would be ideal for our algorithm to be proactive rather than reactive. As a result, we added four conditions to compare incoming prices and, in the event of one of these conditions being true, signal the algorithm to sell all it currently has for a given product.

```python
# In round_2.py

# Condition 1: Sell order is slightly higher than a recent average (small-dip checker)
# Condition 2: Sell order is too high above the historical average (big-dip checker)
# Condition 3: Sell order of PICNIC_BASKET1 and PICNIC_BASKET2 is slightly higher than a recent average (small-dip checker)
# Condition 4: Sell order of DJEMBES is slightly higher than a recent average (small-dip checker)
# Condition 5 (not used): Sell order is too low vs 5 sell orders ago

# ...later in the code...
if ((condition_one or condition_two or condition_three or condition_four or condition_five) and (sell_order_history.get(product) is not None)):
    # Sell everything for that product
```

#### We also attempted to work with the current positions and position limits of the products, however, due to time constraints, we were not able to implement relevant functionality that we found meaningful. We were able to begin implementation to track current positions for our products, and store these values in `traderData` for future iterations.

```python
# In round_2.py

current_positions = {}

if state.traderData != "":
    order_histories = convert_trading_data(state.traderData)
    # ...
    current_positions = order_histories[2]

# ...

position = 0
    if current_positions.get(product) is not None:
        position = current_positions[product]
    else:
        current_positions[product] = 0

# ...

if int(best_bid) > acceptable_sell_price:
    # Sell some of the product
    # ...
    position -= best_bid_amount

# ...

newData = []
# ...
newData.append(current_positions)

# String value holding Trader state data required. 
# It will be delivered as TradingState.traderData on next execution.
traderData = str(newData)
```

### Manual Trading
#### Info on manual round

#### Info on what we did
---
## Round 3
### Algorithmic Trading
#### Info on algo round

#### Info on what we did

### Manual Trading
#### Info on manual round

#### Info on what we did
---
## Round 4
### Algorithmic Trading
#### Info on algo round

#### Info on what we did

### Manual Trading
#### Info on manual round

#### Info on what we did
---
## Round 5
### Algorithmic Trading
#### Info on algo round

#### Info on what we did

### Manual Trading
#### Info on manual round

#### Info on what we did
---
## Results and Rankings
<table>
    <tr align="center">
        <th></th>
        <th colspan="4">Rank</th>
    </tr>
    <tr align="center">
        <th>Round</th>
        <th>Overall</th>
        <th>Manual</th>
        <th>Algorithmic</th>
        <th>Country</th>
    </tr>
    <tr align="center">
        <td>Round 1</td>
        <td>1022</td>
        <td>715</td>
        <td>1121</td>
        <td>293</td>
    </tr>
    <tr align="center">
        <td>Round 2</td>
        <td>2971</td>
        <td>1508</td>
        <td>2764</td>
        <td>815</td>
    </tr>
    <tr align="center">
        <td>Round 3</td>
        <td>4036</td>
        <td>1298</td>
        <td>2907</td>
        <td>1013</td>
    </tr>
    <tr align="center">
        <td>Round 4</td>
        <td>3537</td>
        <td>Didn't Record</td>
        <td>Didn't Record</td>
        <td>Didn't Record</td>
    </tr>
    <tr align="center">
        <td>Round 5</td>
        <td>1330</td>
        <td>92</td>
        <td>2875</td>
        <td>369</td>
    </tr>
</table>
