#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest

from tests.tools import make_auth, make_db, make_ds, make_storage
from tests.config import (
	TEST_USER_EMAIL, TEST_USER_PASSWORD,
	TEST_USER_EMAIL_2, TEST_USER_PASSWORD_2
)


@pytest.fixture(scope='session')
def auth():
	return make_auth()


@pytest.fixture(scope='session')
def auth_admin():
	return make_auth(True)


@pytest.fixture(scope='session')
def db():
	# To make it easier to test, we keep the test restricted to firebase_tests
	# Because of the current mutations on calls, we return it as a function.
	try:
		yield lambda: make_db(service_account=True).child('firebase_tests')
	finally:
		make_db(service_account=True).child('firebase_tests').remove()


@pytest.fixture(scope='session')
def email():
	return TEST_USER_EMAIL

@pytest.fixture(scope='session')
def email_2():
	return TEST_USER_EMAIL_2

@pytest.fixture(scope='session')
def ds():
	return make_ds()


@pytest.fixture(scope='session')
def ds_admin():
	return make_ds(True)


@pytest.fixture(scope='session')
def password():
	return TEST_USER_PASSWORD

@pytest.fixture(scope='session')
def password_2():
	return TEST_USER_PASSWORD_2

@pytest.fixture(scope='session')
def storage():
	return make_storage()


@pytest.fixture(scope='session')
def storage_admin():
	return make_storage(service_account=True)
