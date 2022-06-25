
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from requests import Session


class KeepAuthSession(Session):
	"""
	A session that doesn't drop Authentication on redirects between domains.
	"""

	def rebuild_auth(self, prepared_request, response):
		pass
