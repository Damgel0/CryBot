#imports, use pip3 install telebot
import telebot as tb
from telebot import types


#Write token of bot. U can get it at Bot_Father
token = 'YOUR_TOKEN'

bot = tb.TeleBot(token)

clients = 0
clientsLocate = 'clients.txt' #Making a database to show how many clients are left
ratesLocate = 'rates.txt' #Making a database of rates

#Start message
@bot.message_handler(commands=['start'])
def start(message):
    send_start_menu(message.chat.id)

def send_start_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Questions', callback_data='quest')
    markup.row(btn1)
    btn4 = types.InlineKeyboardButton('See works', url='https://t.me/crypt1csi')
    markup.row(btn4)
    btn2 = types.InlineKeyboardButton('Rates', callback_data='rate')
    btn3 = types.InlineKeyboardButton('Queue', callback_data='queue')
    markup.row(btn2, btn3)
    bot.send_message(message, 'Choose option \n\nⓘ If bot don\'t request, please wait.', reply_markup=markup)

#Special command for owner
@bot.message_handler(commands=['q'])
def queue_zarya(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Menu', callback_data='menu')
    markup.row(btn1)
    bot.send_message("USER\"S CHAT ID (E.G: 1234)", 'Write queue: ', reply_markup=markup)
    bot.register_next_step_handler(message, que)

def que(message):
    global clients
    try:
        count = int(message.text.strip())
        clients = count
        with open(clientsLocate, 'w') as file:
            file.write(str(clients))
    except ValueError:
        bot.send_message("USER\"S CHAT ID (E.G: 1234)", 'Write number -_-')
        return

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'quest':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Menu', callback_data='menu')
        markup.row(btn1)
        bot.send_message(callback.message.chat.id, 'Most asked questions:\nHow much worth to order?\n  • Avatar - $10\n  • Art - $20\nWhere can u order art?\n  • Write here @ryantkelly', reply_markup=markup)
    elif callback.data == 'rate':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('See rates', callback_data='see_rates')
        btn2 = types.InlineKeyboardButton('Write rate', callback_data='write_rate')
        markup.row(btn1, btn2)
        btn3 = types.InlineKeyboardButton('Menu', callback_data='menu')
        markup.row(btn3)
        bot.send_message(callback.message.chat.id, 'Choose option', reply_markup=markup)
    elif callback.data == 'queue':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Menu', callback_data='menu')
        markup.row(btn1)
        try:
            with open(clientsLocate, 'r') as file:
                clients = int(file.read())
        except:
            bot.send_message(callback.message.chat.id, 'No data')

        try:
            bot.send_message(callback.message.chat.id, f'Clients left {clients}', reply_markup=markup)
        except:
            print('No clients')

    elif callback.data == 'write_rate':
        bot.send_message(callback.message.chat.id, 'Write rate here: ')
        bot.register_next_step_handler(callback.message, save_rate)
    elif callback.data == 'menu':
        send_start_menu(callback.message.chat.id)
    elif callback.data == 'see_rates':
        try:
            with open(ratesLocate, 'r') as file:
                ratings = file.read()
        except:
            bot.send_message(callback.message.chat.id, 'No data')

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Menu', callback_data='menu')
        markup.row(btn1)
        try:
            bot.send_message(callback.message.chat.id, f'Rates:\n{ratings}', reply_markup=markup)
        except:
            print("No rates")

def save_rate(message):
    rating = message.text.strip()
    user_name = message.from_user.username
    if user_name:
        rating_with_name = f'Username: @{user_name}\nRate: {rating}\n'
    else:
        user_name = message.from_user.first_name 
        rating_with_name = f'Username: {user_name}\nRate: {rating}\n'

    with open(ratesLocate, 'a') as file:
        file.write(rating_with_name)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Menu', callback_data='menu')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'Thank you for rate!', reply_markup=markup)


if __name__ == "__main__":
    bot.polling()