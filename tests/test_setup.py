
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


import pytest

from tests.tools import initiate_app_with_service_account_file, make_auth, make_db, make_storage


def test_initiate_app_with_service_account_file():
	with pytest.raises(FileNotFoundError) as exc_info:
		initiate_app_with_service_account_file()
	assert "No such file or directory: 'firebase-adminsdk.json'" in str(exc_info.value)


def test_setup_auth():
	auth = make_auth()
	user = auth.sign_in_anonymous()

	assert auth.delete_user_account(user['idToken'])


def test_setup_auth_admin():
	auth = make_auth(True)
	user = auth.sign_in_anonymous()

	assert auth.delete_user_account(user['idToken'])


def test_setup_db():
	db = make_db(True)

	assert db.get()


def test_setup_storage():
	storage = make_storage()

	with pytest.raises(AttributeError) as exc_info:
		storage.list_files()
	assert 'bucket' in str(exc_info.value)


def test_setup_storage_admin():
	storage = make_storage(True)

	assert storage.list_files()
