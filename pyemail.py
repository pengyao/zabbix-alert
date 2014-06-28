#!/usr/bin/env python
#coding=utf8

import sys
import os

from zabbixalert.utils import get_options, get_args
from zabbixalert.exceptions import NotifyError
from zabbixalert.notifier.pyemail import Email

__config_section__ = 'email'
__requisit_opts__ = ['smtp_host', 'user']

def notify(options, to, subject, message):
    notifier = Email(options)
    ret = notifier.notify(to, subject, message) 
    return ret
    

if __name__ == '__main__':
    to, subject, message = get_args() 
    config_file = 'config.yaml'
    config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + config_file
    options = get_options(config_file, __config_section__, __requisit_opts__)
    ret = notify(options, to, subject, message)
    if not ret['result']:
       raise NotifyError(';'.join(ret['comment']))
    else:
        print ';'.join(ret['comment'])
