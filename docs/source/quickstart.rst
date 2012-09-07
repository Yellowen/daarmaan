Daarmaan Quick Start
====================
At first you should know about `SSO <http://en.wikipedia.org/wiki/Single_sign-on>`_ systems. By using an SSO service you will have a central authentication and authorization service that users
from every other services like a Blog application or a Wiki application easily can authenticate against each other.

.. note:: **Daarmaan** is a SSO server that works on top of Django web framework, It supports only webapplication at this time (version 0.2.1). Also there is only a **Django client** for
          **Daarmaan**, of course we have plans to add others clients but until that you can write your own by looking at developers guide.

**Daarmaan** is based on a Server/Client architecture so at the first step a running **Daarmaan** server is needed.

**Daarmaan** Server
-------------------
**Daarmaan** is just a well baked python package that need to be implement into a **Django** project to become a complete SSO server. Enought talking, let's start to work.
Daarmaan provides a Django application for server code, add it to your installed applications::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'daarmaan.server',
    )

Now include the main ``urls`` module of **Daarmaan** server application, here is an example::

    urlpatterns = patterns('',

        url(r"^", include("daarmaan.server.urls")),
        url(r'^admin/', include(admin.site.urls)),
    )

Just like any other Django application its time to synchronize your database with your models::

    $ python manage.py syncdb

And that is all. You have a **Daarmaan** server now.

**Daarmaan** client
-------------------
Client code also needs to install (That's obvious you idiot). But before jumping to installation you have to install the **Vakhshour** application. Client application requires
**Vakhshour** to send events. Here is the instruction for installing client application.

First add the client application to your INSTALLED_APPS::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
        'daarmaan.client',
    )

There is a middleware that will allow Django to authenticate its user against **Daarmaan**, add the middleware to your application middlewares list::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'daarmaan.client.middlewares.DaarmaanAuthMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

.. note:: Make sure to add the ``daarmaan.client.middlewares.DaarmaanAuthMiddleware`` in the exact place as the example above.

Now replace the Django authentication backend with **Daarmaan**'s one::

    AUTHENTICATION_BACKENDS = (
        'daarmaan.client.backends.DaarmaanBackend',
    )

Put the event handler discovery and client urls into your main ``urls.py`` module::

    from vakhshour.events.discovery import handler_discovery

    handler_discovery()

    urlpatterns = patterns('',
        (r'^pages/', include("page.urls")),
	(r'^auth/', include("daarmaan.client.urls", namespace="daarmaan",
                            app_name="client")),
        (r'^$', 'exampleproj.views.index'),
    )


In the above code you can see the we added the **Vakhsour** event handler discovery to allow client application to register its event handlers. Also we take a look at client urls inclusion.
There some variables that you should add to your ``settings.py`` before using client application::

      # Configuring SSO through Daarmaan service
      DAARMAAN_SERVER = "http://daarmaan.server"
      DAARMAAN_LOGIN = "%s/authenticate/" % DAARMAAN_SERVER

      SERVICE_NAME = "mydomain.com"
      SERVICE_KEY = "a simple string representing service key"

      LOGIN_URL = DAARMAAN_SERVER
      LOGOUT_URL = "/auth/logout/"

      SESSION_EXPIRE_AT_BROWSER_CLOSE = True

The last step for using client application is synchronizing database::

    $ python manage.py syncdb

Noe your planted the **Daarmaan** client application in your project and can use SSO service.

.. note:: You have to be aware of your ``LOGIN`` and ``LOGOUT`` urls, your should simply use the value of ``LOGIN_URL`` and ``LOUGOUT_URL`` settings variables in your template for example.


