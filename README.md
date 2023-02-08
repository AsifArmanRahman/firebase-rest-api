<div align="center">

   <h1> Firebase REST API </h1>

   <p>A simple python wrapper for <a href="https://firebase.google.com">Google's Firebase REST API's</a>.</p>
   <br>

</div>

<div align="center">
   <a href="https://pepy.tech/project/firebase-rest-api"> 
      <img alt="Total Downloads" src="https://static.pepy.tech/personalized-badge/firebase-rest-api?period=total&units=international_system&left_color=blue&right_color=grey&left_text=Downloads">
   </a>
</div>

<div align="center">

   <a href="https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/build.yml"> 
      <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/AsifArmanRahman/firebase-rest-api/build.yml?logo=GitHub">
   </a>
   <a href="https://github.com/AsifArmanRahman/firebase-rest-api/actions/workflows/tests.yml">
      <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/asifarmanrahman/firebase-rest-api/tests.yml?label=tests&logo=Pytest">
   </a>
   <a href="https://firebase-rest-api.readthedocs.io/en/latest/">
      <img alt="Read the Docs" src="https://img.shields.io/readthedocs/firebase-rest-api?logo=Read%20the%20Docs&logoColor=white">
   </a>
   <a href="https://codecov.io/gh/AsifArmanRahman/firebase-rest-api"> 
      <img alt="CodeCov" src="https://codecov.io/gh/AsifArmanRahman/firebase-rest-api/branch/main/graph/badge.svg?token=N7TE1WVZ7W"> 
   </a>

</div>

<div align="center">
   <a href="https://pypi.org/project/firebase-rest-api/"> 
      <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/firebase-rest-api?logo=python">
   </a>
   <a href="https://pypi.org/project/firebase-rest-api/"> 
      <img alt="PyPI" src="https://img.shields.io/pypi/v/firebase-rest-api?logo=PyPI&logoColor=white">
   </a>
</div>



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
storage.child(user.get('localId')).child('uploaded-picture.png').put(file_path, user.get('idToken'))
```
