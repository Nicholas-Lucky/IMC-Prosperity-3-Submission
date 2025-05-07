# IMC Prosperity 3 (2025) Submission
### Note: This writeup is heavily inspired by the [Alpha Animals](https://github.com/CarterT27/imc-prosperity-3) and [Byeongguk Kang, Minwoo Kim, and Uihyung Lee](https://github.com/pe049395/IMC-Prosperity-2024)'s writeups.
---
### Team Name: Salty Seagulls

### Team Members:
1. Tyler Thomas ([LinkedIn](https://www.linkedin.com/in/tyler-b-thomas/), [GitHub](https://github.com/TylerThomas6))
2. Lismarys Cabrales ([LinkedIn](https://www.linkedin.com/in/lismaryscabrales/), [GitHub](https://github.com/ikozmicx))
3. Nicholas Lucky ([LinkedIn](https://www.linkedin.com/in/nicholas-lucky/), [GitHub](https://github.com/Nicholas-Lucky))
---
## Overview
#### [IMC's Prosperity 2025](https://prosperity.imc.com/) is an annual trading challenge that challenges participants to program an algorithm to trade various goods on a virtual trading market — with the goal of gaining as much profit, in the form of seashells, as possible. In addition to the algorithm, there are manual trading challenges that allow participants to gain additional seashells. The competition spans five rounds, with each round adding new products for our trading algorithms to consider, and a new manual trading challenge to attempt. This year is the third iteration of the competition (Prosperity 3), and lasted from April 7th, 2025 to April 22nd, 2025. This is our first year in the competition, and we focused on learning and gaining a (at least) general understanding of the competition and the programming and skills required to perform in both the trading algorithm and manual trading challenges.

#### Further details on this year's competition can be found on the [Prosperity 3 Wiki](https://imc-prosperity.notion.site/Prosperity-3-Wiki-19ee8453a09380529731c4e6fb697ea4).
---
## Round 1
### Algorithmic Trading
#### Round 1 introduced us to our first three tradable products: `RAINFOREST_RESIN`, `KELP`, and `SQUID_INK`. These products seem to have varying levels of stability, with `RAINFOREST_RESIN` having relatively stable values, `KELP` having some variation, and `SQUID_INK` having the most volatility of the three products. `RAINFOREST_RESIN` has a position limit of `50`, `KELP` has a position limit of `50`, and `SQUID_INK` has a position limit of `50`.

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

#### In subsequent iterations, we took the average of the sell orders in `sell_order_history` for each product, and used this average as our threshold for buying and selling; we also attempted to add slight offsets for the buy/sell thresholds for some products, which we hoped would allow us to sell a product at a higher price than what we bought the product for. For round 1, we actually ended up not using `buy_order_history` for calculating thresholds for `SQUID_INK`, I think because of time constraints.

```python
# In round_1.py

if product == "KELP":
    #acceptable_buy_price = get_average(sell_order_history[product])
    acceptable_sell_price = get_average(sell_order_history[product]) + 3
```

#### For the first iteration of the `Trader` class, we hardcoded thresholds for all three products. We originally wanted these hardcoded values to only be used in the first iteration, however we found that they provided us with more profit when used in future iterations as well. As a result, assuming that the historical data given would reflect on the final submission data (which we later learned is not the case), we ended up sticking with these hardcoded values for many of our thresholds. 

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

### Manual Trading
#### Info on manual round

#### Info on what we did
---
## Round 2
### Algorithmic Trading
#### Info on algo round

#### Info on what we did

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
