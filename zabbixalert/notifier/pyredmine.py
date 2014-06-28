# -*- coding: utf-8 -*-
__author__ = 'pengyao'

import sys
import os
from redmine import Redmine
from zabbixalert.notifier import BaseNotifier

class RedmineNotifier(BaseNotifier):
    '''
    Redmine Notifier
    '''
    def __init__(self, options):
        super(RedmineNotifier, self).__init__(options)
        self.tracker_id = self.options.get('tracker_id', 1)
        self.event_prioritys = {'Not classified': 1, 'Information': 1, 'Warning': 2, 'Average': 3, 'High': 4, 'Disaster': 5}
        self.event_status = {'PROBLEM': 1, 'UNKNOWN': 1, 'OK': 3}

    def _get_eventinfo(self, message):
        '''
        Get zabbix event info from message
        '''
        eventinfo = {}
        eventinfo['eventid'] = -1
        eventinfo['status'] = 'UNKNOWN'
        eventinfo['severity'] = 'Not classified'
        eventinfo['message'] = message
        for eachline in message.split('\n'):
            if eachline.find('Trigger status:') != -1 or eachline.find('当前状态:') != -1:
                eventinfo['status'] = eachline.split()[-1]
            if eachline.find('Trigger severity') != -1 or eachline.find('报警级别:') != -1:
                if eachline.find(eventinfo['severity']) == -1:
                    eventinfo['severity'] = eachline.split()[-1]
            elif eachline.find('Original event ID:') != -1 or eachline.find('Event ID:') != -1:
                eventinfo['eventid'] = eachline.split()[-1]
        self.eventinfo = eventinfo

    def _issue(self, to, subject, message):
        '''
        Create/Update Redmine Issue
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        cache_dir = '/tmp/zabbix-events/'
        issue_update = False

        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        self._get_eventinfo(message)
        event_file = cache_dir + os.sep + str(self.eventinfo['eventid'])
        if os.path.isfile(event_file):
            event_fd = open(event_file, 'r')
            for eachline in event_fd:
                if eachline.startswith('issueid:'):
                    issueid = int(eachline.split()[-1])
                    issue_update = True
                    break
            event_fd.close()

        # Process Issue
        redmine = Redmine(self.options['url'], key=self.options['key'])
        if not issue_update and self.eventinfo['status'] != 'OK':
            # Create Issue
            issue = redmine.issue.new()
            issue.project_id = self.options['project']
            issue.subject = subject
            issue.description = message
            issue.priority_id = self.event_prioritys.get(self.eventinfo['severity'], 1)
            issue.status_id = self.event_status[self.eventinfo['status']]
            issue.assigned_to_id = int(to)
            issue.tracker_id = self.tracker_id
            try:
                issue.save()
            except Exception, e:
                ret['result'] = False
                ret['comment'].append(str(e))
                return ret
            issueid = issue.id
            event_fd = open(event_file, 'a')
            event_fd.write('issueid: %s\n'%(issueid))
            event_fd.close()
            ret['comment'].append('Issue create success!')
        elif issue_update:
            # Update Issue
            try:
                issue = redmine.issue.update(issueid, notes=message)
                if self.eventinfo['status'] == 'OK':
                    # If status is ok, remove event cache file
                    os.remove(event_file)
            except Exception, e:
                ret['result'] = False
                ret['comment'].append(str(e))
                return ret
            ret['comment'].append('Issue update success!')
        return ret

    def notify(self, to, subject, message):
        '''
        Redmine Notify
        '''
        return self._issue(to, subject, message)
