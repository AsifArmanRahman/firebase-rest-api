# Firebase REST API

[![build](https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/build.yml/badge.svg)](https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/build.yml)
[![tests](https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/tests.yml/badge.svg)](https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/firebase-rest-api/badge/?version=latest)](https://firebase-rest-api.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/AsifArmanRahman/firebase-rest-api/branch/main/graph/badge.svg?token=N7TE1WVZ7W)](https://codecov.io/gh/AsifArmanRahman/firebase-rest-api)


A simple python wrapper for [Google's Firebase REST API's](https://firebase.google.com).

## Installation

```python
pip install firebase-rest-api
```


## Quick Start

In order to use this library, you first need to go through the following steps:

1. Select or create a Firebase project from [Firebase](https://console.firebase.google.com) Console.

2. Register an Web App.


### Example Usage

```python
# Import Firebase REST API library
import firebase

# Firebase configuration
config = {
   "apiKey": "apiKey",
   "authDomain": "projectId.firebaseapp.com",
   "databaseURL": "https://databaseName.firebaseio.com",
   "projectId": "projectId",
   "storageBucket": "projectId.appspot.com",
   "messagingSenderId": "messagingSenderId",
   "appId": "appId"
}

# Instantiates a Firebase app
app = firebase.initialize_app(config)


# Firebase Authentication
auth = app.auth()

# Create new user and sign in
auth.create_user_with_email_and_password(email, password)
user = auth.sign_in_with_email_and_password(email, password)


# Firebase Realtime Database
db = app.database()

# Data to save in database
data = {
   "name": "Robert Downey Jr.",
   "email": user.get('email')
}

# Store data to Firebase Database
db.child("users").push(data, user.get('idToken'))


# Firebase Storage
storage = app.storage()

# File to store in storage
file_path = 'static/img/example.png'

# Store file to Firebase Storage
storage.child(user.get('email')).child('uploaded-picture.png').put(file_path, user.get('idToken'))
```
