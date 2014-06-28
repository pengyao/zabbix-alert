'''
Utils
'''

import yaml
import os
import argparse
from zabbixalert.exceptions import ConfigError, OptionReq

def _get_config(config_file, section):
    '''
    Get Config from yaml file
    '''
    ret = {
        'result': True,
        'comment': [],
        'options': {},
    }
    try:
        config_fd = open(config_file)
        configs = yaml.load(config_fd)
        ret['options'] = configs[section]
    except Exception, e:
        ret['result'] = False
        ret['comment'].append(str(e))
        return ret
    return ret

def _check_options(options, requisit_opts):
    '''
    Check Requisit options
    '''
    ret = {
        'result': True,
        'comment': [],
    }
    for eachopt in requisit_opts:
        if not options.has_key(eachopt):
            ret['result'] = False
            ret['comment'].append('%s option is requisite' %(eachopt))
    return ret

def get_options(config_file, section, requisit_opts):
    '''
    Get options from yaml file
    '''
    config = _get_config(config_file, section)
    if not config['result']:
        raise ConfigError(';'.join(config['comment'])) 
    options = config['options']
    options_check = _check_options(options, requisit_opts)
    if not options_check['result']:
        raise OptionReq(';'.join(options_check['comment'])) 
    return options 

def get_args():
    '''
    Get args
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('to', help='send to someone')
    parser.add_argument('subject', help='subject')
    parser.add_argument('message', help='message')
    args = parser.parse_args()
    to = args.to
    subject = args.subject
    message = args.message
    return (to, subject, message)

def notify(config_file, config_section, requisit_opts, notifier):
    '''
    Notify wrapper
    '''
    to, subject, message = get_args()
    options = get_options(config_file, config_section, requisit_opts)
    ret = notifier(options).notify(to, subject, message)
    return ret
