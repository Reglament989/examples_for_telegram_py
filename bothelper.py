import telebot
from exampls import token_help
from datetime import datetime
import os

PHOTO = None
POST_REQUEST = {'file_id': None, 'text':None,'date':None, 'nickname':None}
RESPONSE_OBJ = {'id': None, 'text': None}
########## TELEBOT ##########
TOKEN = token_help
bot = telebot.TeleBot(TOKEN)
########## TELE KEYBOARDS ##########
start_key = telebot.types.InlineKeyboardMarkup(row_width=1)
but1 = telebot.types.InlineKeyboardButton(text="Да, у меня есть к тебе вопрос", callback_data="yes")
but2 = telebot.types.InlineKeyboardButton(text="Нет, я просто проверяю тебя", callback_data="no")
start_key.add(but1,but2)

ifknow = telebot.types.InlineKeyboardMarkup(row_width=1)
ifbut1 = telebot.types.InlineKeyboardButton(text="Да, я уверен!", callback_data="ifyes")
ifbut2 = telebot.types.InlineKeyboardButton(text="Нет, я не уверен!", callback_data="ifno")
ifknow.add(ifbut1,ifbut2)

iffile = telebot.types.InlineKeyboardMarkup(row_width=1)
filebutton1 = telebot.types.InlineKeyboardButton(text="Да", callback_data="fileyes")
filebutton2 = telebot.types.InlineKeyboardButton(text="Нет", callback_data="fileno")
iffile.add(filebutton1,filebutton2)
########## TXT ##########
text = {
	'welcome':"""
Привет, если ты обратился ко мне значит у тебя появилась проблема при использовании бота
Верно?""",
	'post':"""
Еще какие-то вопросы?""",
	'makros':"""
Спасибо за обращение в нашу службу поддержки!
Наш администратор ответил на ваш вопрос\n"""
}
########## TELEBOT ##########
@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, text=text['welcome'], reply_markup=start_key)

@bot.message_handler(commands=['response'])
def start(message):
	msg = bot.send_message(message.chat.id, text='Кому отвечаем?')
	bot.register_next_step_handler(msg, _response)
@bot.message_handler(commands=['post'])
def start(message):
	bot.send_message(message.chat.id, text=text['post'], reply_markup=start_key)

@bot.message_handler(commands=['idea'])
def start(message):
	request_help(message,status='idea')

def _response(message):
	RESPONSE_OBJ['id'] = message.text
	msg = bot.send_message(message.chat.id, text='Что ответим?')
	bot.register_next_step_handler(msg, response_text)

def response_text(message):
	RESPONSE_OBJ['text'] = message.text
	bot.send_message(chat_id=RESPONSE_OBJ['id'], text=text['makros'] + RESPONSE_OBJ['text'])

def request_help(message,status=None):
	if status == 'idea':
		msg = bot.send_message(chat_id=message.chat.id, text = 'Внимательно тебя слушаю О_о')
	elif status == None:
		msg = bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
	            text = 'Хорошо попытайся как можно подробней описать свою проблему')
	with open('{0}.txt'.format(message.chat.id), 'w') as f:
		f.write('1')
	bot.register_next_step_handler(msg, check_request)

def ifyouknow(message,status):
	if status == True:
		# with open('test.txt', 'w') as f:
		# 	f.write(message.text)
		POST_REQUEST['nickname'] = str(message.from_user.id)
		bot.send_message(message.chat.id, 'Хочешь прикрепить фото?', reply_markup=iffile)
		# bot.send_message(message.chat.id, '')
	elif status == False:
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
            text = 'Попробуй еще раз (/post)')

# @bot.callback_query_handler(func=lambda c:True)
def check_request(message):
	# print(message)
	if len(message.text) < 10:
		POST_REQUEST['text'] = message.text
		bot.send_message(message.chat.id, 'Ты уверен(a) что это все что мне нужно знать?', reply_markup=ifknow)
		# bot.register_next_step_handler(msg, ifyouknow)
	# elif message.content_types ==  
	else:
		POST_REQUEST['text'] = message.text
		POST_REQUEST['nickname'] = str(message.from_user.id)
		bot.send_message(message.chat.id, 'Хочешь прикрепить фото?', reply_markup=iffile)
		try:
			os.remove('{u}.txt'.format(u=message.chat.id))
		except:
			pass

def check_photo(message, status):
	if status == True:
		bot.send_message(message.chat.id, 'Отправь мне фото')
		global PHOTO
		PHOTO = True
	elif status == False:
		SEND_REQUEST(message)

def SEND_REQUEST(message):
	POST_REQUEST['date'] = str(datetime.now().strftime('%Y-%m-%d\n%H:%M\n'))
	bot.send_message(message.chat.id, 'Отправил твое сообщение на обработку!')
	bot.send_message('YOUR_ID',POST_REQUEST['date'] + POST_REQUEST['nickname'] +'\n'+ POST_REQUEST['text'])
	try:
		bot.send_photo('YOUR_ID', POST_REQUEST['file_id'])
	except:
		pass
	POST_REQUEST.clear()
	global PHOTO
	PHOTO = None
	try:
		os.remove('{0}.txt'.format(message.chat.id))
	except:
		pass

@bot.message_handler(content_types=['text'])
def photo_check(message):
	global PHOTO
	if PHOTO == True:
		bot.send_message(message.chat.id, 'Пожалуйста отправь мне фото вместо текста')
	elif PHOTO == None:
		bot.send_message(message.chat.id, 'Ты можешь оставить отчет об ошибке (/post)\nИли отправить нам идею для развития (/idea)')

@bot.message_handler(content_types=['photo'])
def photo(message):
	global PHOTO
	if PHOTO == True:
		POST_REQUEST['file_id'] = message.json['photo'][0]['file_id']
		# bot.send_message(message.chat.id, 'Отправил твое сообщение на обработку')
		# bot.send_photo(message.chat.id, idphoto)
		SEND_REQUEST(message)
	else:
		pass

@bot.callback_query_handler(func=lambda c:True) # Раздел со всеми .data перемeнными
def inlin(c):
	# print(c.message)
	if c.data == 'yes':
		try:
			with open('{0}.txt'.format(message.chat.id), 'r') as f:
				r = f.read()
		except:
			request_help(c.message)
	if c.data == 'no':
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
            text = 'Ты также можешь прислать мне свою идею для модификации(/idea)')
	elif c.data == 'ifyes':
		ifyouknow(c.message, status=True)
	elif c.data == 'ifno':
		ifyouknow(c.message, status=False)
	if c.data == 'fileyes':
		check_photo(c.message, status=True)
	elif c.data == 'fileno':
		check_photo(c.message, status=False)
