Storage
=======

The storage service allows you to upload files (eg. text, image,
video) to Firebase.

child
-----

Just like with the Database service, you can build paths to your data
with the Storage service.

.. code-block:: python

   storage.child("images/example.jpg")
..

put
---

The put method takes the path to the local file and an optional user
token.

.. code-block:: python

   storage = firebaseApp.storage()
   # as admin
   storage.child("images/example.jpg").put("example2.jpg")
   # as user
   storage.child("images/example.jpg").put("example2.jpg", user['idToken'])
..

download
--------

The download method takes the path to the saved database file and the
name you want the downloaded file to have.

.. code-block:: python

   storage.child("images/example.jpg").download("downloaded.jpg")
..

get_url
-------

The get_url method takes the path to the saved database file and user
token which returns the storage url.

.. code-block:: python

   storage.child("images/example.jpg").get_url(user["idToken"])
   # https://firebasestorage.googleapis.com/v0/b/storage-url.appspot.com/o/images%2Fexample.jpg?alt=media
..

delete
------

The delete method takes the path to the saved database file and user
token.

.. code-block:: python

   storage.delete("images/example.jpg",user["idToken"])
..


Helper Methods
--------------

generate_key
^^^^^^^^^^^^

``db.generate_key()`` is an implementation of Firebase's `key generation
algorithm <https://www.firebase.com/blog/2015-02-11-firebase-unique-identifiers.html>`__.

See multi-location updates for a potential use case.


sort
^^^^

Sometimes we might want to sort our data multiple times. For example, we
might want to retrieve all articles written between a certain date then
sort those articles based on the number of likes.

Currently the REST API only allows us to sort our data once, so the
``sort()`` method bridges this gap.

.. code-block:: python

   articles = db.child("articles").order_by_child("date").start_at(startDate).end_at(endDate).get()
   articles_by_likes = db.sort(articles, "likes")
..


Common Errors
-------------

Index not defined
^^^^^^^^^^^^^^^^^

+ `Indexing`_ is **not enabled** for the database reference.

.. _Indexing: https://firebase.google.com/docs/database/security/indexing-data
