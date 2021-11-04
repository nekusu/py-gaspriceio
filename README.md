# py-gaspriceio

[![PyPI Latest Release](https://img.shields.io/pypi/v/gaspriceio.svg)](https://pypi.org/project/gaspriceio)

Structured Python wrapper for [GasPrice.io](https://gasprice.io/) API.

# Installation

Install **py-gaspriceio**.

## Using pip
```sh
pip3 install gaspriceio
```

## Build from source
```sh
git clone https://github.com/nekusu/py-gaspriceio.git
cd py-gaspriceio
pip3 install -r requirements.txt
sudo make install  # or `sudo python3 setup.py install`
```

# Usage

Quick example:
```python
>>> from gasprice import *
>>> from gasprice import utils
>>> from threading import Thread

# Estimates
>>> estimates_ = estimates()
>>> estimates_.base_fee
64.318551651
>>> estimates_.eth_price
3828.13
>>> estimates_.instant.fee_cap
73.75040681610001

# History (30 days)
>>> history = history_by_hour()
>>> history[0].estimates.base_fee
70.531785439

# Txpool Analysis
>>> txpool = txpool_analysis()
>>> txpool.base_fee
54.18059689
>>> utils.format_decimals(txpool.data[0].total_fees)
'0.225 ETH'
>>> txpool.data[0].analysis.transfer
0.126

# Lowest base fee
>>> lowest_fee = utils.lowest_base_fee(history)
>>> lowest_fee.estimates.base_fee
50.18255170481667
>>> str(lowest_fee.time)
'2021-10-18 07:00:00'

# Cheapest day
>>> utils.cheapest_day_average(history)
'Saturday'

# Realtime estimates (websocket)
>>> rt = realtime(print)
>>> Thread(target=rt.run).start()
<gasprice.shared.Estimates object (Instant: 140, Fast: 139, Eco: 101)>
<gasprice.shared.Estimates object (Instant: 129, Fast: 128, Eco: 95)>
<gasprice.shared.Estimates object (Instant: 138, Fast: 137, Eco: 95)>
>>> rt.close()
```

For better understanding, I recommend reading the [GasPrice API documentation](https://gasprice.io/docs/api). All variables/functions names were renamed from **camelCase** to **snake_case**.

# License
MIT - Copyright (c) 2021
