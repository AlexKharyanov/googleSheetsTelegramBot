from datetime import date
import telebot
import gspread
import logging
import re
from telebot import types
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = '5295995033:AAFuIYpH0jQxvi_MOj_g8NkJXFyQD0mRPFs'
googlesheet_id = '16s47gRbgz7XSuEpbnSXeeFpM_ojIJfxovtV4poy2fdg'
bot = telebot.TeleBot(token)
gc = gspread.service_account()

today = date.today().strftime("%d.%m.%Y")
dataPerem = ''
adresPerem = ''
tehPerem = ''
kolChasovPerem = ''
imyaPerem = ''
kolFactPerem = ''
procheePerem = ''

# приветствуем пользователя и говорим что умеем..
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	keyboards = telebot.types.ReplyKeyboardMarkup(True)
	keyboards.row('ВНЕСТИ ДАННЫЕ')
	bot.reply_to(message, f"Привет, я буду записивать ваши данные. Для начала работы нажмите ВНЕСТИ ДАННЫЕ", reply_markup=keyboards)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	if message.text == 'ВНЕСТИ ДАННЫЕ':
		# bot.send_message(message.from_user.id, "Введите адрес работы:")
		bot.send_message(message.from_user.id, "Введите дату ( дд.мм.гггг):")
		bot.register_next_step_handler(message, dats)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	global tehPerem
	if call.message.text == 'ВНЕСТИ ДАННЫЕ':
		bot.send_message(message.from_user.id, "Введите дату ( дд.мм.гггг):")
		bot.register_next_step_handler(call.message, dats);
	elif call.data == 'jcb8035':
		tehPerem = 'Мини-экскаватор jcb8035'
		bot.send_message(call.message.chat.id, text=f"Введите кол-во отработанных часов по рапорту или количество рейсов или объем м3:", parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, kolChasov)
	elif call.data == 'к322хс198':
		# global teh
		tehPerem = 'Измельчитель forst-st8 к322хс198'
		bot.send_message(call.message.chat.id, text=f"Введите кол-во отработанных часов по рапорту или количество рейсов или объем м3:", parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, kolChasov)
	elif call.data == 'к600хс198':
		# global teh
		tehPerem = 'Измельчитель forst-st8 к600хс198'
		bot.send_message(call.message.chat.id, text=f"Введите кол-во отработанных часов по рапорту или количество рейсов или объем м3:", parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, kolChasov)
	elif call.data == 'м226кс198':
		# global teh;
		tehPerem = 'Лесовоз с кму м226кс198'
		bot.send_message(call.message.chat.id, text=f"Введите кол-во отработанных часов по рапорту или количество рейсов или объем м3:", parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, kolChasov)
	elif call.data == 'Другое':
		# global teh;
		tehPerem = 'Другое'
		bot.send_message(call.message.chat.id, text=f"Введите кол-во отработанных часов по рапорту или количество рейсов или объем м3:", parse_mode= 'HTML')
		bot.register_next_step_handler(call.message, kolChasov)
def dats(message):
	global dataPerem
	dataPerem = message.text
	bot.send_message(message.chat.id, text=f"Введите адрес работы:", parse_mode= 'HTML')
	bot.register_next_step_handler(message, adres)
def adres(message):
	global adresPerem
	adresPerem = str(message.text)
	catalog = telebot.types.InlineKeyboardMarkup()
	catalog.add(telebot.types.InlineKeyboardButton(text='Мини-экскаватор jcb8035', callback_data='jcb8035'))
	catalog.add(telebot.types.InlineKeyboardButton(text='Измельчитель forst-st8 к322хс198', callback_data='к322хс198'))
	catalog.add(telebot.types.InlineKeyboardButton(text='Измельчитель forst-st8 к600хс198', callback_data='к600хс198'))
	catalog.add(telebot.types.InlineKeyboardButton(text='Лесовоз с кму м226кс198', callback_data='м226кс198'))
	catalog.add(telebot.types.InlineKeyboardButton(text='Другое', callback_data='Другое'))
	bot.send_message(message.chat.id, text=f"Выберите вид техники:", reply_markup=catalog, parse_mode= 'HTML')

def kolChasov(message):
	global kolChasovPerem
	kolChasovPerem = message.text
	bot.send_message(message.chat.id, text=f"Введите ваше имя и фамилию:", parse_mode= 'HTML')
	bot.register_next_step_handler(message, imya)

def imya(message):
	global imyaPerem
	imyaPerem = message.text
	bot.send_message(message.chat.id, text=f"Введите кол-во отработанных часов по факту или другое (если оплата по сменно то ставим 1):", parse_mode= 'HTML')
	bot.register_next_step_handler(message, prochee)

def prochee(message):
	global kolFactPerem
	kolFactPerem = message.text
	bot.send_message(message.chat.id, text=f"Введите дополнительную информацию (если хотите оставить поле пустым поставьте прочерк):", parse_mode= 'HTML')
	bot.register_next_step_handler(message, succes)


def succes(message):
	global procheePerem
	procheePerem = message.text
	sh = gc.open_by_key(googlesheet_id)
	sh.sheet1.append_row([dataPerem, adresPerem, tehPerem, kolChasovPerem, imyaPerem, kolFactPerem, procheePerem ])
	bot.send_message(message.chat.id, text=f"Данные успешно внесены. Чтобы снова внести данные нажмите кнопку ВНЕСТИ ДАННЫЕ", parse_mode= 'HTML')


def main(use_logging, level_name):
    if use_logging:
        telebot.logger.setLevel(logging.getLevelName(level_name))
    bot.polling(none_stop=True, interval=.5)
if __name__ == '__main__':
    main(True, 'DEBUG')