#
#   Software distrubuted under MIT License (MIT)
#
#   Copyright (c) 2021 nekusu
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

from .api import HistoryItem

from typing import List


def format_decimals(value: int, prec: int=6) -> str:
	amount = round(value / 10 ** 18, prec)
	if amount == int(amount):
		amount = int(amount)
	return f'{amount} ETH'

def lowest_base_fee(history: List[HistoryItem]) -> HistoryItem:
	lowest_fee_item = None
	lowest_fee = float('inf')
	for item in history:
		if item.estimates.base_fee < lowest_fee:
			lowest_fee = item.estimates.base_fee
			lowest_fee_item = item
	return lowest_fee_item

def cheapest_day_average(history: List[HistoryItem]) -> str:
	cheapest_day = None
	lowest_fee = float('inf')
	days = {}
	for item in history:
		day = item.time.strftime('%A')
		if day not in days:
			days[day] = { 'fees': 0, 'times': 0 }
		days[day]['fees'] += item.estimates.base_fee
		days[day]['times'] += 1
	for day in days.keys():
		average_fee = days[day]['fees'] / days[day]['times']
		if average_fee < lowest_fee:
			lowest_fee = average_fee
			cheapest_day = day
	return cheapest_day
