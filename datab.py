from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.ConversationData
collection = db.conversations
limit = 50
toShow = 10

def update(cookie_id, message, origin):
	cursor = collection.find({"id":cookie_id})
	if not cursor.count():
		collection.insert_one(
			{ 
				"id": cookie_id,
				"conversation": [{"message": message, "bot": origin}]
			})

	elif cursor.count() == 1: 
		newMsg = cursor[0][u'conversation']+[{"message": message, "bot": origin}]
		if (len(newMsg) > limit):
			newMsg = newMsg[1:]
		collection.update_one(
			{"id": cookie_id},
			{
				"$set": {
					"conversation": newMsg
			}
			})

def read(cookie_id):
	try:
		cursor = collection.find({"id": cookie_id})
		if cursor.count() == 0:
			return []
		if len(cursor[0][u'conversation']) >= toShow:
			return cursor[0][u'conversation'][-toShow:]
		else:
			return cursor[0][u'conversation']

	except Exception, e:
		print []
