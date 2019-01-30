import threading

class responseThread (threading.Thread):
    def __init__(self, chatbot, query):
        threading.Thread.__init__(self)
        self.bot = chatbot
        self.query = chatbot
        self.response = None
    def run(self):
	    self.response = chatbot.get_response(self.query)

