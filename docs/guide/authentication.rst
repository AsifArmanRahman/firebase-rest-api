Authentication
==============

The authentication service allows you to signup, login,
edit profile, apply security to the data you might store
in either :ref:`Database<guide/database:Database>` or
:ref:`Storage<guide/storage:Storage>`, and of course delete
your account.

.. code-block:: python

   # Get a reference to the auth service
   auth = firebaseApp.auth()
..

   .. note::
      All sign in methods return user data, including a token
      you can use to adhere the security rules.


create_user_with_email_and_password
-----------------------------------

Users can create an account using their
email address and choice of password.

.. code-block:: python

   # Creating an account
   auth.create_user_with_email_and_password(email, password)
..

   .. note::
      Make sure you have the Email/Password provider enabled in your
      Firebase dashboard under Authentication -> Sign In Method.


sign_in_with_email_and_password
-------------------------------

User can login using their email and password, provided they
:ref:`created an account<guide/authentication:create_user_with_email_and_password>`
first.

.. code-block:: python

   # Log the user in
   user = auth.sign_in_with_email_and_password(email, password)
..


create_custom_token
-------------------

| You can also create users using `custom tokens`_,
| For example:

.. code-block:: python

   # Create custom token
   token = auth.create_custom_token("your_custom_id")
..

You can also pass in additional claims.

.. code-block:: python

   # Create custom token with claims
   token_with_additional_claims = auth.create_custom_token("your_custom_id", {"premium_account": True})
..

   .. note::
      You need admin credentials (Service Account Key) to create 
      custom tokens.

.. _custom tokens:
   https://firebase.google.com/docs/auth/server/create-custom-tokens


sign_in_with_custom_token
-------------------------

You can send these custom tokens to the client to
sign in, or sign in as the user on the server.

.. code-block:: python

   # log in user using custom token
   user = auth.sign_in_with_custom_token(token)
..


set_custom_user_claims
----------------------

You can add custom claims to existing user, or remove
claims which was previously added to that account.

.. code-block:: python

   # add claims
   auth.set_custom_user_claims(user['localId'], {'premium': True})

   # remove claims
   auth.set_custom_user_claims(user['localId'], {'premium': None})
..

   .. note::
      1. You need admin credentials (Service Account Key) to add or 
      remove custom claims.

      2. The new custom claims will propagate to the user's ID token 
      the next time a new token is issued.


verify_id_token
---------------

You can decode the Firebase ID token, and check for claims.

.. code-block:: python

   # check if user is subscribed to premium
   claims = auth.verify_id_token(user['IdToken'])

   if claims['premium'] is True:
    # Allow access to requested premium resource.
    pass
..


sign_in_anonymous
-----------------

Allows users (who haven't signed up yet) to
use your app without creating an account.


.. code-block:: python

   # Log the user in anonymously
   user = auth.sign_in_anonymous()
..

   .. note:: 
      Make sure you have the **Anonymous** provider enabled in your
      Firebase dashboard under Authentication -> Sign In Method.


create_authentication_uri
-------------------------

Signing in with social providers is done through two steps. First step
one is done via redirecting user to the providers' login page using
:ref:`create_authentication_uri<guide/authentication:create_authentication_uri>`
which is can be used dynamically for all providers.


   .. warning::
      At the moment only sign is via **Google** is supported, other
      ones might break or work.

The method returns an link to redirect user to providers' sign in page.
Once the user signs into their account, user is asked for permissions
and when granted, are redirect to the uri set while creating
**OAuth Client IDs**, with authorization code to which can be further
used to generate tokens to sign in with social providers in
:ref:`second step<guide/authentication:sign_in_with_oauth_credential>`.

.. code-block:: python

   # Get a reference to the auth service with provider secret file
   auth = firebaseApp.auth(client_secret='client-secret-file.json')

   # Reference to auth service with provider secret from env variable
   client_secret_config = { 
      "client_id": environ.get("CLIENT_ID"), 
      "client_secret": environ.get("CLIENT_SECRET"),
      "redirect_uris": [environ.get("REDIRECT_URI")]
   }

   auth = firebaseApp.auth(client_secret=client_secret_config)
..

.. code-block:: python

   # Example usage with Flask
   @auth.route('/login/google')
   def login_google():
      return redirect(auth.create_authentication_uri('google.com'))

..

   .. note:: 
      Make sure you have the **social** provider enabled in your
      Firebase dashboard under Authentication -> Sign In Method.


authenticate_login_with_google
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method is actually an reference to
:ref:`create_authentication_uri<guide/authentication:create_authentication_uri>`
with **Google** preset as the provider to use.


.. code-block:: python

   # Example usage with Flask
   @auth.route('/login/google')
   def login_google():
      return redirect(auth.authenticate_login_with_google())
..

   .. note:: 
      Make sure you have the **Google Sign In** provider enabled in
      your Firebase dashboard under Authentication -> Sign In Method.


authenticate_login_with_facebook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method is actually an reference to
:ref:`create_authentication_uri<guide/authentication:create_authentication_uri>`
with **Facebook** preset as the provider to use.


.. code-block:: python

   # Example usage with Flask
   @auth.route('/login/facebook')
   def login_facebook():
      return redirect(auth.authenticate_login_with_facebook())
..

   .. note:: 
      Make sure you have the **Google Sign In** provider enabled in
      your Firebase dashboard under Authentication -> Sign In Method.



sign_in_with_oauth_credential
-----------------------------

Second step to sign in using social provider is to pass the URL
(containing multiple params) that the user is redirected to, into this
method. This method auto generates the tokens using params from that
URL, then signs the user in using those tokens to Firebase linking the
specific provider.


.. code-block:: python

   # Here https://example.com/oauth2callback/ is the redirect URI
   # that was set while creating OAuth Client ID

   # Example usage with Flask
   @auth.route('/oauth2callback/')
   def oauth2callback():

      user = auth.sign_in_with_oauth_credential(request.url)

	   return jsonify(**user)


get_account_info
----------------

This method returns an detailed version of the user's data associated
with Authentication service.

.. code-block:: python

   # User account info
   user_info = auth.get_account_info(user['idToken'])
..


update_profile
--------------

Update stored information or add information into the user's account.

.. code-block:: python

   # Update user's name
   auth.update_profile(user['idToken'], display_name='Iron Man')

   # update user's profile picture
   auth.update_profile(user['idToken'], photo_url='https://i.pinimg.com/originals/c0/37/2f/c0372feb0069e6289eb938b219e0b0a1.jpg')
..


change_email
--------------

Change the email associated with the user's account.

.. code-block:: python

   # change user's email
   auth.change_email(user['idToken'], email='iam@ironman.com')

..


change_password
--------------

Change the password associated with the user's account.

.. code-block:: python

   # change user's password
   auth.change_password(user['idToken'], password='iLoveYou3000')

..


refresh
-------

Firebase Auth Tokens are granted when an user logs in, and are
associated with an expiration time of an hour generally, after
that they lose validation and a new set of Tokens are needed,
and they can be obtained by passing the ``refreshToken`` key
from the users' tokens, received when logged in.

.. code-block:: python

   # before the 1 hour expiry:
   user = auth.refresh(user['refreshToken'])

   # now we have a fresh token
   user['idToken']
..


delete_user_account
-------------------

In case any user want to delete their account, it can be done by
passing ``idToken`` key from the users' tokens, received when logged
in.

.. code-block:: python

   auth.delete_user_account(user['idToken'])
..


send_password_reset_email
-------------------------

In case any user forgot his password, it is possible to send
them email containing an code or link to reset their password.

.. code-block:: python

   auth.send_password_reset_email(email)
..


send_email_verification
-----------------------

To ensure the email address belongs to the user who created the
account, it is recommended to request verification of the email.
Verification code/link can be sent to the user by passing ``idToken``
key from the users' tokens, to this method.

.. code-block:: python

   auth.send_email_verification(user['idToken'])
..
