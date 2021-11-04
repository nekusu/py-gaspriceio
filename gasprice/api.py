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

from . import shared
from .shared import Estimate, Estimates

import requests
from typing import Dict, List
from datetime import datetime

_api_endpoint = None


def update_endpoint(endpoint: str):
	global _api_endpoint
	_api_endpoint = endpoint


class HistoryItem:
	def __init__(self, timestamp: int, estimates: Estimates):
		self.time = datetime.fromtimestamp(timestamp)
		self.timestamp = timestamp
		self.estimates = estimates

	def __repr__(self):
		return f'<gasprice.api.HistoryItem object ({self.time}, {int(self.estimates.base_fee)} Gwei)>'


class Analysis:
	def __init__(self, transfer: float, token: float, defi: float, nft: float, l2: float, other: float):
		if transfer:
			self.transfer = transfer
		if token:
			self.token = token
		if defi:
			self.defi = defi
		if nft:
			self.nft = nft
		if l2:
			self.l2 = l2
		if other:
			self.other = other

	def __repr__(self):
		return f'<gasprice.api.Analysis object>'


class TxpoolAnalysisItem:
	def __init__(self, total_fees: int, gas_used: int, analysis: Analysis):
		self.total_fees = total_fees
		self.gas_used = gas_used
		self.analysis = analysis

	def __repr__(self):
		return f'<gasprice.api.TxPoolAnalysisItem object>'


class TxpoolAnalysis:
	def __init__(self, base_fee: float, step_size_gas: int, desired_block_gas: int, data: List[TxpoolAnalysisItem]):
		self.base_fee = base_fee
		self.step_size_gas = step_size_gas
		self.desired_block_gas = desired_block_gas
		self.data = data

	def __repr__(self):
		return f'<gasprice.api.TxPoolAnalysis object ({int(self.base_fee)} Gwei)>'


def estimates(countervalue: str='') -> Estimates:
	'''Get gas price estimates
	countervalue: Currency counter for eth price'''
	api_request = requests.get(f'{_api_endpoint}/estimates', params=[('countervalue', countervalue)])
	shared.check_response(api_request)
	return shared.get_estimates(api_request.json()['result'])

def _get_history(history: List) -> List[HistoryItem]:
	data = []
	for item in history:
		estimates = item['estimates']
		instant = estimates['instant']
		fast = estimates['fast']
		eco = estimates['eco']
		data.append(HistoryItem(
			timestamp=item['timestamp'],
			estimates=Estimates(
				instant=Estimate(instant['feeCap'], instant['maxPriorityFee']),
				fast=Estimate(fast['feeCap'], fast['maxPriorityFee']),
				eco=Estimate(eco['feeCap'], eco['maxPriorityFee']),
				base_fee=estimates['baseFee']
			)
		))
	return data

def history_by_minute(duration: int=10800) -> List[HistoryItem]:
	'''Get minute based gas price history
	duration: History duration in seconds <0 to 3600>'''
	api_request = requests.get(f'{_api_endpoint}/historyByMinute', params=[('duration', duration)])
	shared.check_response(api_request)
	return _get_history(api_request.json()['result'])

def history_by_hour(duration: int=2592000) -> List[HistoryItem]:
	'''Get hour based gas price history
	duration: History duration in seconds <0 to 86300 * 30>'''
	api_request = requests.get(f'{_api_endpoint}/historyByHour', params=[('duration', duration)])
	shared.check_response(api_request)
	return _get_history(api_request.json()['result'])

def txpool_by_gas_price() -> Dict:
	'''Get transaction pool data by gas price'''
	api_request = requests.get(f'{_api_endpoint}/txpoolByGasPrice')
	shared.check_response(api_request)
	return api_request.json()['result']

def txpool_analysis() -> TxpoolAnalysis:
	'''Get analysis data on ethereum transaction pool'''
	api_request = requests.get(f'{_api_endpoint}/txpoolAnalysis')
	shared.check_response(api_request)
	result = api_request.json()['result']
	data = []
	categories = ['transfer', 'token', 'defi', 'nft', 'l2', 'other']
	for item in result['data']:
		analysis = item['analysis']
		analysis_data = {}
		for category in categories:
			analysis_data[category] = category in analysis and analysis[category] or None
		data.append(TxpoolAnalysisItem(
			total_fees=item['totalFees'],
			gas_used=item['gasUsed'],
			analysis=Analysis(
				transfer=analysis_data['transfer'],
				token=analysis_data['token'],
				defi=analysis_data['defi'],
				nft=analysis_data['nft'],
				l2=analysis_data['l2'],
				other=analysis_data['other']
			)
		))
	return TxpoolAnalysis(
		base_fee=result['baseFee'],
		step_size_gas=result['stepSizeGas'],
		desired_block_gas=result['desiredBlockGas'],
		data=data
	)
