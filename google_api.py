from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.text import MIMEText
import base64
import datetime
from tzlocal import get_localzone
import pytz

def getCredentials(accessToken, userAgent):
    try:
        credentials = client.AccessTokenCredentials(accessToken, userAgent);
        return credentials;
    except client.AccessTokenCredentialsError as err:
        # print(err);
        return;

def createMessage(to, _from, subject, message):
    email = MIMEText(message);
    email['to'] = to;
    email['from'] = _from;
    email['subject'] = subject;
    return {'raw': base64.urlsafe_b64encode(email.as_string())};

def sendEmail(accessToken, to, _from, subject, message):
    try:
        credentials = getCredentials(accessToken, 'PseudoBotEmail');
        http = credentials.authorize(httplib2.Http());
        service = discovery.build('gmail', 'v1', http=http);
        email = createMessage(to, _from, subject, message);
        sent = service.users().messages().send(userId='me', body=email).execute();
        return message; #check message id
    except client.AccessTokenCredentialsError as err:
        print(err);
        return;
    except IndexError as err:
        print(err);
        return;



def setReminder(accessToken, evenTime, emailId, minutes=10):
    credentials = getCredentials(accessToken, 'PseudoBotReminder');
    http = credentials.authorize(httplib2.Http());
    service = discovery.build('calendar', 'v3', http=http);
    #convert event time to UTC, its in the format => "%Y-%m-%dT%H:%M:%S"
    timezone = pytz.timezone(str(get_localzone()));
    evenTimeObj = datetime.datetime.strptime(evenTime, "%Y-%m-%dT%H:%M:%S");
    localev = timezone.localize(evenTimeObj);
    timeStr = localev.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z";
    print(timeStr);
    event = {
        'summary': "Reminder",
        'location': "N/A",
        'description': "N/A",
        'start': {
            'dateTime': timeStr
        },
        'end': {
            'dateTime': timeStr
        },
        'attendees': [
                {'email': emailId},
            ],
        'reminders':{
            'useDefault': False,
            'overrides':[
                {'method':'email', 'minutes':5}
            ],
        },
    }
    service.events().insert(calendarId="primary", body=event, sendNotifications=True).execute();
    return;

# if __name__ == '__main__':
#     accessToken = 'ya29.GlxFBBXtNcF1i86Et1525vaJxX2e7CT310zewFtnTw1KfVThHNkceAGJKv2qdN82KIUk3EietDc0-Pc51GSTGRyi9Rha5WTPLdWEM9AMIgHI1gmXSQOAq6PP_RQ82w';
#     # info = client.AccessTokenInfo(accessToken, 3600);
#     # print(info.access_token);
#     # sendEmail(accessToken, '18100203@lums.edu.pk', 'ali.9raz@gmail.com', "LOLOLOL", "HAHAHAHAH");
#     setReminder(accessToken, "2017-05-10T04:31:00", "ali.9raz@gmail.com", 5);