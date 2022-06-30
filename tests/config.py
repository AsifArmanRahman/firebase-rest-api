
#   Copyright (c) 2022 Asif Arman Rahman
#   Licensed under MIT (https://github.com/AsifArmanRahman/firebase/blob/main/LICENSE)

# --------------------------------------------------------------------------------------


from decouple import config


# get this from firebase console
# go to project settings, general tab and click "Add Firebase to your web app"
SIMPLE_CONFIG = {
	"apiKey": config('FIREBASE_API_KEY'),
	"authDomain": config('FIREBASE_AUTH_DOMAIN'),
	"databaseURL": config('FIREBASE_DATABASE_URL'),
	"storageBucket": config('FIREBASE_STORAGE_BUCKET'),
}

# get this in json file from firebase console
# go to project settings, service accounts tab and click generate new private key
SERVICE_ACCOUNT = {
	"type": 'service_account',
	"project_id": config('FIREBASE_SERVICE_ACCOUNT_PROJECT_ID'),
	"private_key_id": config('FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY_ID'),
	"private_key": config('FIREBASE_SERVICE_ACCOUNT_PRIVATE_KEY').replace('\\n', '\n'),
	"client_email": config('FIREBASE_SERVICE_ACCOUNT_CLIENT_EMAIL'),
	"client_id": config('FIREBASE_SERVICE_ACCOUNT_CLIENT_ID'),
	"auth_uri": 'https://accounts.google.com/o/oauth2/auth',
	"token_uri": 'https://oauth2.googleapis.com/token',
	"auth_provider_x509_cert_url": 'https://www.googleapis.com/oauth2/v1/certs',
	"client_x509_cert_url": config('FIREBASE_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL'),
}


SERVICE_CONFIG = dict(SIMPLE_CONFIG, serviceAccount=SERVICE_ACCOUNT)


# get this json file from firebase console
# go to project settings, service accounts tab and click generate new private key
SERVICE_ACCOUNT_PATH = "firebase-adminsdk.json"

SERVICE_CONFIG_WITH_FILE_PATH = dict(SIMPLE_CONFIG, serviceAccount=SERVICE_ACCOUNT_PATH)


TEST_USER_EMAIL = config('TEST_USER_EMAIL')
TEST_USER_PASSWORD = config('TEST_USER_PASSWORD')
