import smtplib
from email import  MIMEText
from email.Header import Header
from socket import timeout
from zabbixalert.notifier import BaseNotifier

class EmailNotifier(BaseNotifier):
    '''
    Email Notifier
    '''
    def notify(self, to, subject, message):
        '''
        Email notify
        '''
        ret = {
            "result": True,
            "comment": [],  
        }
        smtp_host = self.options['smtp_host']
        smtp_tls = self.options.get('smtp_tls', False)
        if smtp_tls:
            smtp_port = int(self.options.get('smtp_port', 465))
            smtp_class = smtplib.SMTPSSL
        else:
            smtp_port = int(self.options.get('smtp_port', 25))
            smtp_class = smtplib.SMTP
        try:
            server = smtp_class(smtp_host, smtp_port)
        except timeout:
            ret['result'] = False
            ret['comment'].append('%s connect timeout' %(smtp_host))
            return ret
        user = self.options['user']
        password = self.options.get('password')
        if password:
            try:
                server.login(user, password)
            except Exception, e:
                ret['result'] = False
                ret['comment'].append(str(e))
                return ret

        message = MIMEText.MIMEText(message, 'plain', 'utf-8')
        message['From'] = '%s<%s>' %(self.options.get('alias', 'zabbix-alert'), user)
        message['To'] = to
        message['Subject'] = Header(subject, 'utf-8')
        try:
            server.sendmail(user, to, message.as_string())
        except Exception, e:
            ret['result'] = False
            ret['comment'].append(str(e))
            return ret
        ret['comment'].append('send mail success!')
        return ret
