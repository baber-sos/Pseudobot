import datetime
import pytz
import utils
import random
from chatterbot.chatterbot import ChatBot
import sys
from tzlocal import get_localzone
import json
from google_api import sendEmail, setReminder
from weather import getWeather
from datab import read

chatbot = ChatBot(
    'PseudoBot',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            "response_selection_method" : "chatterbot.response_selection.get_first_response"

        }],
    filters=['chatterbot.filters.RepetitiveResponseFilter']

)


triggered = {}
numberOfReplies = {}

threshold = 50



def get_response(query,assistant, accessToken='', userEmail='', session_id=''):
    global triggered
    global numberOfReplies
    if assistant == '1':
        #parse the receiver email or query time here

        #assuming we have a variable for deciding the type of query => type
        #1 -> gmail, 2 -> reminder, 3 -> time, 4 ->  weather
        if accessToken == '' or userEmail == '':
            return 'You need to sign in to google account'
        qType = 0;

        parsed = utils.queryClass(query)

        qType = parsed[0]

        if qType == 0:
            return "I can't understand what you said"

        if qType == 1:
            emailTo = parsed[2]
            message = parsed[1]
            #parse subject and message from query, below is the actual commented call for send email
            sendEmail(accessToken, emailTo, userEmail, 'No subject', message);
            return "I have sent your email."
        elif qType == 2:
            message = parsed[1]
            time = parsed[2] + ':00';
            if time[0] != 0 and time[1] == ':':
                time = '0' + time;
            evenTime = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d')+'T'+time, '%Y-%m-%dT%H:%M:%S')
            #parse eventTime from the query, below is the actual call for setReminder
            setReminder(accessToken, evenTime.strftime('%Y-%m-%dT%H:%M:%S'), userEmail);
            return "Okay. I will set the reminder."
        elif qType == 3:
            #time code goes here
            # print str(get_localzone());
            return pytz.timezone(str(get_localzone())).localize(datetime.datetime.now()).strftime('%I:%M:%S%p %Z');
        elif qType == 4:
            #weather code goes here
            for word in query.split():
                word = word.strip();
                with open('city.list.json') as citilist:
                    data = json.load(citilist);
                    city = [c['name'] for c in data if c['name'].lower() == word.lower() and c['name'].lower() != "of"];
                    if len(city) > 0:
                        # print city[0];
                        return getWeather(city[0]);
            # print 'weather found';
            return "City Not Found";

    else:
        query = query.lower()
        if session_id not in triggered:
            triggered[session_id] = False
            numberOfReplies[session_id] = 0

        swearWords = utils.parseSwearWords()
        swearWords = [w.strip() for w in swearWords]
        triggeredResponses = utils.parseTriggeredResponses()
        score = utils.stringScoring(query)

        if score <= threshold:
            return "I don't understand gibberish :)"

        for word in query.split():
            if word in swearWords:
                numberOfReplies[session_id] = 4
                triggered[session_id] = True
                break

        if triggered[session_id]:
            if numberOfReplies[session_id] == 0:
                triggered[session_id] = False
            numberOfReplies[session_id] -= 1
            return random.choice(triggeredResponses)
        livetrainInverted = [];
        livetrain = [];
        f = open("ontheflytraining.txt", 'rw+');
        f2 = open("ontheflytraining2.txt", 'rw+');
        for eachline in f.readlines():
            livetrainInverted.append(eachline.strip());
        for eachline in f2.readlines():
            livetrain.append(eachline.strip())
        if len(livetrain)==10:
            chatbot.train(livetrainInverted);
            chatbot.train(livetrain)
            f.seek(0);
            f.truncate();
            f2.seek(0);
            f2.truncate();
            livetrain = [];
            livetrainInverted = [];
        #     f.close();
        # return chatbot.get_response(query)
        resp = chatbot.get_response(query);
        # previousResponse_1 = read(session_id)[-1]["message"];
        # previousResponse_2 = read(session_id)[-2]["message"];
        # print str(resp);
        # print previousResponse_1;
        # print previousResponse_2
        # if query == previousResponse_1 or query == previousResponse_2:
        #     resp = chatbot.get_response(query);
        f.write(str(resp)+"\n");
        f.write(query+"\n");
        f2.write(query+"\n");
        f2.write(str(resp)+"\n");
        f.close();
        f2.close();
        return resp;

print get_response(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])