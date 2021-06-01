import os, requests

class TelegramApi:
	TOKEN = os.environ.get("BOT_TOKEN")


	def sendMessage(userid: str, message: str):
		try:
			TelegramApi._sendMessage(userid, message)
			return True
		except Exception as ex:
			return False ## TODO: add logging


	def _sendMessage(userid: str, message: str):
		url = TelegramApi._getUrl() + 'sendMessage'
		data = {
			'chat_id': userid,
			'text': message
		}
		requests.post(url, json=data)


	def _getUrl():
		return 'https://api.telegram.org/bot' + TelegramApi.TOKEN + '/'