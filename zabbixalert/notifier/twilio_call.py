__author__ = 'pengyao'

from urllib import urlencode
from zabbixalert.notifier import BaseNotifier
from twilio.rest import TwilioRestClient
from twilio import twiml

class TwilioCallNotifier(BaseNotifier):
    '''
    Twilio Call Notifier
    '''
    def _mk_twiml(self, message):
        '''
        Make Twiml Say XML
        '''
        voice = self.options.get('voice', 'alice')
        language = self.options.get('language', 'en-US')
        loop = self.options.get('loop', 1)
        response = twiml.Response()
        response.addSay(message, voice=voice, language=language, loop=loop)
        return response.toxml()

    def notify(self, to, subject, message):
        '''
        Twilio Call notify
        '''
        ret = {
            "result": True,
            "comment": [],  
        }
        token = self.options['token']
        sid = self.options['sid']
        from_ = self.options['from']
        if not to.startswith('+'):
            to = '+' + to
        client = TwilioRestClient(sid, token)
        twiml_xml = self._mk_twiml(subject.decode('utf-8'))
        twiml_echo = urlencode({'Twiml': twiml_xml})
        twiml_url = 'http://twimlets.com/echo?' + twiml_echo
        method = self.options.get('method', 'POST')
        
        try:
            client.calls.create(
                url=twiml_url,
                method=method,
                from_=from_,
                to=to)
        except Exception, e:
            ret['result'] = False
            ret['comment'].append(str(e))
            return ret
        ret['comment'].append('send call success!')
        return ret
