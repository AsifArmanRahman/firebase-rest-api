#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest

from tests.tools import make_auth, make_db, make_storage
from tests.config import TEST_USER_EMAIL, TEST_USER_PASSWORD


@pytest.fixture(scope='session')
def db():
	# To make it easier to test, we keep the test restricted to firebase_tests
	# Because of the current mutations on calls, we return it as a function.
	try:
		yield lambda: make_db(service_account=True).child('firebase_tests')
	finally:
		make_db(service_account=True).child('firebase_tests').remove()


@pytest.fixture(scope='session')
def auth():
	return make_auth(True)


@pytest.fixture(scope='session')
def email():
	return TEST_USER_EMAIL


@pytest.fixture(scope='session')
def password():
	return TEST_USER_PASSWORD


@pytest.fixture(scope='session')
def storage():
	# To make it easier to test, we keep the test restricted to firebase_tests
	# Because of the current mutations on calls, we return it as a function.
	return make_storage(service_account=True)
