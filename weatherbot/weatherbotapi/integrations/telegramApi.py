import os
import requests


class TelegramApi:
	TOKEN = os.environ.get("BOT_TOKEN")

	@staticmethod
	def send_message(userid: str, message: str):
		try:
			TelegramApi._send_message(userid, message)
			return True
		except requests.exceptions.RequestException as e:
			# TODO: add logging
			return False

	@staticmethod
	def _send_message(userid: str, message: str):
		url = TelegramApi._get_url() + 'sendMessage'
		data = {
			'chat_id': userid,
			'text': message
		}
		r = requests.post(url, json=data)
		r.raise_for_status()

	@staticmethod
	def _get_url():
		return 'https://api.telegram.org/bot{}/'\
			.format(TelegramApi.TOKEN)
