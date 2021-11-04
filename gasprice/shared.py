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

from . import exceptions


class Estimate:
	def __init__(self, fee_cap: float, max_priority_fee: int):
		self.fee_cap = fee_cap
		self.max_priority_fee = max_priority_fee

	def __repr__(self):
		return f'<gasprice.shared.Estimate object ({int(self.fee_cap)} Gwei)>'


class Estimates:
	def __init__(self, instant: Estimate, fast: Estimate, eco: Estimate, base_fee: float, eth_price: float=None):
		self.instant = instant
		self.fast = fast
		self.eco = eco
		self.base_fee = base_fee
		if eth_price:
			self.eth_price = eth_price

	def __repr__(self):
		return f'<gasprice.shared.Estimates object '\
			f'(Instant: {int(self.instant.fee_cap)}, Fast: {int(self.fast.fee_cap)}, Eco: {int(self.eco.fee_cap)})>'


def check_response(request):
	if request.status_code not in [200, 400]:
		raise(exceptions.UnexpectedStatusCode(
			f'API Returned unexpected status code: {request.status_code} '
			f'{request.reason} (Request URL: {request.url})'
		))

	error = request.json()['error']
	if error:
		raise(exceptions.APIError(f'API Returned error: {error} (Request URL: {request.url})'))

def get_estimates(data):
	instant = data['instant']
	fast = data['fast']
	eco = data['eco']
	return Estimates(
		instant=Estimate(instant['feeCap'], instant['maxPriorityFee']),
		fast=Estimate(fast['feeCap'], fast['maxPriorityFee']),
		eco=Estimate(eco['feeCap'], eco['maxPriorityFee']),
		base_fee=data['baseFee'],
		eth_price=data['ethPrice']
	)
