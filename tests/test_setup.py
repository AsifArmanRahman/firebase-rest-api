
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest

from tests.tools import initiate_app_with_service_account_file, make_auth, make_db, make_storage


@pytest.mark.xfail
def test_initiate_app_with_service_account_file():
	assert initiate_app_with_service_account_file()


def test_setup_auth():
	auth = make_auth(True)
	user = auth.sign_in_anonymous()

	assert auth.delete_user_account(user['idToken'])


def test_setup_db():
	db = make_db(True)

	assert db.get()


def test_setup_storage():
	storage = make_storage(True)

	assert storage.list_files()
