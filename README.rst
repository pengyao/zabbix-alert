What is this?
##################

ZabbixAlert is `zabbix <http://www.zabbix.com/>`_ alertscripts.

Features
##################

Support send notification to:
* Email
* `Redmine <http://www.redmine.org/>`_ Issue

How to?
############

Email
*************

Send notification by email

* Install requirements

.. code-block:: bash

  pip install -r requirements_pyemail.txt

* Config config.yaml, like:

.. code-block:: yaml

  email:
    smtp_host: mail.example.com
    user: test@example.com
    alias: zabbix-alert
    password: mypassword

* Test

.. code-block:: bash

  ./pyemail.py "test@example.com" "this is subject" "this is message"


Redmine Issue
*****************

Send notification to Redmine issue for track problem.

* Install requirements

.. code-block:: bash

  pip install -r requirements_pyredmine.txt

* Config config.yaml, like:

.. code-block:: yaml

  redmine:
    url: http://redmine.example.com  # redmine url
    user: pengyao                    # redmine user
    key: 1f2u3c4k5g6f7w              # redmine api key for this user
    project: zabbix-alert            # redmine project name

* Test

.. code-block:: bash

  ./pyredmine "1" "this is subject" "this is message"

*1* is redmine user id to assign
