Integrate Firebase
##################

You can integrate Firebase project into your Python app in
two ways.

User based Authentication
*************************

For use with only user based authentication we can create the
following configuration:

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
   firebaseApp = firebase.initialize_app(config)
..


Admin based Authentication
**************************

We can optionally send `service account credential`_ to our app that
will allow our server to authenticate with Firebase as an **admin**
and disregard any security rules.

.. _service account credential: https://firebase.google.com/docs/server/setup#prerequisites


Service Account Secret File
===========================

The following example uses the service account secrets `file` path
as the value for `serviceAccount` key.

.. code-block:: python

   # Import Firebase REST API library
   import firebase

   # Firebase configuration with service account secret file path
   config = {
      "apiKey": "apiKey",
      "authDomain": "projectId.firebaseapp.com",
      "databaseURL": "https://databaseName.firebaseio.com",
      "projectId": "projectId",
      "storageBucket": "projectId.appspot.com",
      "messagingSenderId": "messagingSenderId",
      "appId": "appId"

      "serviceAccount": "path/to/serviceAccountCredentials.json"
   }

   firebaseApp = firebase.initialize_app(config)
..


Service Account Secret Dict
===========================


The following example uses the service account secrets `dict`
as the value for `serviceAccount` key.

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

   # Service Account Secret dict
   service_account_key = {
      "type": "service_account",
      "project_id": "project_id",
      "private_key_id": "private_key_id",
      "private_key": "private_key",
      "client_email": "client_email",
      "client_id": "client_id",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "client_x509_cert_url"
   }

   config['serviceAccount'] = service_account_key

   firebaseApp = firebase.initialize_app(config)
..

.. note::
   Adding a service account will authenticate as an admin
   by default for all database queries, check out the
   :ref:`Authentication documentation<guide/authentication:Authentication>`
   for how to authenticate users.

Use Services
************

A Firebase app can use multiple Firebase services.

``firebaseApp.auth()`` - :ref:`Authentication<guide/authentication:Authentication>`

``firebaseApp.database()`` - :ref:`Database<guide/database:Database>`

``firebaseApp.storage()`` - :ref:`Storage<guide/storage:Storage>`

Check out the documentation for each service for further details.
