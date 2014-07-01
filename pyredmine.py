#!/usr/bin/env python
#coding=utf8

import os
from zabbixalert.notifier.pyredmine import RedmineNotifier
from zabbixalert.exceptions import NotifyError
from zabbixalert.utils import notify

__config_section__ = 'redmine'
__requisit_opts__ = ['url', 'user', 'key', 'project']
notifier = RedmineNotifier

if __name__ == '__main__':
    config_file = 'config.yaml'
    config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + config_file
    ret = notify(config_file, __config_section__, __requisit_opts__, notifier)
    if not ret['result']:
       raise NotifyError(';'.join(ret['comment']))
    else:
        print ';'.join(ret['comment'])
