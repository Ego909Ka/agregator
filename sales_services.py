import telebot
import requests
import traceback
import time
import random
from section.keyboard import *
from section.db import execute
from config import token_bot, login_garant, login_bot, msg_rules, msg_help, qiwi_number, qiwi_token, admins_id, number_categories, percent, min_withdraw, summ_rez, summ_zak

bot = telebot.TeleBot(token_bot, threaded=True);

def add_moder(m):
	message = m.text
	user_id = m.from_user.id
	unix = int(time.time())
	try:
		name = execute('SELECT user_name FROM users WHERE user_id=%s', int(message))[0][0]
		execute('INSERT INTO moderators VALUES (%s, %s, %s)', [message, name, unix])
		bot.send_message(user_id, '✅ Модератор успешно добавлен')
	except:
		bot.send_message(user_id, '❌ Неудалось добавить модератора')

def add_subcategory(m, typee):
	try:
		message = m.text.split()
		user_id = m.from_user.id
		subcategories_table = random.randint(111111, 999999)
		if typee == 1:
			execute('INSERT INTO sale_advertising_channel VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  conditions VARCHAR(256) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		elif typee == 2:
			execute('INSERT INTO sale_advertising_bot VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  conditions VARCHAR(256) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		elif typee == 3:
			execute('INSERT INTO sale_advertising_chat VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  conditions VARCHAR(256) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		elif typee == 4:
			execute('INSERT INTO sale_channel VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  earnings DECIMAL(11,2) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		elif typee == 5:
			execute('INSERT INTO sale_bot VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  earnings DECIMAL(11,2) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		elif typee == 6:
			execute('INSERT INTO sale_chat VALUES (%s, %s, %s)', [message[0], subcategories_table, message[1]])
			execute('CREATE TABLE sell_channel.%s (user_id BIGINT NOT NULL,  user_name VARCHAR(64) NOT NULL,  name VARCHAR(64) NOT NULL,  earnings DECIMAL(11,2) NOT NULL,  summ DECIMAL(11,2) NOT NULL, participants_count BIGINT NOT NULL, time BIGINT NOT NULL, type INT NOT NULL) ENGINE = InnoDB;', subcategories_table)
		bot.send_message(user_id, '✅ Подкатегория успешно создана')
	except:
		bot.send_message(user_id, '❌ Ошибка при создании подкатегории')

def add_proposal(user_id, table, typee):
	markup = types.InlineKeyboardMarkup(row_width=1)
	if (typee == '1') or (typee == '2') or (typee == '3'):
		if typee == '1':
			cost = execute('SELECT price FROM sale_advertising_channel WHERE subcategories_table=%s', table)[0][0]
		elif typee == '2':
			cost = execute('SELECT price FROM sale_advertising_bot WHERE subcategories_table=%s', table)[0][0]
		elif typee == '3':
			cost = execute('SELECT price FROM sale_advertising_chat WHERE subcategories_table=%s', table)[0][0]
		try:
			execute('INSERT INTO temporary_addition_1 VALUES (%s, %s, %s, %s, 0, 0)', [user_id, '0', str(0), str(0)])
			name = '0'
			conditions = '0'
			summ = 0
			users = 0
		except:
			info = execute('SELECT name, conditions, summ, users FROM temporary_addition_1 WHERE user_id=%s', user_id)[0]
			name = info[0]
			conditions = info[1]
			summ = info[2]
			users = info[3]
		if name == '0':
			name = 'Не установлено'
		if conditions == '0':
			conditions='Не установлено'
		if summ == 0:
			summ == '0.00'
		markup.add(types.InlineKeyboardButton(text='Установить название', callback_data='select_name_1'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить условия', callback_data='select_conditions_1'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить сумму', callback_data='select_summ_1'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить кол-во юзеров', callback_data='select_users_1'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Отправить объявление на модерацию', callback_data='add_obv'+':'+str(table)+':'+str(typee)))
		bot.send_message(user_id, 
			'*Название канала:* `'+name+'`\n'+
			'*Условия:* `'+conditions+'`\n'+
			'*Сумма услуги:* `'+str(summ)+'₽`\n'+
			'*Кол-во юзеров:* `'+str(users)+'`\n\n'+
			'*Стоимость размещения объявления:* `'+str(cost)+'₽`'
		, reply_markup=markup, parse_mode='MarkDown')

	elif (typee == '4') or (typee == '5') or (typee == '6'):
		if typee == '4':
			cost = execute('SELECT price FROM sale_channel WHERE subcategories_table=%s', table)[0][0]
		elif typee == '5':
			cost = execute('SELECT price FROM sale_bot WHERE subcategories_table=%s', table)[0][0]
		elif typee == '6':
			cost = execute('SELECT price FROM sale_chat WHERE subcategories_table=%s', table)[0][0]
		try:
			execute('INSERT INTO temporary_addition_2 VALUES (%s, %s, 0, 0, 0)', [user_id, '0'])
			name = '0'
			users = 0
			doxod = 0
			summ = 0
		except:
			info = execute('SELECT name, users, doxod, summ FROM temporary_addition_2 WHERE user_id=%s', user_id)[0]
			name = info[0]
			users = info[1]
			doxod = info[2]
			summ = info[3]
		if name == '0':
			name = 'Не указано'
		if users == 0:
			users = 'Не указано'
		if doxod == 0:
			doxod = '0.00'
		if summ == 0:
			summ = '0.00'
		markup.add(types.InlineKeyboardButton(text='Установить название', callback_data='select_name_2'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить кол-во юзеров', callback_data='select_users_2'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить сумму дохода', callback_data='select_doxod_2'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Установить стоимость', callback_data='select_summ_2'+':'+str(table)+':'+str(typee)))
		markup.add(types.InlineKeyboardButton(text='Отправить объявление на модерацию', callback_data='add_obv'+':'+str(table)+':'+str(typee)))
		bot.send_message(user_id,
			'*Название канала:* `'+name+'`\n'+
			'*Юзеров:* `'+str(users)+'`\n'+
			'*Доход в месяц:* `'+str(doxod)+'₽`\n'+
			'*Стоимость:* `'+str(summ)+'₽`\n\n'+
			'*Стоимость размещения объявления:* `'+str(cost)+'₽`'
		, reply_markup=markup, parse_mode='MarkDown')

def select_name_1(m, table, typee):
	try:
		execute('UPDATE temporary_addition_1 SET name=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_conditions_1(m, table, typee):
	try:
		execute('UPDATE temporary_addition_1 SET conditions=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_summ_1(m, table, typee):
	try:
		execute('UPDATE temporary_addition_1 SET summ=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_users_1(m, table, typee):
	try:
		execute('UPDATE temporary_addition_1 SET users=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_name_2(m, table, typee):
	try:
		execute('UPDATE temporary_addition_2 SET name=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_users_2(m, table, typee):
	try:
		execute('UPDATE temporary_addition_2 SET users=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_doxod_2(m, table, typee):
	try:
		execute('UPDATE temporary_addition_2 SET doxod=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def select_summ_2(m, table, typee):
	try:
		execute('UPDATE temporary_addition_2 SET summ=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	add_proposal(m.from_user.id, table, typee)

def submit_ad_rab(user_id):
	try:
		execute('INSERT INTO offers_time (user_id) VALUES (%s)', user_id)
		zagol = '0'
		opis = '0'
	except:
		info = execute('SELECT zagol, opis FROM offers_time WHERE user_id=%s', user_id)[0]
		zagol = info[0]
		opis = info[1]

	if zagol == '0':
		zagol = 'Не установлен'
	if opis == '0':
		opis = 'Не установлено'

	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(types.InlineKeyboardButton(text='Установить заголовок', callback_data='set_zagol'))
	markup.add(types.InlineKeyboardButton(text='Установить описание', callback_data='set_opis'))
	markup.add(types.InlineKeyboardButton(text='Подать резюме', callback_data='2submit_offer'))
	bot.send_message(user_id,
		'*Заголовок:* `'+zagol+'`\n'+
		'*Описание:* `'+opis+'`\n\n'+
		'*Стоимость подачи резюме:* `'+str(summ_rez)+'₽`'
	, parse_mode='MarkDown', reply_markup=markup)

def set_zagol_2(m):
	try:
		execute('UPDATE offers_time SET zagol=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	submit_ad_rab(m.from_user.id)

def set_zagol_3(m):
	try:
		execute('UPDATE orders_time SET zagol=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	submit_ad_zak(m.from_user.id)

def set_opis_2(m):
	try:
		execute('UPDATE offers_time SET opis=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	submit_ad_rab(m.from_user.id)

def set_opis_3(m):
	try:
		execute('UPDATE orders_time SET opis=%s WHERE user_id=%s', [m.text, m.from_user.id])
	except:
		pass
	submit_ad_zak(m.from_user.id)

def set_summ(m):
	try:
		execute('UPDATE orders_time SET summ=%s WHERE user_id=%s', [int(m.text), m.from_user.id])
	except:
		pass
	submit_ad_zak(m.from_user.id)

def submit_ad_zak(user_id):
	try:
		execute('INSERT INTO orders_time (user_id) VALUES (%s)', int(user_id))
		zagol = '0'
		opis = '0'
		summ = 0
	except:
		info = execute('SELECT zagol, opis, summ FROM orders_time WHERE user_id=%s', user_id)[0]
		zagol = info[0]
		opis = info[1]
		summ = info[2]

	if zagol == '0':
		zagol = 'Не установлен'
	if opis == '0':
		opis = 'Не установлено'
	if int(summ) == 0:
		summ = '0.00'

	markup = types.InlineKeyboardMarkup(row_width=1)
	markup.add(types.InlineKeyboardButton(text='Установить заголовок', callback_data='set_zagol_3'))
	markup.add(types.InlineKeyboardButton(text='Установить описание', callback_data='set_opis_3'))
	markup.add(types.InlineKeyboardButton(text='Установить сумму', callback_data='set_summ'))
	markup.add(types.InlineKeyboardButton(text='Подать заказ', callback_data='3submit_offer'))
	bot.send_message(user_id,
		'*Заголовок:* `'+str(zagol)+'`\n'+
		'*Описание:* `'+str(opis)+'`\n'+
		'*Сумма:* `'+str(summ)+'₽`\n\n'+
		'*Стоимость подачи заказа:* `'+str(summ_zak)+'₽`'
	, parse_mode='MarkDown', reply_markup=markup)

def set_balance(m):
	try:
		message = m.text.split()
		execute('UPDATE users SET balance=%s WHERE user_id=%s', [int(message[0]), message[1]])
		bot.send_message(m.from_user.id, 'Баланс успешно установлен')
	except:
		bot.send_message(m.from_user.id, 'Ошибка при установке баланса')

def add_promo(m):
	try:
		ms = m.text.split()
		execute('INSERT INTO promo VALUES (%s, %s, %s)', [ms[0], ms[1], ms[2]])
		bot.send_message(m.from_user.id, 'Промокод успешно добавлен')
	except:
		bot.send_message(m.from_user.id, 'Ошибка')

def act_promo(m):
	try:
		info = execute('SELECT isp, summ FROM promo WHERE promo=%s', m.text)
		info_2 = execute('SELECT * FROM promo_isp WHERE user_id=%s', m.from_user.id)
		if info != [] and info[0][0] != 0 and info_2 == []:
			execute('UPDATE promo SET isp=isp-1 WHERE promo=%s', m.text)
			execute('INSERT INTO promo_isp VALUES (%s, %s, %s)', [m.from_user.id, m.text, 1])
			execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [info[0][1], m.from_user.id])
			bot.send_message(m.from_user.id, 'Вы успешно активировали промокод и получили '+str(info[0][1])+'₽')
		else:
			bot.send_message(m.from_user.id, 'Такого промокода нет')
	except:
		pass

def bringout(m):
	mes = m.text.split(':')
	info = execute('SELECT balance FROM users WHERE user_id=%s', m.from_user.id)[0][0]
	try:
		if info < int(mes[0]):
			bot.send_message(m.from_user.id, 'У вас недостаточно средст для вывода такой суммы')
		else:
			execute('UPDATE users SET balance=balance-%s WHERE user_id=%s', [int(mes[0]), m.from_user.id])
			execute('INSERT INTO bringout (user_id, summ, req) VALUES (%s, %s, %s)', [m.from_user.id, mes[0], mes[1]])
			bot.send_message(m.from_user.id, 'Заявка на вывод успешно создана')
	except:
		bot.send_message(m.from_user.id, 'Ошибка')

def mailing(m):
	if m.text == '-':
		bot.send_message(m.from_user.id, 'Рассылка успешно отменена')
		return
	else:
		info = execute('SELECT user_id FROM users')
		time_1 = time.time()
		for x in info:
			try:
				bot.send_message(x[0], m.text)
			except:
				pass
			time.sleep(0.1)
		time_2 = time.time()
		time_3 = time_2 - time_1
		bot.send_message(m.from_user.id, 'Рассылка успешно выполнена за '+str(time_3)+' секунд')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	user_id = call.message.chat.id
	user_name = str(call.message.chat.username)
	message_id = call.message.message_id
	unxi = int(time.time())
	try:
		if call.message:
			if call.data == "rules":
				bot.send_message(user_id, msg_rules)

			elif call.data == "help":
				bot.send_message(user_id, msg_help)

			elif call.data == 'monetization':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Вы хотите вывести или пополнить баланс?:', reply_markup=monetization_keyboard())

			elif call.data == 'topup':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Через какую платежную систему вы хотите пополнить баланс?:', reply_markup=payment_keyboard())

			elif call.data == 'qiwi':
				bot.delete_message(user_id, message_id)
				nabor = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
				coment = ''
				for x in range(12):
					coment += random.choice(nabor)
				execute('INSERT INTO payments (user_id, type, coment) VALUES (%s, 1, %s)', [user_id, coment])
				bot.send_message(user_id, 'Нажмите на кнопку "Перевести", укажите нужную вам сумму и после удачного перевода нажмите кнопку "Проверить"', reply_markup=qiwi_keyboard(coment, qiwi_number))

			elif 'check_payment_qiwi' in call.data:
				coment = call.data.replace('check_payment_qiwi:', '')
				check_payment = requests.get('https://edge.qiwi.com/payment-history/v2/persons/'+qiwi_number+'/payments?rows=15&IN', headers={'Authorization': 'Bearer ' + qiwi_token},).json()
				check = execute('SELECT status FROM payments WHERE coment=%s', coment)[0][0]
				if check == 0:
					for x in check_payment['data']:
						if x['comment'] == coment:
							if x['sum']['currency'] == 643:
								pass
							bot.delete_message(user_id, message_id)
							execute('UPDATE payments SET status=1, summ=%s WHERE coment=%s', [x['sum']['amount'], coment])
							execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [x['sum']['amount'], user_id])
							bot.send_message(user_id, '✅ Ваш баланс успешно пополен на '+str(x['sum']['amount'])+'₽')
							return
					bot.answer_callback_query(callback_query_id=call.id, text='❌ Платеж не найден, попробуйте чуть позже!', show_alert=True)
				else:
					bot.send_message(user_id, '❌ За этот платеж баланс уже начислен!')

			elif call.data == 'add_moder':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите user id модератора:\n(Будующий модератор должен написать /start в боте)')
				bot.register_next_step_handler(call.message, add_moder)

			elif call.data == 'dell_moder':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT user_id, user_name FROM moderators')
				if info == []:
					bot.send_message(user_id, '❌Модераторов нет')
				else:
					markup = types.InlineKeyboardMarkup(row_width=1)
					for x in info:
						markup.add(types.InlineKeyboardButton(text=x[1]+' ('+str(x[0])+')', callback_data='ddel_moder:'+str(x[0])))
					bot.send_message(user_id, 'Выберите модератора которого нужно удалить:', reply_markup=markup)

			elif 'ddel_moder:' in call.data:
				bot.delete_message(user_id, message_id)
				moder = call.data.replace('ddel_moder:', '')
				try:
					execute('DELETE FROM moderators WHERE user_id=%s', moder)
					bot.send_message(user_id, '✅ Модератор успешно удален')
				except:
					 bot.send_message(user_id, '❌ Ошибка при удалении модератора')

			elif call.data == 'add_subcategory':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Куда нужно добавить подкатегорию?:', reply_markup=add_subcategories_keyboard())

			elif call.data == 'sale_advertising_channel':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 1))
			elif call.data == 'sale_advertising_bot':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 2))
			elif call.data == 'sale_advertising_chat':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 3))
			elif call.data == 'sale_channel':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 4))
			elif call.data == 'sale_bot':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 5))
			elif call.data == 'sale_chat':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите название подкатегории и сумму размещения через пробел:\nПример: Новости 100')
				bot.register_next_step_handler(call.message, lambda m: add_subcategory(m, 6))

			elif call.data == 'dell_subcategory':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'От куда нужно удалить подкатегорию?:', reply_markup=dell_subcategories_keyboard())

			elif call.data == 'dell_sale_advertising_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'1'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'dell_sale_advertising_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'2'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'dell_sale_advertising_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'3'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'dell_sale_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'5'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'dell_sale_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'6'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'dell_sale_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='del_table:'+str(x[1])+':'+'4'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif 'del_table:' in call.data:
				bot.delete_message(user_id, message_id)
				info = call.data.replace('del_table:', '').split(':')
				if info[1] == '1':
					execute('DELETE FROM sale_advertising_channel WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				elif info[1] == '3':
					execute('DELETE FROM sale_advertising_chat WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				elif info[1] == '2':
					execute('DELETE FROM sale_advertising_bot WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				elif info[1] == '4':
					execute('DELETE FROM sale_channel WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				elif info[1] == '6':
					execute('DELETE FROM sale_bot WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				elif info[1] == '5':
					execute('DELETE FROM sale_chat WHERE subcategories_table=%s', int(info[0]))
					execute('DROP TABLE `%s`', int(info[0]))
				bot.send_message(user_id, '✅ Подкатегория успешно удалена')

			elif call.data == 'buy_advertising_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'buy_advertising_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'buy_advertising_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'buy_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'buy_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'buy_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='show:'+str(x[1])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			
			elif call.data.startswith('show:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('show:', '')
				markup = types.InlineKeyboardMarkup(row_width=1)
				info_db = execute('SELECT participants_count, summ, user_id, time FROM `%s`' % int(info))
				for x in info_db:
					markup.add(types.InlineKeyboardButton(text=str(x[0])+' юзеров | Стоимость '+str(x[1]), callback_data='1obdshow:'+str(info)+':'+str(x[0])+':'+str(x[1])+':'+str(x[2])+':'+str(x[3])))
				bot.send_message(user_id, 'Выберите объявление:', reply_markup=markup)

			elif call.data.startswith('1obdshow'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('1obdshow:', '').split(':')
				info_db = execute('SELECT * FROM `'+str(info[0])+'` WHERE user_id=%s and participants_count=%s and summ=%s and time=%s', [info[3], info[1], info[2], info[4]])[0]
				markup = types.InlineKeyboardMarkup(row_width=1)
				markup.add(types.InlineKeyboardButton(text='Перейти', url='t.me/'+str(info_db[2]).replace('@', '').replace('http://t.me/', '').replace('https://t.me/', '')))
				url = ''
				bot_op = ''
				if (info_db[7] == 1) or (info_db[7] == 2) or (info_db[7] == 3):
					if info_db[7] == 2:
						bot_op = '\n\nВажно! Нет возможности проверить точное количество активных пользователей бота. Будьте внимательны!'
					if (info_db[5] > 1000) and (info_db[7] == 1):
						url = 'tgstat.ru/channel/'+info_db[2].replace('http://t.me/joinchat/', '').replace('https://t.me/joinchat/', '').replace('t.me/joinchat/', '')+'/widget.png'
						req = requests.get('https://'+url).status_code
						if req != 200:
							url = ''
						else:
							url = '\n\n'+url.replace('_', '\\_')
					bot.send_message(user_id,
						'🔥 `'+str(info_db[2])+'` 🔥\n\n'+
						'Условия: '+str(info_db[3])+'\n\n'+
						'Цена: '+str(info_db[4])+'₽\n\n'+
						'Услуги гаранта за 5% от суммы сделки: '+login_garant+bot_op+url
					, reply_markup=markup, parse_mode='MarkDown')

				elif (info_db[7] == 4) or (info_db[7] == 5) or (info_db[7] == 6):
					if info_db[7] == 5:
						bot_op = '\n\nВажно! Нет возможности проверить точное количество активных пользователей бота. Будьте внимательны!'
					if (info_db[5] > 1000) and (info_db[7] == 4):
						url = 'tgstat.ru/channel/'+info_db[2].replace('http://t.me/joinchat/', '').replace('https://t.me/joinchat/', '').replace('t.me/joinchat/', '')+'/widget.png'
						req = requests.get('https://'+url).status_code
						if req != 200:
							url = ''
						else:
							url = '\n\n'+url.replace('_', '\\_')
					bot.send_message(user_id,
						'🔥 `'+str(info_db[2])+'` 🔥\n\n'+
						'Примерный доход в месяц: '+str(info_db[3])+'₽\n\n'+
						'Цена: '+str(info_db[4])+'₽\n\n'+
						'Кол-во юзеров: '+str(info_db[5])+'\n\n'+
						'Услуги гаранта за 5% от суммы сделки: '+login_garant+bot_op+url
					, reply_markup=markup, parse_mode='MarkDown')

			elif call.data == 'salee_advertising_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':1'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'salee_advertising_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':2'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'salee_advertising_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_advertising_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':3'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'salee_chat':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_chat')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':6'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'salee_channel':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_channel')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':4'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)
			elif call.data == 'salee_bot':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT subcategories_name, subcategories_table FROM sale_bot')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='sale_show:'+str(x[1])+':5'))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data.startswith('sale_show:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('sale_show:', '').split(':')
				add_proposal(user_id, info[0], info[1])

			elif call.data.startswith('select_name_1'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_name_1:', '').split(':')
				if info[1] == '1':
					bot.send_message(user_id, 'Укажите логин канала:\n(Если это приватный канал, то ссылку на вступление)')
				elif info[1] == '2':
					bot.send_message(user_id, 'Укажите логин бота:')
				elif info[1] == '3':
					bot.send_message(user_id, 'Укажите логин чата:\n(Если это приватный чат, то ссылку на вступление)')
				bot.register_next_step_handler(call.message, lambda m: select_name_1(m, info[0], info[1]))

			elif call.data.startswith('select_conditions_1'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_conditions_1:', '').split(':')
				bot.send_message(user_id, 'Подробно опишите на каких условиях вы готовы работать:')
				bot.register_next_step_handler(call.message, lambda m: select_conditions_1(m, info[0], info[1]))

			elif call.data.startswith('select_summ_1'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_summ_1:', '').split(':')
				bot.send_message(user_id, 'Укажите сумму размещения рекламы в рублях:')
				bot.register_next_step_handler(call.message, lambda m: select_summ_1(m, info[0], info[1]))

			elif call.data.startswith('select_users_1'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_users_1:', '').split(':')
				bot.send_message(user_id, 'Укажите примерное кол-во пользователей:')
				bot.register_next_step_handler(call.message, lambda m: select_users_1(m, info[0], info[1]))

			elif call.data.startswith('select_name_2'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_name_2:', '').split(':')
				if info[1] == '4':
					bot.send_message(user_id, 'Укажите логин канала:\n(Если это приватный канал, то ссылку на вступление)')
				elif info[1] == '5':
					bot.send_message(user_id, 'Укажите логин бота:')
				elif info[1] == '6':
					bot.send_message(user_id, 'Укажите логин чата:\n(Если это приватный чат, то ссылку на вступление)')
				bot.register_next_step_handler(call.message, lambda m: select_name_2(m, info[0], info[1]))

			elif call.data.startswith('select_users_2'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_users_2:', '').split(':')
				bot.send_message(user_id, 'Укажите примерное кол-во пользователей:')
				bot.register_next_step_handler(call.message, lambda m: select_users_2(m, info[0], info[1]))

			elif call.data.startswith('select_doxod_2'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_doxod_2:', '').split(':')
				bot.send_message(user_id, 'Укажите примерную сумму заработка в месяц:')
				bot.register_next_step_handler(call.message, lambda m: select_doxod_2(m, info[0], info[1]))

			elif call.data.startswith('select_summ_2'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('select_summ_2:', '').split(':')
				bot.send_message(user_id, 'Укажите стоимость продажи:')
				bot.register_next_step_handler(call.message, lambda m: select_summ_2(m, info[0], info[1]))

			elif call.data.startswith('add_obv'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('add_obv:', '').split(':')
				info_user = execute('SELECT balance FROM users WHERE user_id=%s', user_id)[0][0]
				if info[1] == '1':
					info_obv = execute('SELECT price FROM sale_advertising_channel WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_1 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_1 WHERE user_id=%s', user_id)
				elif info[1] == '2':
					info_obv = execute('SELECT price FROM sale_advertising_bot WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_1 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_1 WHERE user_id=%s', user_id)
				elif info[1] == '3':
					info_obv = execute('SELECT price FROM sale_advertising_chat WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_1 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_1 WHERE user_id=%s', user_id)
				elif info[1] == '4':
					info_obv = execute('SELECT price FROM sale_channel WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_2 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_2 WHERE user_id=%s', user_id)
				elif info[1] == '5':
					info_obv = execute('SELECT price FROM sale_bot WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_2 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_2 WHERE user_id=%s', user_id)
				elif info[1] == '6':
					info_obv = execute('SELECT price FROM sale_chat WHERE subcategories_table=%s', info[0])[0][0]
					info_obv2 = execute('SELECT * FROM temporary_addition_2 WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM temporary_addition_2 WHERE user_id=%s', user_id)

				if info_user < info_obv:
					bot.send_message(user_id, 'У вас недостаточно средст для размещения рекламы. Нужно '+str(info_obv)+'₽, а у вас '+str(info_user)+'₽')
				else:

					if (info[1] == '1') or (info[1] == '2') or (info[1] == '3'):
						try:
							execute('INSERT INTO obd_moder VALUES (%s, %s, %s, %s, %s, %s, %s)', [user_id, info[0], info[1], info_obv2[2], info_obv2[3], info_obv2[4], info_obv2[5]])
							execute('UPDATE users SET balance=balance-%s WHERE user_id=%s', [int(info_obv), user_id])
							bot.send_message(user_id, 'Объявление успешно отправлено на модерацию')
						except:
							bot.send_message(user_id, 'Ваше предидущие объявление еще не проверили')
							return
					elif (info[1] == '4') or (info[1] == '5') or (info[1] == '6'):
						try:
							execute('INSERT INTO obd_moder_2 VALUES (%s, %s, %s, %s, %s, %s, %s)', [user_id, info[1], info[0], info_obv2[1], info_obv2[2], info_obv2[3], info_obv2[4]])
							execute('UPDATE users SET balance=balance-%s WHERE user_id=%s', [int(info_obv), user_id])
							bot.send_message(user_id, 'Объявление успешно отправлено на модерацию')
						except:
							bot.send_message(user_id, 'Ваше предидущие объявление еще не проверили')
							return

			elif call.data == 'info_obd_admin':
				bot.delete_message(user_id, message_id)
				info_1 = execute('SELECT * FROM obd_moder')
				info_2 = execute('SELECT * FROM obd_moder_2')
				info_3 = execute('SELECT * FROM orders WHERE status=0')
				info_4 = execute('SELECT * FROM offers WHERE status=0')
				markup = types.InlineKeyboardMarkup(row_width=1)
				if info_1 != []:
					for a in info_1:
						id_obd = random.randint(111111, 999999)
						markup.add(types.InlineKeyboardButton(text='Активные заявки c id '+str(id_obd), callback_data='obd_info:'+str(a[0])+':'+str(a[1])+':'+str(a[2])))
				if info_2 != []:
					for b in info_2:
						id_obd = random.randint(111111, 999999)
						markup.add(types.InlineKeyboardButton(text='Активные заявки c id '+str(id_obd), callback_data='obd_info:'+str(b[0])+':'+str(b[2])+':'+str(b[1])))
				if info_3 != []:
					for c in info_3:
						id_obd = random.randint(111111, 999999)
						markup.add(types.InlineKeyboardButton(text='Активные заявки c id '+str(id_obd), callback_data='check_order:'+str(c[0])+':'+str(c[1])+':'+str(c[2])+':'+str(c[3])))
				if info_4 != []:
					for d in info_4:
						id_obd = random.randint(111111, 999999)
						markup.add(types.InlineKeyboardButton(text='Активные заявки c id '+str(id_obd), callback_data='check_offers:'+str(d[0])+':'+str(d[1])+':'+str(d[2])))
				bot.send_message(user_id, 'Активные заявки:', reply_markup=markup)
	
			elif call.data.startswith('check_order'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('check_order:', '').split(':')
				markup = types.InlineKeyboardMarkup(row_width=2)
				markup.add(types.InlineKeyboardButton(text='Одобрить', callback_data='order_true'+':'+str(info[0])+':'+str(info[1])+':'+str(info[2])+':'+str(info[3])), types.InlineKeyboardButton(text='Отказать', callback_data='order_false'+':'+str(info[0])+':'+str(info[1])+':'+str(info[2])+':'+str(info[3])))
				bot.send_message(user_id,
					'*Тип объявления:* `создание заказа`\n'+
					'*Заголовок:* `'+str(info[1])+'`\n'+
					'*Описание:* `'+str(info[2])+'`\n'+
					'*Оплата:* `'+str(info[3])+'₽`'
				, reply_markup=markup, parse_mode='MarkDown')

			elif call.data.startswith('check_offers'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('check_offers:', '').split(':')
				markup = types.InlineKeyboardMarkup(row_width=1)
				markup.add(types.InlineKeyboardButton(text='Одобрить', callback_data='offers_true'+':'+str(info[0])+':'+str(info[1])+':'+str(info[2])), types.InlineKeyboardButton(text='Отказать', callback_data='offers_false'+':'+str(info[0])+':'+str(info[1])+':'+str(info[2])))
				bot.send_message(user_id,
					'*Тип объявления:* `создание резюме`\n'+
					'*Заголовок:* `'+str(info[1])+'`\n'+
					'*Описание:* `'+str(info[2])+'`'
				, reply_markup=markup, parse_mode='MarkDown')

			elif call.data.startswith('order_true:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('order_true:', '').split(':')
				try:
					bd_time = execute('SELECT count(*) FROM orders')[0][0]
					if bd_time >= 20:
						bd_time_2 = execute('SELECT min(time) FROM orders')[0][0]
						execute('DELETE FROM orders WHERE time=%s', bd_time_2)
					execute('UPDATE orders SET status=1 WHERE user_id=%s and zagol=%s and opis=%s and summ=%s', [info[0], info[1], info[2], info[3]])
					info_ref = execute('SELECT ref FROM users WHERE user_id=%s', info[0])[0][0]
					if info_ref != 0:
						execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [summ_zak / 100 * percent, info_ref])
						bot.send_message(info_ref, 'Вам было начислено '+str(ref_price / 100 * percent)+'₽ за вашего реферала')
					bot.send_message(user_id, 'Объявление успешно одобрено')
				except:
					traceback.print_exc()
					pass

			elif call.data.startswith('offers_true:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('offers_true:', '').split(':')
				try:
					bd_time = execute('SELECT count(*) FROM offers')[0][0]
					if bd_time >= 20:
						bd_time_2 = execute('SELECT min(time) FROM offers')[0][0]
						execute('DELETE FROM orders WHERE time=%s', bd_time_2)
					execute('UPDATE offers SET status=1 WHERE user_id=%s and zagol=%s and opis=%s', [info[0], info[1], info[2]])
					info_ref = execute('SELECT ref FROM users WHERE user_id=%s', info[0])[0][0]
					if info_ref != 0:
						execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [summ_rez / 100 * percent, info_ref])
						bot.send_message(info_ref, 'Вам было начислено '+str(ref_price / 100 * percent)+'₽ за вашего реферала')
					bot.send_message(user_id, 'Объявление успешно одобрено')
				except:
					traceback.print_exc()
					pass

			elif call.data.startswith('order_false'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('order_false:', '').split(':')
				try:
					execute('DELETE FROM orders WHERE user_id=%s and zagol=%s and opis=%s and summ=%s', [info[0], info[1], info[2], info[3]])
					execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [summ_zak, info[0]])
					bot.send_message(info[0], 'Вашу заявку на работу было отклонено, средства вернулись к вам на баланс!')
					bot.send_message(user_id, 'Объявление успешно отклонено')
				except:
					pass

			elif call.data.startswith('offers_false'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('offers_false:', '').split(':')
				try:
					execute('DELETE FROM offers WHERE user_id=%s and zagol=%s and opis=%s', [info[0], info[1], info[2]])
					execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [summ_rez, info[0]])
					bot.send_message(info[0], 'Ваше резюме было отклонено, средства вернулись к вам на баланс!')
					bot.send_message(user_id, 'Объявление успешно отклонено')
				except:
					pass

			elif call.data.startswith('obd_info'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('obd_info:', '').split(':')
				info_db_1 = 0
				info_db_2 = 0
				if (info[2] == '1') or (info[2] == '2') or (info[2] == '3'):
					info_db_1 = execute('SELECT * FROM obd_moder WHERE user_id=%s and tablee=%s and type=%s', [info[0], info[1], info[2]])[0]
				elif (info[2] == '4') or (info[2] == '5') or (info[2] == '6'):
					info_db_2 = execute('SELECT * FROM obd_moder_2 WHERE user_id=%s and tablee=%s and type=%s', [info[0], info[1], info[2]])[0]

				if info_db_1 != 0:
					if info_db_1[2] == 1:
						typee = 'Продажа рекламы в канале'
					elif info_db_1[2] == 3:
						typee = 'Продажа рекламы в чате'
					elif info_db_1[2] == 2:
						typee = 'Продажа рекламы в боте'

					bot.send_message(user_id, 
						'*Тип объявления:* `'+typee+'`\n'+
						'*Логин (Если ссылка, то значит чат или канал приватный):* '+str(info_db_1[3].replace('_', '\\_'))+'\n'+
						'*Условия рекламы:* `'+str(info_db_1[4])+'`\n'+
						'*Стоимость рекламы:* `'+str(info_db_1[5])+'`\n'+
						'*Кол-во юзеров:* `'+str(info_db_1[6])+'`'
					, reply_markup=obd_decision(info_db_1[0], info_db_1[1], info_db_1[2]), parse_mode='MarkDown')
				else:
					if info_db_2[1] == 4:
						typee = 'Продажа канала'
					elif info_db_2[1] == 6:
						typee = 'Продажа чата'
					elif info_db_2[1] == 5:
						typee = 'Продажа бота'
					bot.send_message(user_id, 
						'*Тип объявления:* `'+typee+'`\n'+
						'*Логин (Если ссылка, то значит чат или канал приватный):* '+str(info_db_2[3].replace('_', '\\_'))+'\n'+
						'*Кол-во юзеров:* `'+str(info_db_2[4])+'`\n'+
						'*Доход в месяц:* `'+str(info_db_2[5])+'`\n'+
						'*Стоимость:* `'+str(info_db_2[6])+'`'
					, reply_markup=obd_decision(info_db_2[0], info_db_2[2], info_db_2[1]), parse_mode='MarkDown')

			elif call.data.startswith('obd_good:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('obd_good:', '').split(':')
				info_db_1 = 0
				info_db_2 = 0

				if (info[2] == '1') or (info[2] == '2') or (info[2] == '3'):
					info_db_1 = execute('SELECT user_id, type, tablee, name, conditions, summ, users FROM obd_moder WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])
				elif (info[2] == '4') or (info[2] == '5') or (info[2] == '6'):
					info_db_2 = execute('SELECT user_id, type, tablee, name, users, doxod, summ FROM obd_moder_2 WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])

				if info_db_1 != 0:
					info_db_1 = info_db_1[0]
					execute('DELETE FROM obd_moder WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])
					bd_time = execute('SELECT count(*) FROM `'+str(info_db_1[2])+'`')[0][0]
					if bd_time >= 20:
						bd_time_2 = execute('SELECT min(time) FROM `'+str(info_db_1[2])+'`')[0][0]
						execute('DELETE FROM `'+str(info_db_1[2])+'` WHERE time=%s', bd_time_2)
					execute('INSERT INTO `'+str(info_db_1[2])+'` VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (info_db_1[0], '0', info_db_1[3], info_db_1[4], info_db_1[5], info_db_1[6], int(time.time()), info_db_1[1]))
					info_ref = execute('SELECT ref FROM users WHERE user_id=%s', info[0])[0][0]
					if info_ref != 0:
						if info[2] == '1':
							ref_price = execute('SELECT price FROM sale_advertising_channel WHERE subcategories_table=%s', info[1])[0][0]
						elif info[2] == '2':
							ref_price = execute('SELECT price FROM sale_advertising_bot WHERE subcategories_table=%s', info[1])[0][0]
						elif info[2] == '3':
							ref_price = execute('SELECT price FROM sale_advertising_chat WHERE subcategories_table=%s', info[1])[0][0]
						execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [ref_price / 100 * percent, info_ref])
						bot.send_message(info_ref, 'Вам было начислено '+str(ref_price / 100 * percent)+'₽ за вашего реферала')
				else:
					info_db_2 = info_db_2[0]
					execute('DELETE FROM obd_moder_2 WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])
					bd_time = execute('SELECT count(*) FROM `'+str(info_db_2[2])+'`')[0][0]
					if bd_time >= 20:
						bd_time_2 = execute('SELECT min(time) FROM `'+str(info_db_2[2])+'`')[0][0]
						execute('DELETE FROM `'+str(info_db_2[2])+'` WHERE time=%s', bd_time_2)
					execute('INSERT INTO `'+str(info_db_2[2])+'` VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', [info_db_2[0], '0', info_db_2[3], info_db_2[5], info_db_2[6], info_db_2[4], int(time.time()), info_db_2[1]])
					info_ref = execute('SELECT ref FROM users WHERE user_id=%s', info[0])[0][0]
					if info_ref != 0:
						if info[2] == '4':
							ref_price = execute('SELECT price FROM sale_channel WHERE subcategories_table=%s', info[1])[0][0]
						elif info[2] == '5':
							ref_price = execute('SELECT price FROM sale_bot WHERE subcategories_table=%s', info[1])[0][0]
						elif info[2] == '6':
							ref_price = execute('SELECT price FROM sale_chat WHERE subcategories_table=%s', info[1])[0][0]
						execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [ref_price / 100 * percent, info_ref])
						bot.send_message(info_ref, 'Вам было начислено '+str(ref_price / 100 * percent)+'₽ за вашего реферала')
				bot.send_message(user_id, 'Вы успешно одобрили заявку')

			elif call.data.startswith('obd_false:'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('obd_false:', '').split(':')
				if (info[2] == '1') or (info[2] == '2') or (info[2] == '3'):
					info_db_1 = execute('DELETE FROM obd_moder WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])
				elif (info[2] == '4') or (info[2] == '5') or (info[2] == '6'):
					info_db_2 = execute('DELETE FROM obd_moder_2 WHERE user_id=%s and type=%s and tablee=%s', [info[0], int(info[2]), info[1]])

				if info[2] == '1':
					summ = execute('SELECT price FROM sale_advertising_channel WHERE subcategories_table=%s', info[1])[0][0]
				elif info[2] == '2':
					summ = execute('SELECT price FROM sale_advertising_bot WHERE subcategories_table=%s', info[1])[0][0]
				elif info[2] == '3':
					summ = execute('SELECT price FROM sale_advertising_chat WHERE subcategories_table=%s', info[1])[0][0]
				elif info[2] == '4':
					summ = execute('SELECT price FROM sale_channel WHERE subcategories_table=%s', info[1])[0][0]
				elif info[2] == '5':
					summ = execute('SELECT price FROM sale_bot WHERE subcategories_table=%s', info[1])[0][0]
				elif info[2] == '6':
					summ = execute('SELECT price FROM sale_chat WHERE subcategories_table=%s', info[1])[0][0]

				execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [summ, int(info[0])])
				bot.send_message(user_id, 'Вы успешно отклонили объявление')
				bot.send_message(info[0], 'Ваше объявление было отклонено, средства были возвращены вам на баланс')

			elif call.data == 'rab_i':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Выберите действие:', reply_markup=rab_i())
			elif call.data == 'zak_i':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Выберите действие:', reply_markup=zak_i())

			elif call.data == 'submit_ad_rab':
				bot.delete_message(user_id, message_id)
				submit_ad_rab(user_id)

			elif call.data == 'set_zagol':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите заголовок, он будет отображатся в названии вашего резюме:')
				bot.register_next_step_handler(call.message, set_zagol_2)

			elif call.data == 'set_zagol_3':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите заголовок, он будет отображатся в названии вашего заказа:')
				bot.register_next_step_handler(call.message, set_zagol_3)

			elif call.data == 'set_opis':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите подробное описание, что вы умете:')
				bot.register_next_step_handler(call.message, set_opis_2)

			elif call.data == 'set_opis_3':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите подробное описание, что вы вам нужно:')
				bot.register_next_step_handler(call.message, set_opis_3)

			elif call.data == 'set_summ':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите сумму которую вы зплатите за задание:')
				bot.register_next_step_handler(call.message, set_summ)

			elif call.data == '2submit_offer':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT user_id FROM offers WHERE user_id=%s and status=0', user_id)
				if info != []:
					bot.send_message(user_id, 'Вы уже подавали заказ и его еще не проверили модераторы')
					return
				info_user = execute('SELECT balance FROM users WHERE user_id=%s', user_id)[0][0]
				if int(info_user) < summ_rez:
					bot.send_message(user_id, 'У вас недостаточно средств. У вас '+str(info_user)+'₽, а стоимость размещения стоить '+str(summ_rez)+'₽')
				else:
					execute('UPDATE users SET balance=balance-%s WHERE user_id=%s', [summ_rez, user_id])
					info = execute('SELECT zagol, opis FROM offers_time WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM offers_time WHERE user_id=%s', user_id)
					execute('INSERT INTO offers VALUES (%s, %s, %s, 0, %s)', [user_id, info[0], info[1], int(time.time())])
					bot.send_message(user_id, 'Вы успешно подали резюме, ожидайте одобрение модератора')

			elif call.data == '3submit_offer':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT user_id FROM orders WHERE user_id=%s and status=0', user_id)
				if info != []:
					bot.send_message(user_id, 'Вы уже подавали заказ и его еще не проверили модераторы')
					return
				info_user = execute('SELECT balance FROM users WHERE user_id=%s', user_id)[0][0]
				if int(info_user) < summ_zak:
					bot.send_message(user_id, 'У вас недостаточно средств. У вас '+str(info_user)+'₽, а стоимость размещения стоить '+str(summ_rez)+'₽')
				else:
					execute('UPDATE users SET balance=balance-%s WHERE user_id=%s', [summ_rez, user_id])
					info = execute('SELECT zagol, opis, summ FROM orders_time WHERE user_id=%s', user_id)[0]
					execute('DELETE FROM orders_time WHERE user_id=%s', user_id)
					execute('INSERT INTO orders VALUES (%s, %s, %s, %s, 0, %s)', [user_id, info[0], info[1], info[2], int(time.time())])
					bot.send_message(user_id, 'Вы успешно создали заказ, ожидайте одобрение модератора')

			elif call.data == 'resume':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT zagol FROM offers WHERE status=1')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='get_resum:'+str(x[0])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data == 'job_openings':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT zagol FROM orders WHERE status=1')
				markup = types.InlineKeyboardMarkup(row_width=1)
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0], callback_data='2get_resum:'+str(x[0])))
				bot.send_message(user_id, 'Выберите подкатегорию:', reply_markup=markup)

			elif call.data.startswith('get_resum'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('get_resum:', '')
				info_db = execute('SELECT user_id, opis FROM offers WHERE zagol=%s', info)[0]
				name = execute('SELECT user_name FROM users WHERE user_id=%s', int(info_db[0]))[0][0]
				markup = types.InlineKeyboardMarkup(row_width=1)
				markup.add(types.InlineKeyboardButton(text='Перейти в диалог', url='t.me/'+str(name).replace('@', '')))
				bot.send_message(user_id, 
					'💥 '+info+' 💥\n\n'+
					info_db[1]
				, reply_markup=markup)

			elif call.data.startswith('2get_resum'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('2get_resum:', '')
				info_db = execute('SELECT user_id, opis, summ FROM orders WHERE zagol=%s', info)[0]
				name = execute('SELECT user_name FROM users WHERE user_id=%s', int(info_db[0]))[0][0]
				markup = types.InlineKeyboardMarkup(row_width=1)
				markup.add(types.InlineKeyboardButton(text='Перейти в диалог', url='t.me/'+str(name).replace('@', '')))
				bot.send_message(user_id, 
					'💥 '+info+' 💥\n\n'+
					info_db[1]+'\n\n'+
					'Сумма заказа: '+str(info_db[2])+'₽'
				, reply_markup=markup)

			elif call.data == 'submit_ad_zak':
				bot.delete_message(user_id, message_id)
				submit_ad_zak(user_id)

			elif call.data == 'bot_stats':
				bot.delete_message(user_id, message_id)
				info_1 = execute('SELECT count(*), sum(balance) FROM users')[0]
				info_2 = execute('SELECT count(*) FROM moderators')[0]
				info_3 = execute('SELECT count(*), sum(summ) FROM payments WHERE status=1')[0]
				bot.send_message(user_id,
					'*Всего пользователей:* `'+str(info_1[0])+'`\n'+
					'*Общий баланс пользователей:* `'+str(info_1[1])+'₽`\n'+
					'*Всего модераторов:* `'+str(info_2[0])+'`\n'+
					'*Всего удачных пополнений:* `'+str(info_3[0])+'`\n'+
					'*Общая сумма пополнений:* `'+str(info_3[1])+'₽`'
				, parse_mode='MarkDown')

			elif call.data == 'set_balance':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Укажите новое значение баланса и через пробел user_id пользователя у которого нужно установить баланс:')
				bot.register_next_step_handler(call.message, set_balance)

			elif call.data == 'add_promo':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите промокод, через пробел число использований, через пробел сумму начисления:')
				bot.register_next_step_handler(call.message, add_promo)

			elif call.data == 'act_promo':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите промокод:')
				bot.register_next_step_handler(call.message, act_promo)

			elif call.data == 'dell_promo':
				bot.delete_message(user_id, message_id)
				markup = types.InlineKeyboardMarkup(row_width=1)
				info = execute('SELECT * FROM promo')
				for x in info:
					markup.add(types.InlineKeyboardButton(text=x[0]+' | '+str(x[2])+'₽ | Осталось: '+str(x[1]), callback_data='promo_dell:'+str(x[0])))
				bot.send_message(user_id, 'Выберите промокод для удаления:', reply_markup=markup)

			elif call.data.startswith('promo_dell'):
				bot.delete_message(user_id, message_id)
				info = call.data.replace('promo_dell:', '')
				execute('DELETE FROM promo WHERE promo=%s', info)
				execute('DELETE FROM promo_isp WHERE promo=%s', info)
				bot.send_message(user_id, 'Промокод успешно удален')

			elif call.data == 'bringout':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите сумму вывода и через двоеточие без пробелов реквизиты:')
				bot.register_next_step_handler(call.message, bringout)

			elif call.data == 'withdrawal_requests':
				bot.delete_message(user_id, message_id)
				info = execute('SELECT * FROM bringout WHERE status=0')
				if info == []:
					bot.send_message(user_id, 'Заявок на вывод нет')
				else:
					markup = types.InlineKeyboardMarkup(row_width=1)
					for x in info:
						name = execute('SELECT user_name FROM users WHERE user_id=%s', x[1])[0][0]
						markup.add(types.InlineKeyboardButton(text=name+' | '+str(x[2])+'₽', callback_data='withdrawal:'+str(x[0])))
					bot.send_message(user_id, 'Выберите заявку:', reply_markup=markup)

			elif call.data.startswith('withdrawal:'):
				bot.delete_message(user_id, message_id)
				req_id = call.data.replace('withdrawal:', '')
				info = execute('SELECT * FROM bringout WHERE id=%s', int(req_id))[0]
				markup = types.InlineKeyboardMarkup(row_width=2)
				markup.add(types.InlineKeyboardButton(text='Отправил', callback_data='req_sent:'+str(req_id)+':'+str(info[1])))
				markup.add(types.InlineKeyboardButton(text='Вернуть', callback_data='req_ver:'+str(req_id)+':'+str(info[1])+':'+str(info[2])), types.InlineKeyboardButton(text='Забрать', callback_data='req_zab:'+str(req_id)))
				bot.send_message(user_id, 
					'Реквизиты: '+str(info[3])+'\nСумма вывода: '+str(info[2])
				, reply_markup=markup)

			elif call.data.startswith('req_sent:'):
				bot.delete_message(user_id, message_id)
				req_id = call.data.replace('req_sent:', '').split(':')
				execute('UPDATE bringout SET status=1 WHERE id=%s', int(req_id[0]))
				bot.send_message(int(req_id[1]), 'Деньги выведены')
				bot.send_message(user_id, 'Заявка успешно скрыта')

			elif call.data.startswith('req_ver:'):
				bot.delete_message(user_id, message_id)
				req_id = call.data.replace('req_ver:', '').split(':')
				execute('UPDATE bringout SET status=2 WHERE id=%s', int(req_id[0]))
				execute('UPDATE users SET balance=balance+%s WHERE user_id=%s', [req_id[2], req_id[1]])
				bot.send_message(int(req_id[1]), 'Деньги возвращены вам на счет, создайте заявку на вывод повторно')
				bot.send_message(user_id, 'Заявка успешно скрыта')

			elif call.data.startswith('req_zab:'):
				bot.delete_message(user_id, message_id)
				req_id = call.data.replace('req_zab:', '')
				execute('UPDATE bringout SET status=3 WHERE id=%s', int(req_id))
				bot.send_message(user_id, 'Заявка успешно скрыта')

			elif call.data == 'mailing':
				bot.delete_message(user_id, message_id)
				bot.send_message(user_id, 'Введите текст рассылки (после отправки сообщения сразу начнется рассылка, если хотите отменить рассылку отправьте -):')
				bot.register_next_step_handler(call.message, mailing)

	except:
		traceback.print_exc()

@bot.message_handler(commands=['start', 'help'])
def start(message):
	try:
		user_id = message.from_user.id
		user_name = str(message.from_user.username)
		ref = message.text[7:]
		if ref == '':
			ref = 0
		try:
			execute('INSERT INTO users VALUES (%s, %s, %s, 0)', [user_id, '@'+user_name, ref])
		except:
			pass
		bot.send_message(user_id, 'Главное меню', reply_markup=main_keyboard())
	except:
		pass

@bot.message_handler(commands=['admin'])
def admin(message):
	user_id = message.from_user.id
	user_name = str(message.from_user.username)
	unxi = int(time.time())

	try:
		if user_id in admins_id:
			bot.send_message(user_id, 'Выберите действие:', reply_markup=main_admin_keyboard())
		else:
			bot.send_message(user_id, '❌ Неизвестная команда', reply_markup=main_keyboard())
	except:
		pass

@bot.message_handler(commands=['moder'])
def admin(message):
	user_id = message.from_user.id
	user_name = str(message.from_user.username)
	unxi = int(time.time())

	moderators = execute('SELECT user_id FROM moderators')
	moders = []
	for x in moderators:
		moders.append(x[0])

	try:
		if user_id in moders:
			bot.send_message(user_id, 'Выберите действие:', reply_markup=main_moder_keyboard())
		else:
			bot.send_message(user_id, '❌ Неизвестная команда', reply_markup=main_keyboard())
	except:
		pass

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	user_id = message.from_user.id
	user_name = str(message.from_user.username)
	unxi = int(time.time())

	try:
		if message.text == main_menu_btn[4]:
			bot.send_message(user_id, 'Наш гарант бот '+str(login_garant))

		elif message.text == main_menu_btn[3]:
			balance = execute('SELECT balance FROM users WHERE user_id=%s', user_id)[0][0]
			ref = execute('SELECT count(ref) FROM users WHERE ref=%s', user_id)[0][0]
			bot.send_message(user_id, 
				'Ваш user id: '+str(user_id)+'\n'+
				'Ваш логин: @'+str(user_name)+'\n'+
				'Ваш баланс: '+str(balance)+'₽\n\n'+
				
				'Кол-во ваших рефералов: '+str(ref)+'\n'+
				'Процент от каждого реферала: '+str(percent)+'%\n'+
				'Ваша реферальная ссылка:\nhttps://t.me/'+str(login_bot).replace('@', '')+'?start='+str(user_id),
			reply_markup=lk_keyboard())

		elif message.text == main_menu_btn[0]:
			bot.send_message(user_id, 'Что вы хотите купить?', reply_markup=purchase_service())

		elif message.text == main_menu_btn[1]:
			bot.send_message(user_id, 'Что вы хотите продать?', reply_markup=sale_service())

		elif message.text == main_menu_btn[2]:
			bot.send_message(user_id, 'Кто вы?', reply_markup=who_you())
		
		else:
			bot.send_message(user_id, '❌ Неизвестная команда', reply_markup=main_keyboard())
	except:
		traceback.print_exc()

try:
	bot.polling(none_stop=True)
except:
	traceback.print_exc()