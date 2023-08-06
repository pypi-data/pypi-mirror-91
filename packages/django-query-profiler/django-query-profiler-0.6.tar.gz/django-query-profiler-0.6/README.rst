======================
Django Query Profiler
======================

.. image:: https://img.shields.io/pypi/l/django.svg
   :target: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/LICENSE

.. image:: https://travis-ci.com/django-query-profiler/django-query-profiler.svg?branch=master
    :target: https://travis-ci.com/django-query-profiler/django-query-profiler

.. image:: https://codecov.io/gh/django-query-profiler/django-query-profiler/branch/master/graph/badge.svg?token=1Cv7WsOi2W
  :target: https://codecov.io/gh/django-query-profiler/django-query-profiler

.. image:: https://readthedocs.org/projects/django-query-profiler/badge/?version=latest
  :target: https://django-query-profiler.readthedocs.io/en/latest/index.html

.. image:: https://img.shields.io/pypi/pyversions/django-query-profiler.svg
  :target: https://pypi.org/project/django-query-profiler/

.. image:: https://img.shields.io/pypi/djversions/django-query-profiler
  :target: https://pypi.org/project/django-query-profiler/

.. image:: https://badge.fury.io/py/django-query-profiler.svg
    :target: https://pypi.org/project/django-query-profiler/



This is a query profiler for Django applications, for helping developers answer the question "My Django code/page/API is slow, How do I find out why?"

Below are some of the features of the profiler:

1. Shows code paths making N+1 sql calls:  Shows the sql with stack_trace which is making N+1 calls, along with sql count
2. Shows the proposed solution: If the solution to reduce sql is to simply apply a select_related or a prefetch_related, this is highlighted as a suggestion
3. Shows exact sql duplicates: Count of the queries where (sql, parameters) is exactly the same.  This is the kind of sql where implementing a query cache would help
4. Flame Graph visualisation: Collects all the stack traces together to allow quickly identifying which area(s) of code is causing the load to the database
5. Command line or chrome plugin: The profiler can be called from command line via context manager, or can be invoked via a middleware, and output shown in a chrome plugin
6. Super easy to configure in any application:  The only changes are in settings.py file and in urls.py file

This is the `repo <https://github.com/django-query-profiler/django-query-profiler-chrome-plugin>`_ for the chrome plugin

Requirements
============

This works with any version of django >= 2.0, and running on python >= 3.6


Profiler in Action
==================

as a chrome plugin
------------------

This image shows how the chrome plugin would display profiled data, once it is configured & installed

.. image:: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/docs/_static/django_query_profiler_in_action.gif

on command line
---------------

See this `file
<https://github.com/django-query-profiler/django-tip-02/blob/18785d9e44b5f542ce26f555a4bcf18124f788d0/DJANGO_QUERY_PROFILER.md>`_ in the PR to see how to use the context manager, and how easy it is to find performance issues :-)

The output of Django query profiler is same for the command line or the chrome plugin.   In fact, chrome plugin displays the output set by the middleware - which is just a plain wrapper around context manager.

Getting Started
===============

installation
------------

The simplest way to getting started is to install the django query profiler from pip, and get the chrome plugin from
chrome web store.

**Python package:**

.. code-block:: console

  pip install django-query-profiler

**Chrome Plugin:**

Download from `chrome webstore <https://chrome.google.com/webstore/detail/django-query-profiler/ejdgfhecpkhdnpdmdheacfmknaegicff>`__


This is covered in detail in the `installation <https://django-query-profiler.readthedocs.io/en/latest/installation.html>`__ section in the docs

configuration:
--------------

This configuration is when we want to use the profiler along with the chrome plugin.  If we want to just use it on the
command line, the configuration is much more simpler (two lines of change to settings.py file) - that is covered in the `docs <https://django-query-profiler.readthedocs.io/en/latest/configuration_instructions.html#as-context-manager>`__

**settings.py:**

.. code-block:: python

    from django_query_profiler.settings import *

    INSTALLED_APPS = (
        ...
        'django_query_profiler',
        ...
    )

    MIDDLEWARE = (
        ...
         # Request and all middleware that come after our middleware, would be profiled
        'django_query_profiler.client.middleware.QueryProfilerMiddleware',
        ...
    )

    DATABASES = (
        ...
        # Adding django_query_profiler as a prefix to your ENGINE setting
        # Assuming old ENGINE was "django.db.backends.sqlite3", this would be the new one
        "ENGINE": "django_query_profiler.django.db.backends.sqlite3",
    )


**urls.py:**

.. code-block:: python

  # Add this line to existing urls.py
  path('django_query_profiler/', include('django_query_profiler.client.urls'))


See this `PR
<https://github.com/django-query-profiler/django-query-profiler-sample-app/pull/1>`__ on how to configure this in your application,
and how the plugin is going to look like after your configuration

.. image:: https://raw.githubusercontent.com/django-query-profiler/django-query-profiler/master/docs/_static/chrome_plugin.png


This is covered in detail in the `configuration instructions <https://django-query-profiler.readthedocs.io/en/latest/configuration_instructions.html>`__ section in the docs

How the profiler works
======================

This is also covered in detail in the documentation at `how the profiler works <https://django-query-profiler.readthedocs.io/en/latest/how_it_works.html>`__ section in the docs,
along with how the code is organized.

The docs also contain references to various links which helped us to lear about internals of Django, and to various projects which helped us to learn on how to add hooks when Django executes a query


Choosing Profiler levels
========================

We have two levels of profiler, and each of them have a different overhead.  The two levels are:

1. QUERY_SIGNATURE:   This is the mode where we capture the query as well as the stack-trace.  This mode figures out the N+1 code paths and also tells us the proposed solution
2. QUERY: This is the mode where we just capture queries, and not the stack-trace

On an average, QUERY_SIGNATURE level adds an overhead of `1 millisecond per 7 queries`, and QUERY_SIGNATURE adds an overhead of `1 millisecond per 25 queries`.

It is simple to change the profiler level for all the requests, or can be configured per request.  This is covered in the `choosing profiler level <https://django-query-profiler.readthedocs.io/en/latest/choosing_profiler_level.html>`__ section of the docs

Customizing the profiler
========================

We have tried to make the profiler customizable by providing hooks at various points.   Some of the use cases are covered
here in the `customizing the defaults <https://django-query-profiler.readthedocs.io/en/latest/customizing_defaults.html>`__ section in docs.

We plan to add more hooks for customizing the profiler as we gather more feedback from real world use cases.


For contributors
================

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: http://makeapullrequest.com

The django query profiler is released under the BSD license, like Django itself.

If you like it, please consider contributing!  The docs cover everything from how to setup locally, to how the code is organized to running tests.


Documentation
=============

Full documentation is available at `readthedocs <https://django-query-profiler.readthedocs.io/en/latest/index.html>`__
