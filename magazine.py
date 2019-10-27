# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from random import randrange
import random
import telebot
from config import token
from telebot import types
import json
import datetime
import re
import sqlite3
import time
import os
### Нужные для работы бд inline keybords
enchangephonedb = types.InlineKeyboardMarkup()
ch1 = types.InlineKeyboardButton(text="Поменять", callback_data="changep")
ch2 = types.InlineKeyboardButton(text="Оставить как есть", callback_data="stayn")
enchangephonedb.add(ch1,ch2)

enchangenamedb = types.InlineKeyboardMarkup()
chn1 = types.InlineKeyboardButton(text="Поменять", callback_data="changen")
chn2 = types.InlineKeyboardButton(text="Оставить как есть", callback_data="stayn")
enchangenamedb.add(chn1,chn2)

ERROR = "Ошибка"
bot = telebot.TeleBot(token)

def sqlite3_create(message):
    def a(message):
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            print(data)
            if data != []: 
                for c in data:
                    if c == str(message.chat.id):
                        return True
                else:
                    return False

    sqlite_file = 'DB_file.db'    # name of the sqlite database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    columnname = "id"
    table = 'core_fes'
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    writer = (str(message.from_user.id),str(message.from_user.first_name),None,None,None,None)
    c.execute("""CREATE TABLE IF NOT EXISTS core_fes 
        (id TEXT,name TEXT,phone TEXT,longitude TEXT,latitude TEXT, admin INTEGER)
        """)
    if a(message) == False:
        c.execute('INSERT INTO '+ table +' VALUES(?, ?, ?, ?, ?, ?)', writer)
#else:
        #pass

    con.commit()
    con.close()

def sqlite3_createloc(message):
    sqlite_file = 'DB_file.db'    # name of the sqlite database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    column_name = "id"
    table = 'values_location'
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    writerloc = (str(message.from_user.id),None,None,None)
    c.execute("""CREATE TABLE IF NOT EXISTS values_location 
        (id TEXT,city TEXT,street TEXT,numh TEXT)
        """)
    c.execute('INSERT INTO '+ table +' VALUES(?, ?, ?, ?)', writerloc)
    #else:
        #pass

    con.commit()
    con.close()

def printdata(data):
    for line in data:
        print (line)
    print("Number of lines in database table is " + str(len(data)))

def sqlite3_update(message):
    sqlite_file = 'DB_file.db'    # name of the sqlite database file
    phone = message.contact.phone_number
    # Connecting to the database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    #c.execute('CREATE TABLE IF NOT EXISTS core_fes(id TEXT,''name TEXT,''phone TEXT)')
    #c.execute('INSERT INTO core_fes VALUES(?, ?, ?)', test)
    query = 'UPDATE core_fes SET phone = {ph} WHERE id = {id}'.format(id = str(message.chat.id), ph = phone)
    c.execute(query)

    con.commit()
    con.close()

def sqlite3_updateST(message, stlati, stlong):
    sqlite_file = 'DB_file.db'    # name of the sqlite database file
    # Connecting to the database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    #c.execute('CREATE TABLE IF NOT EXISTS core_fes(id TEXT,''name TEXT,''phone TEXT)')
    #c.execute('INSERT INTO core_fes VALUES(?, ?, ?)', test)
    query1 = 'UPDATE core_fes SET latitude = {lati} WHERE id = {id}'.format(id = str(message.chat.id), lati=stlati)
    query2 = 'UPDATE core_fes SET longitude = {long} WHERE id = {id}'.format(id = str(message.chat.id), long=stlong)
    c.execute(query1)
    c.execute(query2)

    con.commit()
    con.close()

def sqlite3_updateSTintext(message, city, street, numh):
    sqlite_file = 'DB_file.db'    # name of the sqlite database file
    # Connecting to the database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    #c.execute('CREATE TABLE IF NOT EXISTS core_fes(id TEXT,''name TEXT,''phone TEXT)')
    #c.execute('INSERT INTO core_fes VALUES(?, ?, ?)', test)
    query1 = 'UPDATE values_location SET city = "{c}" WHERE id = "{id}"'.format(id = str(message.chat.id), c=city)
    query2 = 'UPDATE values_location SET street = "{s}" WHERE id = "{id}"'.format(id = str(message.chat.id), s=street)
    query3 = 'UPDATE values_location SET numh = "{n}" WHERE id = "{id}"'.format(id = str(message.chat.id), n=numh)
    c.execute(query1)
    c.execute(query2)
    c.execute(query3)

    con.commit()
    con.close()

def sqlite3_updateUName(message, name):
    sqlite_file = 'DB_file.db'    # name of the sqlite database file

    # Connecting to the database file
    con = sqlite3.connect(sqlite_file)
    c = con.cursor()
    #c.execute('CREATE TABLE IF NOT EXISTS core_fes(id TEXT,''name TEXT,''phone TEXT)')
    #c.execute('INSERT INTO core_fes VALUES(?, ?, ?)', test)
    query = 'UPDATE core_fes SET name = "{nm}" WHERE id = {id}'.format(id = str(message.chat.id), nm = name)
    c.execute(query)

    con.commit()
    con.close()

def sqliteadmin(message):
    if message.text != 'Отмена':
        namefile = "{m}.txt".format(m=message.chat.id)
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is None:
            query = 'SELECT * FROM ' + table
            c.execute(query)
            data = c.fetchall()
        elif column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            msg = message.text
            for k in data:
                bot.send_message(chat_id = k, text = msg, parse_mode = "HTML", disable_web_page_preview = True)
        try:
            os.remove(namefile)
        except:
            pass
    else:
        bot.send_message(message.chat.id,"Отменил")
        pass
def sqliteadmindba(message, typem = None):
    Name_DB = 'DB_file.db'
    table = 'core_fes'
    column_name = None
    con = sqlite3.connect(Name_DB)
    c = con.cursor()
    query_columna = 'pragma table_info('+table+')'
    c.execute(query_columna)
    column_desck = c.fetchall()
    column_names = []
    for column in column_desck:
        column_names.append(column[1])
    # print(column_names)
    if column_name is None:
        query = 'SELECT * FROM ' + table
        c.execute(query)
        data = c.fetchall()
        num = 0
        lenn = len(data)
        if typem == None:
            bot.send_message(message.chat.id, text = 
                            """
Распределение идет по такому принципу:
id user
name user 
number phone user
longitude Долгота адрса
latitude Широта адреса 
admin являеться ли пользователь админом 1 да 0 нет
                            """, disable_web_page_preview = True)
            for p in range(lenn):
                for k in data[num]:
                    if k is not None:
                        bot.send_message(message.chat.id, text = k, disable_web_page_preview = True)
                    else:
                        pass
                num = num + 1
        elif typem == "lenlist":
            bot.send_message(message.chat.id, text= lenn, disable_web_page_preview = True)

def sqliteopen3(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is None:
            query = 'SELECT * FROM ' + table
            c.execute(query)
            data = c.fetchall()
        elif column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            for check in data:
                if check == str(message.chat.id):
                    query = 'SELECT "name" FROM {tb} WHERE "id" = {id}'.format(tb=table,id=check)
                    c.execute(query)
                    checkname = c.fetchall()
                    new_data = []
                    for element in checkname:
                        new_data.append(element[0])
                    checkname = new_data
                    del(new_data)
                    randomx = ["Вот что мне удалось найти",
                "Прошельстев базы данных я нашел",
                "Спустя несколько мгновений поиска я могу сказать что",
                "Результат поиска показал что","Вот что я нашел"]
                    idx = list(set(randomx[:]))
                    random.shuffle(idx)
                    bot.send_message(message.chat.id, text = "Проверяю базу данных...")
                    time.sleep(0.5)
                    bot.send_message(message.chat.id, text = str(idx[0]) + " ваше имя " + str(checkname[0]), reply_markup = enchangenamedb)
                else:
                    pass
def sqliteopenSTintextphone3(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
    def a(message):
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is None:
            query = 'SELECT * FROM ' + table
            c.execute(query)
            data = c.fetchall()
        elif column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            for check in data:
                if check == str(message.chat.id):
                    query = 'SELECT "longitude" FROM {tb} WHERE "id" = {id}'.format(tb=table,id=check)
                    c.execute(query)
                    longitude = c.fetchall()
                    print(longitude[0][0])
                    if longitude[0][0] == None:
                        return False
                    elif longitude[0][0] != None:
                        return True
                else:
                    return ERROR
    if a(message) == True:
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is None:
            query = 'SELECT * FROM ' + table
            c.execute(query)
            data = c.fetchall()
        elif column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            for check in data:
                if check == str(message.chat.id):
                    query = 'SELECT "longitude" FROM {tb} WHERE "id" = {id}'.format(tb=table,id=check)
                    c.execute(query)
                    longitude = c.fetchall()
                    new_data = []
                    for element in longitude:
                        new_data.append(element[0])
                    longitude = new_data
                    del(new_data)
                    query = 'SELECT "latitude" FROM {tb} WHERE "id" = {id}'.format(tb=table,id=check)
                    c.execute(query)
                    latitude = c.fetchall()
                    new_data = []
                    for element in latitude:
                        new_data.append(element[0])
                    latitude = new_data
                    del(new_data)
                    bot.send_message(message.chat.id, text = "Проверяю базу данных...")
                    time.sleep(0.5)
                    bot.send_location(chat_id=message.chat.id,
               latitude = longitude[0], longitude = latitude[0])#Funcion revers name(Имена наооборот)
                    bot.send_message(message.chat.id, text = "Желаете сменить свой адрес?", reply_markup = changefrom)
                else:
                    pass
    elif a(message) == False:
        bot.send_message(message.chat.id, text =
            """
***!!!ВНИМАНИЕ!!!***
**На ПК этот метод не** _работает_, [подробней](https://telegra.ph/Peredacha-mestopolozheniya-na-PK-08-23)
            """, reply_markup = pcuserbackkatalog, disable_web_page_preview = True, parse_mode = "Markdown")
        try:
            os.remove(namefile)
        except:
            pass
    elif a(message) == ERROR:
        bot.send_message(message.chat.id,
                """
Извините произошла ошибка(39), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                """, parse_mode = "HTML", disable_web_page_preview = True)
        try:
            os.remove(namefile)
        except:
            pass
def sqliteopenphone3(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
        Name_DB = 'DB_file.db'
        table = 'core_fes'
        column_name = "id"
        con = sqlite3.connect(Name_DB)
        c = con.cursor()
        query_columna = 'pragma table_info('+table+')'
        c.execute(query_columna)
        column_desck = c.fetchall()
        column_names = []
        for column in column_desck:
            column_names.append(column[1])
       # print(column_names)
        if column_name is "id":
            query = 'SELECT '+column_name+' FROM '+table
            c.execute(query)
            data = c.fetchall()
            new_data = []
            for element in data:
                new_data.append(element[0])
            data = new_data
            del(new_data)
            for check in data:
                if check == str(message.chat.id):
                    query = 'SELECT phone FROM {tb} WHERE "id" = {id}'.format(tb=table,id=check)
                    c.execute(query)
                    checkphone = c.fetchall()
                    new_data = []
                    for element in checkphone:
                        new_data.append(element[0])
                    checkphone = new_data
                    del(new_data)
                    randomx = ["Вот что мне удалось найти",
                "Прошельстев базы данных я нашел что",
                "Спустя несколько мгновений поиска я могу сказать что",
                "Результат поиска показал что","Вот что я нашел"]
                    idx = list(set(randomx[:]))
                    random.shuffle(idx)
                    bot.send_message(message.chat.id, text = "Проверяю базу данных...")
                    time.sleep(0.5)
                    if checkphone == ['']:
                        bot.send_message(message.chat.id, text = str(idx[0]) + " ваш номер телефона " + "неизвестен", reply_markup = enchangephonedb)
                    else:
                        bot.send_message(message.chat.id, text = str(idx[0]) + " ваш номер телефона " + str(checkphone[0]), reply_markup = enchangephonedb)
keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
mainmenu = types.KeyboardButton('Главное меню🏢')
keyboard.add(mainmenu)

keyboardphone = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
requestphone = types.KeyboardButton('Указать свой номер телефона', request_contact = True)
keyboardphone.add(requestphone)

keyST = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
getST = types.KeyboardButton('Отправить свое местоположение', request_location = True)
keyST.add(getST)

key = types.InlineKeyboardMarkup(row_width=1)
but_2 = types.InlineKeyboardButton(text="Список команд для бота🛎", callback_data="NumberTwo")
but_3 = types.InlineKeyboardButton(text="Личный кабинет🔑", callback_data="NumberTree")
but_4 = types.InlineKeyboardButton(text="Наш сайт📡", url = "https://primo.vip")
but_5 = types.InlineKeyboardButton(text="О боте🤖", callback_data="infobot")
key.add(but_2, but_3, but_5, but_4)


katalogkey = types.InlineKeyboardMarkup()
k1 = types.InlineKeyboardButton(text="🎁Выбор товара🎁", callback_data = "taketovar")
k2 = types.InlineKeyboardButton(text="⭐️Топ продаж⭐️", callback_data = "topitems")
k3 = types.InlineKeyboardButton(text="🚚Доставка🚚", callback_data = "delivery")
k12 = types.InlineKeyboardButton(text="👨‍💻Наши контакты👩‍💻", callback_data= "blockcontact")
k32 = types.InlineKeyboardButton(text="Наши отзывы👍", url = "https://primo.vip/testimonials")
k4 = types.InlineKeyboardButton(text="⏪Назад⏪", callback_data="k4data")
katalogkey.row(k1)
katalogkey.row(k2, k3)
katalogkey.row(k12)
katalogkey.row(k32)
katalogkey.row(k4)

backkeyboardtomenu = types.InlineKeyboardMarkup()
backkeyboardtomenu.add(k4)

kabinet = types.InlineKeyboardMarkup(row_width=1)
#kabnamedata = """text = 'Ваше имя: ' + '{nm}', callback_data = 'first_name_kab'""".format(nm=checkname)
#kabname = types.InlineKeyboardButton(kabnamedata)
#kabphonedata = """text = 'Ваш номер телефона: ' + '{ph}', callback_data = 'phone'""".format(ph=checkphone)
#kabphone = types.InlineKeyboardButton(kabphonedata)
kab1 = types.InlineKeyboardButton(text = "Ваш номер телефона☎️", callback_data = "phone")
kab2 = types.InlineKeyboardButton(text = "Ваше имя👤", callback_data = "first_name_kab")
kab3 = types.InlineKeyboardButton(text = "Адрес🏠", callback_data = "from_kab")
kabinet.add(kab1,kab2,kab3,k4)

deliverywhy = types.InlineKeyboardMarkup(row_width=1)
sposob1 = types.InlineKeyboardButton(text = "Способы доставки", callback_data = "sposobdelivery")
sposob2 = types.InlineKeyboardButton(text = "Способы оплаты", callback_data = "sposobpay")
deliverywhy.add(sposob1,sposob2)

tovarkey = types.InlineKeyboardMarkup(row_width=1)
tovar1 = types.InlineKeyboardButton(text = "Поиск по категориям(Сейчас недоступно)", callback_data = "searchkat")
tovar2 = types.InlineKeyboardButton(text = "Поиск по названию", callback_data = "searchname")
tovarkey.add(tovar1,tovar2)

changeproduct = types.InlineKeyboardMarkup()
backproduct = types.InlineKeyboardButton(text = "⏪Назад⏪", callback_data = "backproduct")
changeproduct.add(backproduct)

ehehochy = types.InlineKeyboardMarkup()
hochy = types.InlineKeyboardButton(text="Да, скинь еще", callback_data="wont")
nehocy = types.InlineKeyboardButton(text="Нет, я нашел", callback_data="notwont")
ehehochy.add(hochy, nehocy)

stock = types.InlineKeyboardMarkup()
stockback = types.InlineKeyboardButton(text = "⏪Назад⏪", callback_data = "stockback")
stock.add(stockback)

changefrom = types.InlineKeyboardMarkup(row_width=1)
geomethod = types.InlineKeyboardButton(text="Да, я хочу изменить адрес", callback_data="sendgeo")
backgeo = types.InlineKeyboardButton(text="⏪Назад⏪", callback_data="stayn")
textmethod = types.InlineKeyboardButton(text="Указать самостоятельно", callback_data="sendtextgeo")
changefrom.add(geomethod,backgeo)

methodbda = types.InlineKeyboardMarkup(row_width=1)
methodlist = types.InlineKeyboardButton(text="Поиск всех участников бота", callback_data="checkdbalist")
methodlen = types.InlineKeyboardButton(text="Количество участников", callback_data="checkdbalen")
methodbda.add(methodlist, methodlen)

adminpanelkey = types.InlineKeyboardMarkup()
a1 = types.InlineKeyboardButton(text="⏪Назад⏪", callback_data = "aback")
a2 = types.InlineKeyboardButton(text="Отправить сообщение всем пользователям", callback_data = "sendmsga")
a3 = types.InlineKeyboardButton(text="Проверить базы данных", callback_data = "checkdba")
#a12 = types.InlineKeyboardButton(text="👨‍💻Наши контакты👩‍💻", callback_data= "blockcontact")
#a32 = types.InlineKeyboardButton(text="Наши отзывы👍", url = "https://primo.vip/testimonials")
#a4 = types.InlineKeyboardButton(text="⏪Назад⏪", callback_data="k4data")
adminpanelkey.row(a3)
adminpanelkey.row(a2)
adminpanelkey.row(a1)
#adminpanel.row(a12)
#adminpanel.row(a32)
#adminpanel.row(a4)

pcuserbackkatalog = types.InlineKeyboardMarkup(row_width=1)
psusergo = types.InlineKeyboardButton(text="Отправить свое местоположение", callback_data="sendgeo")
pcuserbackkatalog.add(psusergo, backgeo)
#Начало диалогов для neworder
order = types.InlineKeyboardMarkup(row_width=2)
butorder1 = types.InlineKeyboardButton(text="Да", callback_data="orderyes")
butorder2 = types.InlineKeyboardButton(text="Еще нет", callback_data="ordernot")
order.add(butorder1, butorder2)



@bot.message_handler(commands=['start'])
def start_previe(message):
    bot.send_message(message.chat.id,
        """
Я бот для интернет магазина PRIMO
С моей помощью ты с легкостю сможешь опредилиться с заказом🤙
Узнать о способах доставки🚚, графике работы🕖
И о прочих не менее интересных вещах👀
<b>Вас приветсвует обновление ALPHA-0.1.3</b>
В этом обновлении исправлена возможность отправлять несколько запросов на изменение данных,<i>ТЕПЕРЬ можно только один раз запросить и бот один раз ответит.</i>
Также правки со стороны администрации теперь не возможно получить доступ к админ панели если нет на то разрешения.
Пока к сожалению добавить нового администратора без обновления бота невозможно но вскоре это исправим!
Исправлена грубая ошибка с базой данных, спасибо Евгению за это!
<i>С уважением</i> <a href="https://t.me/TaksistYandeksa"> поддержка </a>ShopingBot🤖
        """, parse_mode = "HTML",  disable_web_page_preview = True, reply_markup = keyboard)
    sqlite3_create(message)
    sqlite3_createloc(message)

@bot.message_handler(commands=['setname'])
def whatyourname(message):
    wname = bot.send_message(message.chat.id,"Как мне тебя называть?")
    bot.register_next_step_handler(wname, checkname)

@bot.message_handler(commands=['admin'])
def checkadmin(message):
    Name_DB = 'DB_file.db'
    con = sqlite3.connect(Name_DB)
    c = con.cursor()
    query = 'SELECT "admin" FROM "core_fes" WHERE "id" = "{id}"'.format(id = str(message.chat.id))
    c.execute(query)
    dataa = c.fetchall()
    new_data = []
    for element in dataa:
        new_data.append(element[0])
    dataa = new_data
    con.commit()
    con.close()
    print(dataa)
    adimnpanel(message,dataa)
def adimnpanel(message,dataa):
    if dataa[0] == 1:
        bot.send_message(message.chat.id,"Добро пожаловать в Админ Панель!", reply_markup = adminpanelkey)
    elif dataa[0] != 1:
        pass

@bot.message_handler(commands=['neworder'])
def command_neworder(message):
    bot.send_message(message.chat.id,"О ты уже определился с заказом?", reply_markup = keyboard)

@bot.message_handler(commands=['fact'])
def factyread(message):
    random = randrange(100)
    with open("facty.txt",encoding='utf-8') as f:
        factylist = f.read().splitlines()
    bot.send_message(message.chat.id, text = factylist[random] , reply_markup = keyboard)

@bot.message_handler(commands=['katalog'])
def command_katalog(message):
    bot.send_message(message.chat.id,"В моем каталоге ты сможешь найти\nОчень класные ништяки🤓🤓🤓", reply_markup = katalogkey)

@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id,
        """
/start - Возращение в стартовую позицию
/help - Вывод всех доступных команд
/setname - Выбери имя как мне обращаться к тебе
/katalog - Каталог товаров
/neworder - Новый заказ(На данный момент не работает)
/statusorder - Выведет все твои заказы и их статус(На данный момент не работает)
/fact - Отправит тебе интересный факт
        """
        , reply_markup = keyboard)


def adminpanel_msg(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
        post = bot.send_message(message.chat.id,"Ты выбрал пункт отправить сообщение\nСледущие сообщение будет\nОтправлено всем пользователям\nНапиши 'Отмена' для отмены действия")
        bot.register_next_step_handler(post, sqliteadmin)

def topitems(message):
    bot.send_chat_action(message.chat.id, "typing")
    URL = "https://primo.vip"
    session = requests.session()
    request = session.get(URL)
    soup = BeautifulSoup(request.content, 'lxml')
    hrefs = []
    head = soup.find('div', class_='b-content__body').find_all('a', class_="b-product-line__product-name-link")
    for i in head:
        link = "https://primo.vip" + i.get('href')
        hrefs.append(link)
    result = []
    for l in range(3):
        bot.send_chat_action(message.chat.id, "typing")
        idx = list(set(hrefs[:]))
        for x in range (0, 18):
                num = random.randint(0, 18)
                while num in result:
                    num = random.randint(0, 18)
        result.append(num)
        url = idx[num]
        session1 = requests.session()
        request1 = session1.get(url)
        soup1 = BeautifulSoup(request1.content, 'lxml')
        head1 = soup1.find('a', class_="b-button-colored b-button-colored_type_do-order js-product-buy-button b-button-colored_loc_product")
        try:
            titlename  = head1.get('data-product-name')
            hrefjpg = head1.get('data-product-big-picture')
            price = head1.get('data-product-price')
            bot.send_photo(message.chat.id, photo = hrefjpg, caption =
            """
<b>{tn}</b>
<b>{pr}</b>
<a href="{url}">Полная версия</a>
            """.format(tn=titlename,pr=price,url=url), parse_mode = "HTML")
        except:
            pass
def searchitems(message, href):
    namefile = "{m}.txt".format(m=message.chat.id)
    num = 0
    for l in range(5):
        bot.send_chat_action(message.chat.id, "typing")
        if href != []:
            url = href[num]
            session1 = requests.session()
            request1 = session1.get(url)
            if request1.status_code == 200:
                soup1 = BeautifulSoup(request1.content, 'lxml')
                head1 = soup1.find('a', class_="b-button-colored b-button-colored_type_do-order js-product-buy-button b-button-colored_loc_product")
                try:
                    titlename  = head1.get('data-product-name')
                    hrefjpg = head1.get('data-product-big-picture')
                    price = head1.get('data-product-price')
                except:
                    bot.send_message(message.chat.id,
                    """
Извините произошла ошибка, буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                    """, parse_mode = "HTML", disable_web_page_preview = True)
                    try:
                        os.remove(namefile)
                    except:
                        pass
                bot.send_photo(message.chat.id, photo = hrefjpg, caption =
                    """
<b>{tn}</b>
<b>{pr}</b>
<a href="{url}">Полная версия</a>
                    """.format(tn=titlename,pr=price,url=url), parse_mode = "HTML")
                try:
                    os.remove(namefile)
                except:
                    pass
                num = num + 1
            elif request1.status_code is not 200:
                bot.send_message(message.chat.id,
                """
Извините произошла ошибка, буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                """, parse_mode = "HTML", disable_web_page_preview = True)
                try:
                    os.remove(namefile)
                except:
                    pass
                break
        elif href == []:
            bot.send_message(message.chat.id,
                """
Некоректный запрос, попробуй еще раз
                """, parse_mode = "HTML")
            try:
                os.remove(namefile)
            except:
                pass
            break
#     try:
#         print(request1.status_code)
#         bot.send_message(message.chat.id,
#                     """
# Хочете еще?
#                     """, reply_markup = ehehochy)
#     except:
#         pass
def returnsearchname(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
        post = bot.send_message(message.chat.id,"Отправь мне свой запрос в сообщении", reply_markup = keyboard)
        bot.register_next_step_handler(post, searchhref)
def searchhref(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    bot.send_chat_action(message.chat.id, "typing")
    requesttext = message.text
    post = "https://primo.vip/site_search?search_term=" + requesttext
    session = requests.session()
    request = session.get(post)
    href = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')
        p = soup.find_all('div', attrs={'class': 'b-product-line__details-panel'})
        for sp in p:
            p2 = sp.find('a', class_="b-product-line__product-name-link")
            result_href = p2.get("href")
            href.append(result_href)
        searchitems(message, href)
        try:
            os.remove(namefile)
        except:
            pass
    elif request.status_code == 500:
        bot.send_message(message.chat.id,
            """
Некоректный запрос, попробуй еще раз
            """, parse_mode = "HTML")
        try:
            os.remove(namefile)
        except:
            pass
    elif request.status_code is not 200:
                bot.send_message(message.chat.id,
                """
Извините произошла ошибка(342), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                """, parse_mode = "HTML", disable_web_page_preview = True)
                try:
                    os.remove(namefile)
                except:
                    pass

def whatyourphone(message):
    wphone = bot.send_message(message.chat.id,"Отправь мне свой номер телефона", reply_markup = keyboardphone)
    bot.register_next_step_handler(wphone, checkphone)
def returnphone(message):
    post = bot.send_message(message.chat.id,"Пожалуйста отправь мне свой номер телефона", reply_markup = keyboardphone)
    bot.register_next_step_handler(post, checkphone)
def checkphone(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    bot.send_chat_action(message.chat.id, "typing")
    if message.contact is not None:
        sqlite3_update(message)
        bot.send_message(message.chat.id,"Отлично! Все прошло успешно!")
        time.sleep(0.5)
        bot.send_message(message.chat.id,"Возращаю на главное меню...", reply_markup = keyboard)
        time.sleep(0.3)
        bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
        try:
            os.remove(namefile)
        except:
            pass
    elif message.contact is None:
        bot.send_message(message.chat.id, "Контакт не найден.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Произвожу отключение от базы данных..")
        time.sleep(0.3)
        bot.send_message(message.chat.id,"Возращаю на главное меню...", reply_markup = keyboard)
        time.sleep(0.7)
        bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
        try:
            os.remove(namefile)
        except:
            pass
    else:
        try:
            os.remove(namefile)
        except:
            pass
        bot.send_message(message.chat.id,
            """
Извините произошла ошибка(33), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
            """, parse_mode = "HTML", disable_web_page_preview = True)

def checkname(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    name = str(message.text)
    if name.isalpha():
        bot.send_message(message.chat.id,"Выполняю запись...")
        try:
            sqlite3_updateUName(message, name)
            bot.send_message(message.chat.id,"Отлично, все записал!")
            try:
                os.remove(namefile)
            except:
                pass
        except:
            bot.send_message(message.chat.id,
            """
Извините произошла ошибка(37), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
            """, parse_mode = "HTML", disable_web_page_preview = True)
            try:
                os.remove(namefile)
            except:
                pass
    elif message.text == "":
        bot.send_message(message.chat.id,
            """
Извините произошла ошибка(37-0), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
            """, parse_mode = "HTML")
        try:
            os.remove(namefile)
        except:
            pass
        bot.send_message(message.chat.id,"Возращаю на главное меню...")
        time.sleep(0.7)
        bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
    else:
        bot.send_message(message.chat.id,"Пожалуйста укажи настоящие имя(/setname)")
        try:
            os.remove(namefile)
        except:
            pass

def whatyourST(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    try:
        f = open(namefile)
        t = f.read
        if t == 1:
            pass
    except:
        f = open(namefile, 'w')
        f.write("1")
        wphone = bot.send_message(message.chat.id,
            """
<b>Отправь мне свое местоположение и я запомню его как твой дом👇👇👇</b>
            """, parse_mode = "HTML", disable_web_page_preview = True, reply_markup = keyST)#, reply_markup = pcuserbackkatalog
    bot.register_next_step_handler(wphone, checkST)
def checkST(message):
    namefile = "{m}.txt".format(m=message.chat.id)
    if message.location is not None:
        try:
            bot.send_chat_action(message.chat.id, "typing")
            stlong = str(message.location.longitude)
            stlati = str(message.location.latitude)
            bot.send_message(message.chat.id,"Выполняю запись...")
            sqlite3_updateST(message, stlong, stlati)
            bot.send_message(message.chat.id,"Отлично, все записал!")
            time.sleep(0.3)
            bot.send_message(message.chat.id,"Возращаю на главное меню...", reply_markup = keyboard)
            time.sleep(0.6)
            bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
            try:
                os.remove(namefile)
            except:
                pass
        except:
            bot.send_message(message.chat.id,
                """
    Извините произошла ошибка(32), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                """, parse_mode = "HTML", disable_web_page_preview = True)
            try:
                os.remove(namefile)
            except:
                pass
    elif message.location is None:
        bot.send_message(message.chat.id, "Местоположение не найдено.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Произвожу отключение от базы данных..")
        time.sleep(0.3)
        bot.send_message(message.chat.id,"Возращаю на главное меню...", reply_markup = keyboard)
        time.sleep(0.7)
        bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
        try:
            try:
                os.remove(namefile)
            except:
                pass
        except:
            pass
    else:
        bot.send_message(message.chat.id,
                """
    Извините произошла ошибка(32-0), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                """, parse_mode = "HTML", disable_web_page_preview = True)
        try:
            os.remove(namefile)
        except:
            pass

user_dict = {}


class User:
    def __init__(self, chat_id):
        self.id = chat_id
        self.city = None
        self.street = None
        self.numh = None

def whatyourSTintext(message):
    msg = bot.send_message(message.chat.id,
"""
Формат ответа(Город-Улица-Дом)
В каком городе ты проживаешь?
""")
    bot.register_next_step_handler(msg, checkSTcity)


def checkSTcity(message):
    if message.text.isalpha():
        try:
            chat_id = message.chat.id
            city = message.text
            user = User(chat_id)
            user.city = city
            user_dict[chat_id] = user
            msg = bot.send_message(message.chat.id, 'На какой улице ты живешь?')
            bot.register_next_step_handler(msg, checkSTstreet)
        except:
            bot.send_message(message.chat.id,
                        """
            Извините произошла ошибка(38-0), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                        """, parse_mode = "HTML", disable_web_page_preview = True)
    else:
        bot.send_message(message.chat.id, 'Попробуй без цифр =)')

def checkSTstreet(message):
    if message.text.isalpha():
        try:
            chat_id = message.chat.id
            street = message.text
            user = user_dict[chat_id]
            user.street = street
            msg = bot.send_message(message.chat.id, 'И последнее, какой у тебя номер дома?')
            bot.register_next_step_handler(msg, checkSTnumh)
        except:
            bot.send_message(message.chat.id,
                        """
            Извините произошла ошибка(38-0), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                        """, parse_mode = "HTML", disable_web_page_preview = True)
    else:
        bot.send_message(message.chat.id, 'Попробуй без цифр =)')

def checkSTnumh(message):
    # try:
        chat_id = message.chat.id
        numh = message.text
        user = user_dict[chat_id]
        user.numh = numh
        city = user.city
        street = user.street
        bot.send_message(message.chat.id, 'Выполняю запись...')
        sqlite3_updateSTintext(message, city, street, numh)
        bot.send_message(message.chat.id,"Отлично! Все прошло успешно!")
        time.sleep(0.5)
        bot.send_message(message.chat.id,"Возращаю на главное меню...", reply_markup = keyboard)
        time.sleep(0.3)
        bot.send_message(message.chat.id,"Главное меню🏢", reply_markup = key)
        #bot.send_message(chat_id, 'Nice to meet you ' + user.city + '\n Age:' + str(user.street) + '\n Sex:' + user.numh)

    # except:
        # bot.send_message(message.chat.id,
                    # """
        # Извините произошла ошибка(38-0), буду признаетелен если сообщишь моему <a href="https://t.me/TaksistYandeksa">создателю</a>
                    # """, parse_mode = "HTML", disable_web_page_preview = True)

@bot.message_handler(content_types=['sticker'])
def stickmsg(message):
    bot.send_sticker(message.chat.id, 'CAADAgADBgADr8ZRGp7O7vhbqf36FgQ')
#    print(message.sticker)


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def echo_digits(message):
    if message.text == "Главное меню🏢":
        sqlite3_create(message)
        bot.send_message(message.chat.id, "Это главное меню тут ты узнаешь о всех моих функциях\n", reply_markup=key)
        namefile = "{m}.txt".format(m=message.chat.id)
        try:
            os.remove(namefile)
        except:
            pass


@bot.callback_query_handler(func=lambda c:True) # Раздел со всеми .data перемнными
def inlin(c):
    if c.data == 'NumberTwo':
        help_info(c.message)
        bot.send_message(chat_id=c.message.chat.id,
            text="Для получения полного списка команд в любое время наберите (/help)",reply_markup = backkeyboardtomenu)
    if c.data == 'NumberTree':
        bot.send_message(chat_id=c.message.chat.id,
            text = 'Тут вы можете указать информацию о себе\nЧтобы боту было легче определить информацию для оформления', reply_markup = kabinet)
    if c.data == 'k4data':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
            text = 'Главное меню🏢', reply_markup = key)
    if c.data == 'aback':
        namefile = "{m}.txt".format(m=c.message.chat.id)
        try:
            os.remove(namefile)
        except:
            pass
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
            text = 'Главное меню🏢', reply_markup = key)
    if c.data == 'stockback':
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
           text = 'Каталог', reply_markup = katalogkey)
    if c.data == 'backproduct':
       bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
           text = 'Каталог', reply_markup = katalogkey)
    if c.data == 'phone':
        sqliteopenphone3(c.message)
    if c.data == 'changep':
        whatyourphone(c.message)
    if c.data == 'stayn':
        namefile = "{m}.txt".format(m=c.message.chat.id)
        bot.send_message(chat_id=c.message.chat.id,
           text = 'Ваш личный кабинет', reply_markup = kabinet)
        try:
            os.remove(namefile)
        except:
            pass
    if c.data == 'changen':
        whatyourname(c.message)
    if c.data == 'wont':
        searchhref(c.message)
    if c.data == 'first_name_kab':
        sqliteopen3(c.message)
    if c.data == 'topitems':
        topitems(c.message)
    if c.data == 'searchname':
        returnsearchname(c.message)
    if c.data == 'sendtextgeo':
        whatyourSTintext(c.message)
    if c.data == 'sendgeo':
        whatyourST(c.message)
    if c.data == 'sendmsga':
        adminpanel_msg(c.message)
    if c.data == 'checkdba':
        bot.send_message(chat_id=c.message.chat.id,
            text = 'Какой метод желаешь?', reply_markup = methodbda)
    if c.data == 'checkdbalist':
        sqliteadmindba(c.message)
    if c.data == 'checkdbalen':
        sqliteadmindba(c.message, typem = "lenlist")
    if c.data == 'blockcontact':
        bot.send_message(chat_id=c.message.chat.id,
           text =
           '''
Мы находимся по адресу:
<b>м.Запоріжжя, вул.Жуковського 32</b>
        ''', parse_mode = "HTML")
        bot.send_location(chat_id=c.message.chat.id,
           latitude = "47.812245", longitude = "35.190241")
        bot.send_message(chat_id=c.message.chat.id, text =
        """
<strong>Наши контакты</strong>
📱+380506675253 <b>- Отдел Продаж</b>
📱+380976675253 <b>- Отдел Продаж</b>
📱+380736675253 <b>- Отдел Продаж</b>
        """, parse_mode = "HTML")
        bot.send_message(chat_id=c.message.chat.id, text =
        """
<strong>График работы</strong>
Понедельник <b>09:30-19:00</b>
Вторник <b>09:30-19:00</b>
Среда <b>09:30-19:00</b>
Четверг <b>09:30-19:00</b>
Пятница <b>09:30-19:00</b>
Суббота <b>09:30-16:00</b>
Воскресенье <b>Выходной</b>
        """, parse_mode = "HTML")
    if c.data == 'delivery':
        bot.send_message(chat_id=c.message.chat.id,
            text = 'Что вас именно интересует?', reply_markup = deliverywhy)
    if c.data == 'taketovar':
        bot.send_message(chat_id=c.message.chat.id,
            text = 'Выбирите вариант ниже', reply_markup = tovarkey)
    if c.data == 'sposobdelivery':
        bot.send_message(chat_id=c.message.chat.id,
            text =
            """
<b>Нова Пошта🇺🇦>></b>
Возможна доставка наложенным платежом (доставку и услуги наложенного платежа оплачивает покупатель)
Бесплатная доставка от 300 грн (распространяется только на предварительно оплаченный товар)
            """, parse_mode = "HTML")
    if c.data == 'sposobpay':
        bot.send_message(chat_id=c.message.chat.id,
            text =
            """
<b>Наложенный платеж</b>
Это способ оплаты, при котором покупатель оплачивает товар и доставку посылки непосредственно при получении на отделении фирмы перевозчика
Данный способ оплаты доступен только для ТК "Нова Пошта"
<b>Online</b> >> оплата картой Visa, Mastercard
<b>Online</b> >> оплата картой любого банка
<b>Оплата на карту Приватбанка</b>
При выборе данного способа оплаты, после оформления заказа наш менеджер сообщит реквизиты карты Приватбанка для оплаты через терминал банковское отделение или интернет
При таком способе оплаты Вы экономите от 50 до 100% на доставке
Вы можете узнать больше <a href="https://primo.vip/delivery_info">тут</a>
            """, parse_mode = "HTML", disable_web_page_preview = True)
    if c.data == 'infobot':
        bot.send_message(chat_id=c.message.chat.id,
            text =
            """
<b>Если ты здесь значит тебе интересно кто я и зачем меня создали
Я </b> <a href="https://t.me/Testcrmlocal_bot">ShopingBot🤖</a> <b>Version - alfa 0.1.3
Моя цель помогать тебе с выбором товара в интернет-магазине primo.vip
И передавать твои данные на обработку
После чего с тобой в случаи подтверждения заказа свяжиться менеджер</b>
<i>Если возникли проблемы с использованием бота или
Идеи для модификации пишите на этот Telegram</i> <a href="https://t.me/TaksistYandeksa">аккаунт</a>
            """, parse_mode = "HTML", disable_web_page_preview = True)
    if c.data == 'from_kab':
        sqliteopenSTintextphone3(c.message)
        # whatyourST(c.message)
        # time.sleep(0.5)
        # bot.send_message(chat_id=c.message.chat.id,
        #     text = 'Возращаю на главное меню')
        # time.sleep(0.1)
        # bot.send_message(chat_id=c.message.chat.id,
        #    text = 'Главное меню🏢', reply_markup = key)
if __name__ == '__main__':
    bot.polling(none_stop=True)
#КОДЫ ОШИБОК
#37 ошибка записи имени в sqlite3_updateUName
#342 ошибка ответ respon is not 200 searchhref
#33 ошибка в checkphone
#37-0 пустое сообщение sqlite3_updateUName
#32 ошибка записи адреса в checkST
#32-0 Нет сообщения в checkST
#38 Ошибка записи в sqlite3_updateSTintext
#38-0 Отсутсвие текста в сообщении checkSTintext
#39 Ошибка с локацией