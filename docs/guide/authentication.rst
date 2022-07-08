Authentication
==============

The ``sign_in_with_email_and_password()`` method returns user
data, including a token you can use to adhere to security rules.


.. code-block:: python

   # Get a reference to the auth service
   auth = firebaseApp.auth()

   # Log the user in
   user = auth.sign_in_with_email_and_password(email, password)

   # Log the user in anonymously
   user = auth.sign_in_anonymous()

   # Add user info
   user = auth.update_profile(display_name, photo_url, delete_attribute)

   # Get user info
   user = auth.get_account_info()

   # Get a reference to the database service
   db = firebaseApp.database()

   # data to save
   data = {
       "name": "Mortimer 'Morty' Smith"
   }

   # Pass the user's idToken to the push method
   results = db.child("users").push(data, user['idToken'])
..



Token expiry
------------


.. code-block:: python

   user = auth.sign_in_with_email_and_password(email, password)
   # before the 1 hour expiry:
   user = auth.refresh(user['refreshToken'])
   # now we have a fresh token
   user['idToken']
..


Custom tokens
-------------

You can also create users using `custom
tokens <https://firebase.google.com/docs/auth/server/create-custom-tokens>`__,
for example:

.. code-block:: python

   token = auth.create_custom_token("your_custom_id")
..

You can also pass in additional claims.

.. code-block:: python

   token_with_additional_claims = auth.create_custom_token("your_custom_id", {"premium_account": True})
..

You can then send these tokens to the client to sign in, or sign in as
the user on the server.

.. code-block:: python

   user = auth.sign_in_with_custom_token(token)
..



Manage Users
------------


Creating users
^^^^^^^^^^^^^^

.. code-block:: python

   auth.create_user_with_email_and_password(email, password)
..

   .. note::
      Make sure you have the Email/password provider enabled in your
      Firebase dashboard under Authentication -> Sign In Method.

Verifying emails
^^^^^^^^^^^^^^^^

.. code-block:: python

   auth.send_email_verification(user['idToken'])
..

Sending password reset emails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   auth.send_password_reset_email("email")
..

Get account information
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   auth.get_account_info(user['idToken'])
..

Refreshing tokens
^^^^^^^^^^^^^^^^^

.. code-block:: python

   user = auth.refresh(user['refreshToken'])
..

Delete account
^^^^^^^^^^^^^^

.. code-block:: python

   auth.delete_user_account(user['idToken'])
..
