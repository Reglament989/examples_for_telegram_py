import requests, json, re, telebot, os
from exampls import tk
from random import randint
from datetime import datetime
from time import sleep
from texts import macrosts, randommessage
import telebot
global PHOTO

URL = "https://api.telegram.org/bot{0}/{1}"

ADMIN_BOT_token = tk
# ADMIN_BOT_token = ''
ADMIN_BOT = telebot.TeleBot(ADMIN_BOT_token)

def listener(messages):
	# pass
	for message in messages:
		if message.from_user.is_bot:
			try:
				ADMIN_BOT.kick_chat_member(message.chat.id, message.from_user.id)
			except:
				pass
		else:
			pass
		if message.chat.type == 'group':
			ADMIN_BOT.leave_chat(message.chat.id)
		elif message.chat.type == 'channel':
			ADMIN_BOT.leave_chat(message.chat.id)

@ADMIN_BOT.message_handler(content_types=['new_chat_members'])
def WelcomeUsers(message):
	if message.new_chat_member.is_bot:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)
		ADMIN_BOT.kick_chat_member(message.chat.id, message.new_chat_member.id)
	else:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)
		if message.new_chat_member.username != None:
			nick = '@' + message.new_chat_member.username
		else:
			nick = message.new_chat_member.first_name
		welcommessage = macrosts['welcome'].format(nick=nick)
		ADMIN_BOT.send_message(message.chat.id, welcommessage)

@ADMIN_BOT.message_handler(content_types=['left_chat_member'])
def BayBayUsers(message):
	if message.left_chat_member.is_bot:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	else:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)
		if message.left_chat_member.last_name != None:
			lname = message.left_chat_member.last_name
		else:
			lname = ''
		
		if message.left_chat_member.username != None:
			nick = '@' + message.left_chat_member.username
		else:
			nick = message.left_chat_member.first_name
		bbmessage = macrosts['text_bb'].format(nick,randommessage[randint(0, randommessage[-1])].format(first=message.left_chat_member.first_name,last=lname))
		ADMIN_BOT.send_message(message.chat.id, bbmessage)

def AUTOMUTE(message):
	if checkadmin(message) == True:
		if checkadmin(message, t_type='reply') == False:
			# print("MUTE {u}".format(u=message['reply_id']))
			ADMIN_BOT.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_send_messages=False)
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
			if message.reply_to_message.from_user.username != None:
				h = '@' + message.reply_to_message.from_user.username
			else:
				h = message.reply_to_message.from_user.first_name
			ADMIN_BOT.send_message(message.chat.id, macrosts['text_mute'].format(h))
			ADMIN_BOT.send_message(message.reply_to_message.from_user.id, "Тебе выдали мут :(\nОбратись [к этому парню](t.me/Help_horor_re_bot) если это ошибка", parse_mode='markdown')
		elif checkadmin(message, t_type='reply') == True:
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

def UNMUTE(message):
	if checkadmin(message) == True:
		if checkadmin(message, t_type='reply') == False:
			print("UNMUTE {0}".format(message.reply_to_message.from_user.id))
			ADMIN_BOT.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, can_send_messages=True,
                         can_send_media_messages=True, can_send_other_messages=True,
                         can_add_web_page_previews=True)
			# url = URL.format(ADMIN_BOT_token, 'promotechatmember')
			# response = requests.post(
			# 	url=url,data={'chat_id': message.chat.id, 'user_id': message.reply_to_message.from_user.id, 'can_post_messages':True}).json()
			# print(response)
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
			if message.reply_to_message.from_user.username != None:
				h = '@' + message.reply_to_message.from_user.username
			else:
				h = message.reply_to_message.from_user.first_name
			ADMIN_BOT.send_message(message.chat.id, macrosts['text_unmute'].format(h))
			ADMIN_BOT.send_message(message.reply_to_message.from_user.id, "У тебя сняли мут :)")
		elif checkadmin(message, t_type='reply') == True:
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

def KICK(message):
	if checkadmin(message) == True:
		if checkadmin(message, t_type='reply') == False:
			ADMIN_BOT.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
			ADMIN_BOT.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
			print("USER KICK {u}".format(u=message.reply_to_message.from_user.id))
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
			if message.reply_to_message.from_user.username != None:
				h = '@' + message.reply_to_message.from_user.username
			else:
				h = message.reply_to_message.from_user.first_name
			ADMIN_BOT.send_message(message.chat.id, macrosts['text_kick'].format(h))
			ADMIN_BOT.send_message(message.reply_to_message.from_user.id, "Ты был кикнут, печалька :(\nОбратись [к этому парню](t.me/Help_horor_re_bot) если это ошибка", parse_mode='markdown')
		elif checkadmin(message, t_type='reply') == True:
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

def BAN(message):
	regular = re.split(' ', message.text, maxsplit=1)
	if checkadmin(message) == True:
		if checkadmin(message, t_type='reply') == False:
			if message.from_user.username != None:
				adm = '@' + message.from_user.username
			else:
				adm = message.from_user.first_name
			if message.reply_to_message.from_user.username != None:
				user = '@' + message.reply_to_message.from_user.username
			else:
				user = message.reply_to_message.from_user.first_name
			why_ban = ''
			if regular[-1] != '/ban':
				why_ban = regular[-1]
			ADMIN_BOT.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
			print("BAN USER {y}".format(y=message.reply_to_message.from_user.id))
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
			ADMIN_BOT.send_message(message.chat.id, macrosts['text_ban'].format(user, adm, why_ban))
			ADMIN_BOT.send_message(message.reply_to_message.from_user.id, "Тебя забанили :(\nОбратись [к этому парню](t.me/Help_horor_re_bot) если это ошибка", parse_mode='markdown')
		elif checkadmin(message, t_type='reply') == True:
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

def checkadmin(message, t_type='user'):
	if t_type == 'reply':
		i_d = message.reply_to_message.from_user.id
	elif t_type == 'user':
		i_d = message.from_user.id
	response = ADMIN_BOT.get_chat_member(message.chat.id, i_d)
	if response.status == 'creator' or response.status ==  "administrator":
		return True
	else:
		return False

def check_reply(message):
	try:
		a = message.reply_to_message
	except:
		a = None
	if a != None:
		return True
	else:
		return False

def ID(message):
	if check_reply(message) == True:
		response = ADMIN_BOT.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
		# print(response)
		if response.status ==  "administrator":
			st = "Администратор"
		elif response.status ==  "kicked":
			st = "Забанен"
		elif response.status ==  "left":
			st = "Не имеем такого"
		elif response.status ==  "member":
			st = "Обычный смертный"
		elif response.status ==  "creator":
			st = "БОЖЕНЬКА"
		elif response.status ==  "restricted":
			st = "Заглушен кляпом"
		else:
			st = "none"
		if message.reply_to_message.from_user.username != None:
			nick = '@' + message.reply_to_message.from_user.username
		else:
			nick = message.reply_to_message.from_user.first_name
		ADMIN_BOT.send_message(message.chat.id, macrosts['text_id'].format(id=message.reply_to_message.from_user.id,n=nick,st=st))
	elif check_reply(message) == False:
		ADMIN_BOT.send_message(message.chat.id, 'Попробуй ответить на чье-то сообщение')

def UNBAN(message):
	if checkadmin(message) == True:
		if checkadmin(message, t_type='reply') != True:
			ADMIN_BOT.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
			# print("UNBAN USER {y}".format(y=message['reply_id']))
			if message.reply_to_message.from_user.username != None:
				nick = '@' + message.reply_to_message.from_user.username
			else:
				nick = message.reply_to_message.from_user.first_name
			# url = URL.format(tk=tk, method="sendMessage")
			# url = url + '?chat_id={chat_id}&text={text}'.format(chat_id=message['chat_id'],text='Разбанил бедолагу {n}'.format(n=nick))
			# r = requests.get(url)
			ADMIN_BOT.send_message(message.chat.id, macrosts['text_unban'].format(nick))
			ADMIN_BOT.send_message(message.reply_to_message.from_user.id, "Тебя разбанили :)\nПоздравляю тебя\nОбратись [к этому парню](t.me/Help_horor_re_bot) если это ошибка", parse_mode='markdown')
		elif checkadmin(message, t_type='reply') == True:
			ADMIN_BOT.delete_message(message.chat.id, message.message_id)
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

def PURGE(message):
	if checkadmin(message) == True:
		b = message.message_id
		msg_id = message.reply_to_message.message_id
		while msg_id <= b:
			try:
				ADMIN_BOT.delete_message(message.chat.id, msg_id)
			except:
				pass
			msg_id += 1
			# print(msg_id)
		ADMIN_BOT.send_message(message.chat.id, "Очистка заверщена!")
	elif checkadmin(message) == False:
		ADMIN_BOT.delete_message(message.chat.id, message.message_id)

@ADMIN_BOT.message_handler(commands=['start'])
def start(message):
	ADMIN_BOT.send_message(message.chat.id, "hello")

@ADMIN_BOT.message_handler(commands=['mute'])
def mute(message):
	AUTOMUTE(message)

@ADMIN_BOT.message_handler(commands=['unmute'])
def unmute(message):
	UNMUTE(message)

@ADMIN_BOT.message_handler(commands=['info', 'help'])
def info(message):
	ADMIN_BOT.send_message(message.chat.id, macrosts['info'])

@ADMIN_BOT.message_handler(commands=['ban'])
def ban_cmd(message):
	BAN(message)

@ADMIN_BOT.message_handler(commands=['cmd'])
def cmd_cmd(message):
	ADMIN_BOT.send_message(message.chat.id, macrosts['cmd'])

@ADMIN_BOT.message_handler(commands=['events'])
def cmd_cmd(message):
	ADMIN_BOT.send_message(message.chat.id, macrosts['events'])

@ADMIN_BOT.message_handler(commands=['rules'])
def rul_cmd(message):
	ADMIN_BOT.send_message(message.chat.id, macrosts['rules'], parse_mode='markdown')

@ADMIN_BOT.message_handler(commands=['kick'])
def kick_cmd(message):
	KICK(message)

@ADMIN_BOT.message_handler(commands=['unban'])
def unban_cmd(message):
	UNBAN(message)

@ADMIN_BOT.message_handler(commands=['id'])
def id_cmd(message):
	ID(message)

@ADMIN_BOT.message_handler(commands=['purge'])
def deletemsg_purge(message):
	PURGE(message)

@ADMIN_BOT.message_handler(regexp="Шутка")
def deletemsg_purge(message):
	ADMIN_BOT.send_message(message.chat.id, "Тут могла бы быть шутка")

def main():
	# from exampls import token_FILE, host_flask, port_flask
	from flask import Flask, request
	app = Flask(__name__)
	@app.route('/', methods=['GET'], endpoint='index')
	def index():
		return f"Hello", 200
	@app.route('/{t}/'.format(t=''), methods=['POST', 'GET'], endpoint='listen_ADMINBOT')
	def listen_ADMINBOT():
		if request.method == 'POST':
			ADMIN_BOT.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
			# File_manageBOT.set_update_listener(Checker_class().name())
		return f""
	app.run(host='0.0.0.0', port=9797, debug=True)

ADMIN_BOT.set_update_listener(listener)
if __name__ == '__main__':
	main()