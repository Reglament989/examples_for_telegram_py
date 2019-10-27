# import re

# message = '/container Hello My file'
# readyoutube = re.findall(r'awdawdawdawdawd ', message)
# print(readyoutube)
import requests, os, io, re, telebot, zipfile
from exampls import token_FILE
from datetime import datetime
from random import random
from threading import Thread
from shutil import rmtree
from time import sleep

global nocheck
nocheck = False

whs = telebot.types.InlineKeyboardMarkup(row_width=1)
whs1 = telebot.types.InlineKeyboardButton(text="Video", callback_data="Video")
whs2 = telebot.types.InlineKeyboardButton(text="Voice", callback_data="Voice")
whs3 = telebot.types.InlineKeyboardButton(text="Audio", callback_data="Audio")
whs4 = telebot.types.InlineKeyboardButton(text="Photo", callback_data="Photo")
whs5 = telebot.types.InlineKeyboardButton(text="File", callback_data="File")
whs.add(whs1,whs2,whs3,whs4,whs5)

yrd = telebot.types.InlineKeyboardMarkup(row_width=1)
yrd1 = telebot.types.InlineKeyboardButton(text="Yes", callback_data="goput")
yrd2 = telebot.types.InlineKeyboardButton(text="No", callback_data="stopput")
yrd.add(yrd1,yrd2)

ydd = telebot.types.InlineKeyboardMarkup(row_width=1)
ydd1 = telebot.types.InlineKeyboardButton(text="Yes", callback_data="delall")
ydd2 = telebot.types.InlineKeyboardButton(text="No", callback_data="notdell")
ydd.add(ydd1,ydd2)

crypt_y_n = telebot.types.InlineKeyboardMarkup(row_width=1)
crypt_y = telebot.types.InlineKeyboardButton(text="Yes", callback_data="c_yes")
crypt_n = telebot.types.InlineKeyboardButton(text="No", callback_data="c_no")
crypt_y_n.add(crypt_y,crypt_n)

File_manageBOT_TOKEN = ''
# File_manageBOT_TOKEN = token_FILE
File_manageBOT = telebot.TeleBot(File_manageBOT_TOKEN)


def open_and_write(path_to_download,message,msg_type):
	url = 'https://api.telegram.org/file/bot{t}/{path}'.format(t=token_FILE,path=path_to_download)
	search = re.split(r'/', path_to_download, maxsplit=1)[-1]
	out_file_name = '{n}'.format(n=search)
	# print(os.getcwd())
	mypath = os.getcwd() +'/'+ msg_type +'/'+ str(message.chat.id)
	if not os.path.isdir(mypath):
		os.makedirs(mypath)

	with open(os.path.join(mypath, out_file_name), 'wb') as out_stream:
		req = requests.get(url, stream=True)
		for chunk in req.iter_content(1024):
			out_stream.write(chunk)
	print("!!!!FILE SAVED!!!!")
	File_manageBOT.send_message(message.chat.id, text='Resived 200, OK')

def Send_FollowType(message,follow_type):
	mypath = os.getcwd() +'/'+ follow_type +'/'+ str(message.chat.id)
	if os.path.exists(mypath):
		path = os.listdir(mypath)
		files = []
		for add in path:
			r = mypath +'/'+ add
			files.append(r)
		for send_path in files:
			# print(send_path)
			with open(send_path, 'rb') as sp:
				if follow_type == 'photo':
					File_manageBOT.send_chat_action(message.chat.id, 'upload_photo')
					File_manageBOT.send_photo(message.chat.id, sp)
				elif follow_type == 'video':
					File_manageBOT.send_chat_action(message.chat.id, 'upload_video')
					File_manageBOT.send_video(message.chat.id, sp)
				elif follow_type == 'audio':
					File_manageBOT.send_chat_action(message.chat.id, 'upload_audio')
					File_manageBOT.send_audio(message.chat.id, sp)
				elif follow_type == 'files':
					File_manageBOT.send_chat_action(message.chat.id, 'upload_document')
					File_manageBOT.send_document(message.chat.id, sp)
				elif follow_type == 'voice':
					File_manageBOT.send_chat_action(message.chat.id, 'record_audio')
					File_manageBOT.send_voice(message.chat.id, sp)
				# else:
				# 	File_manageBOT.send_message(message.chat.id, text='GET ERROR')
				# 	ERROR = True
				# 	break
		# if ERROR == True:
		# 	pass
		# else:
		File_manageBOT.send_message(message.chat.id, text='Resived all!')
	else:
		File_manageBOT.send_message(message.chat.id, text='You not have {f}'.format(f=follow_type))

def check_time():
	for q in range(10):
		# d = str(datetime.now().strftime('%S'))
		print(random())

@File_manageBOT.message_handler(commands=['start'])
def start_FILE(message):
	File_manageBOT.send_message(message.chat.id, text='Hello send me file\nWont recive?\nUsing the BOT further, you agree with /policy', reply_markup=whs)

@File_manageBOT.message_handler(commands=['put'])
def Send_to_server(message):
	File_manageBOT.send_message(message.chat.id, text='Your realy wont send all data and clear my data?', reply_markup=yrd)

@File_manageBOT.message_handler(commands=['del'])
def Delete_to_server(message):
	File_manageBOT.send_message(message.chat.id, text='Your realy wont delete all data?', reply_markup=ydd)

@File_manageBOT.message_handler(commands=['get'])
def get_FILE(message):
	File_manageBOT.send_message(message.chat.id, text='What i do send you?', reply_markup=whs)


# @File_manageBOT.message_handler(commands=['decrypt'])
def decrypt(message):
	global nocheck
	nocheck = True
	msg = File_manageBOT.send_message(message.chat.id, text='Send me main archive')
	File_manageBOT.register_next_step_handler(msg, checker_archive)

def save_decrypt_send(message,path_to_download):
	url = 'https://api.telegram.org/file/bot{t}/{path}'.format(t=token_FILE,path=path_to_download)
	search = re.split(r'/', path_to_download, maxsplit=1)[-1]
	out_file_name = '{n}'.format(n=search)
	# print(os.getcwd())
	mypath = os.getcwd()
	with open(os.path.join(mypath, out_file_name), 'wb') as out_stream:
		req = requests.get(url, stream=True)
		for chunk in req.iter_content(1024):
			out_stream.write(chunk)
	print(out_file_name)
	with zipfile.ZipFile(out_file_name, 'r') as zfile:
		for name in zfile.namelist():
			if re.search(r'/.zip', name) != None:
				zfiledata = io.BytesIO(zfile.read(name))
				with zipfile.ZipFile(zfiledata) as zfile2:
					for name2 in zfile2.namelist():
						print(name2)

# @File_manageBOT.message_handler(content_types=['document'])
def checker_archive(message):
	# print(message)
	while True:
		if message.content_type == 'document':
			FileID = message.document.file_id
			file = File_manageBOT.get_file(FileID)
			path_to_download = file.file_path
			File_manageBOT.send_message(message.chat.id, text='OK')
			global nocheck
			nocheck = False
			save_decrypt_send(message,path_to_download)
		else:
			File_manageBOT.send_message(message.chat.id, text='ERROR')
			break

@File_manageBOT.message_handler(commands=['policy'])
def get_policy(message):
	File_manageBOT.send_message(message.chat.id, text="""
This BOT saves everything it receives except text, and you can get these files at any time in the chat or in the archive from Anonfiles.com
for any question contact @anonim_too
""")

@File_manageBOT.message_handler(commands=['help'])
def get_policy(message):
	File_manageBOT.send_message(message.chat.id, text="""
You should know that for all actions you are responsible for yourself, this BOT does not bear any responsibility for the information received because you have lost
""")

@File_manageBOT.message_handler(content_types=['photo'])
def getFileID_PHOTO(message):
	FileID = message.photo[-1].file_id
	file = File_manageBOT.get_file(FileID)
	path_to_download = file.file_path
	potok_download = Thread(target=open_and_write,args=(path_to_download,message,'photo',))
	potok_download.start()
	potok_download.join()

@File_manageBOT.message_handler(content_types=['audio'])
def getFileID_AUDIO(message):
	FileID = message.audio.file_id
	file = File_manageBOT.get_file(FileID)
	path_to_download = file.file_path
	potok_download = Thread(target=open_and_write,args=(path_to_download,message,'audio',))
	potok_download.start()
	potok_download.join()

@File_manageBOT.message_handler(content_types=['document'])
def getFileID_DOCUMENT(message):
	global nocheck
	if nocheck == False:
		FileID = message.document.file_id
		file = File_manageBOT.get_file(FileID)
		path_to_download = file.file_path
		potok_download = Thread(target=open_and_write,args=(path_to_download,message,'files',))
		potok_download.start()
		potok_download.join()
	else:
		pass

@File_manageBOT.message_handler(content_types=['video'])
def getFileID_VIDEO(message):
	FileID = message.video.file_id
	file = File_manageBOT.get_file(FileID)
	path_to_download = file.file_path
	potok_download = Thread(target=open_and_write,args=(path_to_download,message,'video',))
	potok_download.start()
	potok_download.join()

@File_manageBOT.message_handler(content_types=['video_note'])
def getFileID_VIDIONOTE(message):
	FileID = message.video_note.file_id
	file = File_manageBOT.get_file(FileID)
	path_to_download = file.file_path
	potok_download = Thread(target=open_and_write,args=(path_to_download,message,'video',))
	potok_download.start()
	potok_download.join()

@File_manageBOT.message_handler(content_types=['voice'])
def getFileID_VOICE(message):
	FileID = message.voice.file_id
	file = File_manageBOT.get_file(FileID)
	path_to_download = file.file_path
	potok_download = Thread(target=open_and_write,args=(path_to_download,message,'voice',))
	potok_download.start()
	potok_download.join()

def check_data_user(message):
	_dir = os.getcwd()
	follow_type = ['video','voice','audio','photo','files']
	dirs = []
	for j in follow_type:
		d = _dir +'/'+ j +'/'+ str(message.chat.id)
		if os.path.exists(d):
			dirs.append(d)
			# print(d)
			break
		else:
			pass
	# print(dirs)
	if dirs != []:
		return True
	else:
		return False

def Send_AllData_and_ClearBotData(message=None, crypt=False, path_user=None, t_type=False):
	try:
		c_chat = message.chat.id
	except:
		c_chat = "auto"
	try:
		c = check_data_user(message)
	except:
		c = True
	# print(c)
	if c == True:
		if crypt == True:
			from Crypto.Cipher import AES
			from Crypto import Random
			from re import split
			key = Random.new().read(AES.block_size)
			iv = Random.new().read(AES.block_size)
			passwordd = key + b'split' + iv
			with open('password', 'wb') as f:
				f.write(passwordd)
		else:
			pass
		follow_type = ['video','voice','audio','photo','files']
		dir_path = os.getcwd()
		crypt_path = []
		for j in follow_type:
			if t_type == True:
				for k in range(5):
					path = dir_path +'/'+ j
					for root, dirs, files in os.walk(path):
						for _dir in dirs:
							d = dir_path +'/'+ j +'/'+ _dir
							crypt_path.append(d)
							c_chat = _dir
			else:
				try:
					path = dir_path +'/'+ j +'/'+ path_user
				except:
					path = None
				if path != None:
					crypt_path.append(path)
		ziph = zipfile.ZipFile('{0}.zip'.format(c_chat), 'w', zipfile.ZIP_DEFLATED)
		for lgrt in crypt_path:
			for root, dirs, files in os.walk(lgrt):
				for file in files:
					data = os.path.join(lgrt +'/'+ file)
					with open(data, 'rb') as they:
						d = they.read()
					if crypt == True:
						cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
						enc_data = cfb_cipher.encrypt(d)
					else:
						enc_data = d
					with open(data, 'wb') as bgr:
						finnale = bgr.write(enc_data)
					ziph.write(data, file)
					rmtree(lgrt)
		if crypt == True:
			dir_pass_pass = os.getcwd() + '/password'
			dir_pass_decrypt = os.getcwd() + '/decrypt_FINALLY'
			ziph.write(dir_pass_pass, 'password')
			ziph.write(dir_pass_decrypt, 'decrypt_FINALLY')
			os.remove(dir_pass_pass)
		else:
			pass
		ziph.close()
		print(c_chat)
		dir_zip = os.getcwd() + '/{id}.zip'.format(id=str(c_chat))
		if t_type == True:
			auto = True
			_id = c_chat
			send_Anonim_Files(dir_zip=dir_zip, _id=_id, auto=auto)
		else:
			auto = False
			send_Anonim_Files(dir_zip=dir_zip, message=message, auto=auto)
	elif c == False:
		File_manageBOT.send_message(message.chat.id, "You not have any data")
	else:
		pass

def send_status(message,status,cools):
	num = 0
	while num < cools:
		sleep(5)
		File_manageBOT.send_chat_action(message.chat.id, status)
		num += 1


def send_Anonim_Files(dir_zip, auto, message=None,_id=None):
	print(_id)
	if auto != True:
		potok_download276 = Thread(target=send_status,args=(message,'upload_document', 5))
		potok_download276.start()
		potok_download276.join()
	else:
		pass
	f = open('%s' % dir_zip, 'rb')
	files = {'file': ('%s' % 'Your_data.zip', f)}
	r = requests.post('https://api.anonfiles.com/upload', files= files)
	f.close()
	response = r.json()
	url = response['data']['file']['url']['full']
	if auto:
		File_manageBOT.send_message(chat_id=_id, text='Sorry, the file expired, we apologize\nYour url to get files - '+url+'')
	else:
		File_manageBOT.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Your data succefull sending to Anonfiles\n'+url+'\nYou can get her with url')
	os.remove(dir_zip)


def Delete_allData_fromUser(message):
	follow_type = ['video','voice','audio','photo','files']
	del_path = []
	for t in follow_type:
		mypath = os.getcwd() +'/'+ t +'/'+ str(message.chat.id)
		del_path.append(mypath)
	# print(del_path)
	for d in del_path:
		if os.path.exists(d):
			rmtree(d)
		else:
			pass
	File_manageBOT.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='All data for you deleted')


@File_manageBOT.callback_query_handler(func=lambda c:True) # Раздел со всеми .data перемeнными 
def inlin_FILE(c):
	# print(c.message) Voice Audio Photo
	if c.data == 'Video':
		# Send_FollowType(c.message, 'video')
		potok_download = Thread(target=Send_FollowType,args=(c.message,'video',))
		potok_download.start()
		potok_download.join()
	elif c.data == 'Voice':
		# Send_FollowType(c.message, 'voice')
		potok_download1 = Thread(target=Send_FollowType,args=(c.message,'voice',))
		potok_download1.start()
		potok_download1.join()
	elif c.data == 'Audio':
		# Send_FollowType(c.message, 'audio')
		potok_download2 = Thread(target=Send_FollowType,args=(c.message,'audio',))
		potok_download2.start()
		potok_download2.join()
	elif c.data == 'Photo':
		# Send_FollowType(c.message, 'photo')
		potok_download3 = Thread(target=Send_FollowType,args=(c.message,'photo',))
		potok_download3.start()
		potok_download3.join()
	elif c.data == 'File':
		# Send_FollowType(c.message, 'files') 
		potok_download4 = Thread(target=Send_FollowType,args=(c.message,'files',))
		potok_download4.start()
		potok_download4.join()
	elif c.data == 'goput':
		File_manageBOT.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='You wont encrypt your data?\n(experemental, only linux user)', reply_markup=crypt_y_n)
	elif c.data == 'stopput':
		File_manageBOT.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Okey send me /put and im send all data to Hosting files')
	elif c.data == 'delall':
		Delete_allData_fromUser(c.message)
	elif c.data == 'c_yes':
		crypt = True
		path_user = str(c.message.chat.id)
		File_manageBOT.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Proccesing...')
		potok_download445 = Thread(target=Send_AllData_and_ClearBotData,args=(c.message,crypt))
		potok_download445.start()
		potok_download445.join()
	elif c.data == 'c_no':
		crypt = False
		path_user = str(c.message.chat.id)
		File_manageBOT.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Proccesing...')
		potok_download445 = Thread(target=Send_AllData_and_ClearBotData,args=(c.message,crypt))
		potok_download445.start()
		potok_download445.join()

def callback_data():
	print("CALL callbackdata")
	while True:
		sleep(5)
		crypt = False
		t_type = True
		print("Call send")
		Send_AllData_and_ClearBotData(crypt=crypt,t_type=t_type)

# File_manageBOT.set_update_listener(callback_data)

def main():
	# from exampls import token_FILE, host_flask, port_flask
	from flask import Flask, request
	app = Flask(__name__)
	@app.route('/', methods=['GET'], endpoint='index')
	def index():
		return f"Hello", 200
	@app.route('/{t}/'.format(t=''), methods=['POST', 'GET'], endpoint='listen_File_manageBOT')
	def listen_File_manageBOT():
		if request.method == 'POST':
			File_manageBOT.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
		return f""
	app.run(host='0.0.0.0', port=9797, debug=True)

if __name__ == '__main__':
	potok_download678 = Thread(target=main)
	potok_download678.start()
	potok_download678.join()
	potok_download321 = Thread(target=callback_data)
	potok_download321.start()
	potok_download321.join()