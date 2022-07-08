Setup Project
=============

Before you can add Firebase to your Python app, you need to
create a Firebase project and register your app with that
project. When you register your app with Firebase, you'll
get a Firebase configuration object that you'll use to
connect your app with your Firebase project resources.


Create a Firebase project
-------------------------

1. In the `Firebase console`_, click **Add project**.

   * To add Firebase resources to an existing Google Cloud project,
     enter its project name or select it from the dropdown menu.

   * To create a new project, enter the desired project name. You
     can also optionally edit the project ID displayed below the
     project name.

     .. attention::

        Firebase generates a unique ID for your Firebase project based
        upon the name you give it. If you want to edit this project
        ID, you must do it now as it cannot be altered after Firebase
        provisions resources for your project. Visit
        `Understand Firebase`_ Projects to learn about how Firebase
        uses the project ID.

2. If prompted, review and accept the Firebase terms.

3. Click **Continue**.

4. (Optional) Set up Google Analytics for your project.

   .. note::

      You can always set up Google Analytics later in the
      |integrations|_ tab of your :fa:`gear; 2em` Project settings.

5. Click **Create project** (or **Add Firebase**, if you're using
   an existing Google Cloud project).

Firebase automatically provisions resources for your Firebase project.
When the process completes, you'll be taken to the overview page for
your Firebase project in the Firebase console.

.. _Firebase Console: https://console.firebase.google.com
.. |integrations| replace:: *integrations*
.. _integrations: https://console.firebase.google.com/u/0/project/_/settings/integrations
.. _Understand Firebase: https://firebase.google.com/docs/projects/learn-more#project-id


Setup Realtime Database
^^^^^^^^^^^^^^^^^^^^^^^

``databaseURL`` key is not present by default in the Firebase
configuration when an app is :ref:`registered<guide/setup:Register your app>`.
It is recommended to setup database before
:ref:`registering an app<guide/setup:Register your app>`.



Register your app
-----------------

After you have a Firebase project, you can register your web app with
that project.

1. In the center of the `Firebase console's project overview page`_,
   click the **Web** icon (:fa:`code; fa-solid; 2em`) to launch the
   setup workflow.

    | If you've already added an app to your Firebase project,
      click **Add app** to display the platform options.

2. | Enter your app's nickname.
   | This nickname is an internal, convenience identifier
     and is only visible to you in the Firebase console.

3. Click **Register app**.

4. | Copy the Firebase configuration dict shown in the screen, and
     store it use to connect to your project later in code example
     part.
   | The dict should be of the architecture shown below:

  .. code-block:: python

     config = {
        "apiKey": "apiKey",
        "authDomain": "projectId.firebaseapp.com",
        "databaseURL": "https://databaseName.firebaseio.com",
        "projectId": "projectId",
        "storageBucket": "projectId.appspot.com",
        "messagingSenderId": "messagingSenderId",
        "appId": "appId"
     }
  ..

5. Click **Continue to console**.

.. _Firebase console's project overview page: https://console.firebase.google.com
