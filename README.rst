================
Django Loose CMS
================

Django Loose CMS is a simple cms based on django framework.

Detailed documentation is in the "docs" directory.

Features
--------

* Build bootstrap grid
* Edit stylesheet of the plugis
* Template pages

Requirements
------------

Loose CMS requires:

* Django version 1.8
* Python 2.6 or 2.7
* tinycss
* django-constance
* bootstrap-admin

Quick Start
-----------

1. Instalation via pip::

    pip install https://github.com/lefterisnik/django-loose-cms/archive/master.zip

2. Create your django project::

    django-admin createproject myproject
    cd myproject
    python manage.py createsuperuser

3. Add "loosecms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'loosecms',
    )

4. Add "bootstrap_admin" to your INSTALLED_APPS setting like this before 'django.contrib.admin'::

    INSTALLED_APPS = (
        'bootstrap_admin',
        'django.contrib.admin',
    )

5. Add "constance" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'constance',
        'constance.backends.database',
    )

6. Include the loosecms URLconf in your project urls.py like this::

    url(r'^', include('loosecms.urls')),

 Loose CMS handles all urls.

7. Run `python manage.py migrate` to create the polls models.

8. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

9. Visit http://127.0.0.1:8000/ to participate in the poll.