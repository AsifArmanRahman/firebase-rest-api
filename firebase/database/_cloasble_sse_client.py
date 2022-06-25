
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import socket

from ._custom_sse_client import SSEClient


class ClosableSSEClient(SSEClient):

	def __init__(self, *args, **kwargs):
		self.should_connect = True
		super(ClosableSSEClient, self).__init__(*args, **kwargs)

	def _connect(self):
		if self.should_connect:
			super(ClosableSSEClient, self)._connect()
		else:
			raise StopIteration()

	def close(self):
		self.should_connect = False
		self.retry = 0

		self.resp.raw._fp.fp.raw._sock.shutdown(socket.SHUT_RDWR)
		self.resp.raw._fp.fp.raw._sock.close()
