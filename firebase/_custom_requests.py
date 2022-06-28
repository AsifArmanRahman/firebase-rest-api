
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from requests import Session
from requests import adapters


def _custom_request(max_retries=None):
	""" Custom Session with N retries.

	Incase a request was not completed successfully due to minor
	errors, such as connection failures due to unreliable networks;
	or server side overload to proceed the request, retrying the
	request couple of times might solve it, without raising an error.

	if no value is sent through the function,
	`max_retries` is set to 3.

	:param max_retries: number of retries.
	:type max_retries: int | None
	:return: custom session
	:rtype: Session
	"""

	session = Session()
	adapter = adapters.HTTPAdapter(max_retries=max_retries)

	for scheme in ('http://', 'https://'):
		session.mount(scheme, adapter)

	return session
