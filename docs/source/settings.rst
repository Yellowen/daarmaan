Daarmaan Django settings reference
==================================
Here is a complete list of **Daarmaan** related Django settings for clients:

DAARMAAN_SERVER:
    Specify the remote **Daarmaan** server in client application

DAARMAAN_LOGIN:
    Specify the remote authentication url (usually `DAARMAAN_SERVER/authenticate/`)

SERVICE_NAME:
    Specify the current service name to use as the service name with **Daarmaan**

SERVICE_KEY:
    Secret key of current server to communicate with Daarmaan server

DAARMAAN_EXCLUDE_URLS:
    A **list** of url patterns to exclude from authentication using Daarmaan.

.. warning:: You should starts each exclude url using `^/` character (starting slash is required)
