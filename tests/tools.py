
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from tests import config
from firebase import initialize_app


def make_db(service_account=False):
	if service_account:
		c = config.SERVICE_CONFIG
	else:
		c = config.SIMPLE_CONFIG

	return initialize_app(c).database()
