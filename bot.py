import vk_api
import random
import json
from collections import defaultdict
from vk_api.longpoll import VkLongPoll, VkEventType



# API-ключ созданный ранее
token = open('api_key.txt', 'r').read()

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)



actions = dict()

with open("index.json") as f:
	index = json.load(f)

for key in index:
	with open(index[key]) as f:
		actions[key] = json.load(f)
		if "keyboard" in actions[key]:
			actions[key]["keyboard"] = json.dumps(actions[key]["keyboard"])


ends = ["ДЛЯ ФИЗИЧЕСКИХ ЛИЦ", "ДЛЯ ЮРИДИЧЕСКИХ ЛИЦ"]



clients_choices = defaultdict(str)

def update_choice(used_id, msg):
	s = clients_choices[used_id] or "__"
	_type, _action = s[0], s[1]
	if msg == "ДЛЯ ФИЗИЧЕСКИХ ЛИЦ":
		clients_choices[used_id] = 'f' + _action
	elif msg == "ДЛЯ ЮРИДИЧЕСКИХ ЛИЦ":
		clients_choices[used_id] = 'u' + _action
	elif msg == "ОФОРМИТЬ ПРОПУСК":
		clients_choices[used_id] = _type + 'o'
	elif msg == "ПРОДЛИТЬ ПРОПУСК":
		clients_choices[used_id] = _type + 'p'


form_url = {
	'fo': "https://forms.yandex.ru/u/5eab9f766b9552251a8c1a25/",
	'fp': "https://forms.yandex.ru/u/5eab9f766b9552251a8c1a25/",
	'uo': "https://forms.yandex.ru/u/5eab9f766b9552251a8c1a25/",
	'up': "https://forms.yandex.ru/u/5eab9f766b9552251a8c1a25/"
}

class VkBot:
	def __init__(self, user_id):
		print("Создан объект бота!")
		self._USER_ID = user_id
		self.random_id = random.randint(0, 2**64)




	def new_message(self, message):
		update_choice(self._USER_ID, message.upper())

		if message.upper() in actions:
			return actions[message.upper()]
		elif message.upper() in ends:
			if clients_choices[self._USER_ID] in form_url:
				return {"message": "Пожалуйста, заполните форму: " + form_url[clients_choices[self._USER_ID]]}
			else:
				return actions["error"]
		else:
			return actions["error"]






print("Server started")
for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW:
		if event.to_me:

			print('New message:')
			print(f'For me by: {event.user_id}')
			print('Text: ', event.text)
			bot = VkBot(event.user_id)
			ans = bot.new_message(event.text)
			ans.update({'user_id': event.user_id, 'random_id': bot.random_id})
			vk.method('messages.send', ans)

			#debug
			print(ans)
