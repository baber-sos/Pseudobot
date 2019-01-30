from chatterbot.chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import UbuntuCorpusTrainer


chatbot = ChatBot(
    'PseudoBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            "response_selection_method" : "chatterbot.response_selection.get_first_response"

        },
        {
            'import_path' : 'chatterbot.logic.MathematicalEvaluation'
        }
    ]

)



print "Trained"
while (True):
    message = str(raw_input())
    print chatbot.get_response(message)






