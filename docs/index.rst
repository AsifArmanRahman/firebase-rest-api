.. firebase-rest-api documentation master file, created by
   sphinx-quickstart on Thu Jul  7 11:47:19 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Firebase REST API |release|
###########################

A simple python wrapper for Google's
`Firebase <https://firebase.google.com>`__ REST API's.


Installation
************

.. code-block:: python

   pip install firebase-rest-api
..



Quick Start
***********

In order to use this library, you first need to go through the
following steps:

1. Select or create a  Firebase project from `Firebase Console`_.
   :ref:`(guide)<guide/setup:Create a Firebase project>`

2. Register an Web App.
   :ref:`(guide)<guide/setup:Register your app>`

.. _Firebase Console: https://console.firebase.google.com



Example Usage
=============

.. code-block:: python

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

..



Documentation contents
######################

.. toctree::
   :maxdepth: 1

   guide/setup
   guide/firebase-rest-api

.. toctree::
   :maxdepth: 2

   firebase/modules



Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
