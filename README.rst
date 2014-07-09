What is this?
##################

ZabbixAlert is `zabbix <http://www.zabbix.com/>`_ alertscripts.

Features
##################

Support send notification to:

* Email
* `Redmine <http://www.redmine.org/>`_ Issue
* `Twilio <https://www.twilio.com/>`_ Voice Call

How to?
############

Email
*************

Send notification by email

* Install requirements

.. code-block:: bash

  pip install -r requirements_pyemail.txt

* Config *config.yaml*, like:

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

* Config *config.yaml*, like:

.. code-block:: yaml

  redmine:
    url: http://redmine.example.com  # redmine url
    user: pengyao                    # redmine user
    key: 1f2u3c4k5g6f7w              # redmine api key for this user
    project: zabbix-alert            # redmine project name

* Test

.. code-block:: bash

  ./pyredmine.py "1" "this is subject" "this is message"

*1* is redmine user id to assign

Twilio Call
******************

Send notification to Twilio Voice Call

* Install requirements

.. code-block:: bash

  pip install -r requirements_twilio_call.txt

* Config *config.yaml*, like:

.. code-block:: yaml

  twilio_call:
    from: '+1234567'
    sid: 'Your twilio sid'
    token: 'Your twilio token'
    voice: alice
    language: zh-CN

* Test

.. code-block:: bash

  ./twilio_call.py "8613123456789" "这是一个测试" ""
