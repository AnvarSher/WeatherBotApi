import os, requests

class Bot:
	def __init__(self):
		self.token = os.environ.get("BOT_TOKEN")

	def sendMessage(self, userid, message):
		url = self.getUrl() + 'sendMessage'
		data = {
			'chat_id': userid,
			'text': message
		}
		return requests.post(url, json=data)

	def sendMe(self, message):
		self.sendMessage('537908946', message)

	def getUrl(self):
		return 'https://api.telegram.org/bot' + self.token + '/'