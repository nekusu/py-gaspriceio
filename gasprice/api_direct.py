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

import websocket, ssl, json
from typing import Callable

websocket.setdefaulttimeout(5)
_api_endpoint = None


def update_endpoint(endpoint: str):
	global _api_endpoint
	_api_endpoint = endpoint


class WebSocketConnection:
	def __init__(self, endpoint: str, on_message: Callable, on_error: Callable, on_close: Callable):
		self.endpoint = endpoint
		self.on_message = on_message
		self.on_error = on_error
		self.on_close = on_close
		self.ws = websocket.WebSocketApp(
			url=f'{_api_endpoint}/{self.endpoint}',
			header={
				'Sec-WebSocket-Extensions': 'permessage-deflate',
				'Sec-Fetch-Dest': 'websocket',
				'Sec-Fetch-Mode': 'websocket',
				'Sec-Fetch-Site': 'same-site',
				'Connection': 'keep-alive',
				'Pragma': 'no-cache',
				'Cache-Control': 'no-cache',
				'Upgrade': 'websocket'
			},
			on_message=self._on_message,
			on_error=self._on_error,
			on_close=self._on_close
		)

	def _on_message(self, ws, message):
		self.on_message(shared.get_estimates(json.loads(message)['data']))

	def _on_error(self, ws, error):
		self.on_error(error)

	def _on_close(self, ws, close_status_code, close_msg):
		if close_status_code or close_msg:
			self.on_close(close_status_code, close_msg)

	def run(self):
		self.ws.run_forever(sslopt={ "cert_reqs": ssl.CERT_NONE }, skip_utf8_validation=True)

	def close(self):
		self.ws.close()

	def __repr__(self):
		return f'<gasprice.api_direct.WebSocketConnection object ({self.endpoint})>'


def realtime(on_message: Callable, on_error: Callable=print, on_close: Callable=print) -> WebSocketConnection:
	'''Get realtime gas price estimates
	on_message (estimates): Callback object called when received data
	on_error (error): Callback object called when received error
	on_close (close_status_code, close_msg): Callback object called when connection is closed'''
	return WebSocketConnection('realtime', on_message, on_error, on_close)
