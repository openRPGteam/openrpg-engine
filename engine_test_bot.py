import telebot
import engine
import os
from random import randint

bot = telebot.TeleBot("TOKEN")

ACTIVE_USERS = {}

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, "OpenRPG engine preview. Use /spawn to start")

@bot.message_handler(commands=['spawn'])
def spawn(message):
    map_spawn_pos = [randint(200, 2800), randint(200, 1500)]
    usr = engine.character('hero.png', map_pos=map_spawn_pos)
    move = engine.mover(usr)
    ACTIVE_USERS[message.chat.id] = move
    fname = engine.save_background(move.spawn(), "{}.jpg".format(message.chat.id))
    fname_handle = open(fname, 'rb')
    bot.send_photo(message.chat.id, fname_handle)
    fname_handle.close()
    os.remove(fname)

@bot.message_handler(commands=['left'])
def left(message):
    if message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(message.chat.id, "Spawn yourself first")
    else:
        fname = engine.save_background(ACTIVE_USERS[message.chat.id].left(), "{}.jpg".format(message.chat.id))
        fname_handle = open(fname, 'rb')
        bot.send_photo(message.chat.id, fname_handle)
        fname_handle.close()
        os.remove(fname)

@bot.message_handler(commands=['right'])
def right(message):
    if message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(message.chat.id, "Spawn yourself first")
    else:
        fname = engine.save_background(ACTIVE_USERS[message.chat.id].right(), "{}.jpg".format(message.chat.id))
        fname_handle = open(fname, 'rb')
        bot.send_photo(message.chat.id, fname_handle)
        fname_handle.close()
        os.remove(fname)

@bot.message_handler(commands=['up'])
def up(message):
    if message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(message.chat.id, "Spawn yourself first")
    else:
        fname = engine.save_background(ACTIVE_USERS[message.chat.id].up(), "{}.jpg".format(message.chat.id))
        fname_handle = open(fname, 'rb')
        bot.send_photo(message.chat.id, fname_handle)
        fname_handle.close()
        os.remove(fname)

@bot.message_handler(commands=['down'])
def down(message):
    if message.chat.id not in ACTIVE_USERS.keys():
        bot.send_message(message.chat.id, "Spawn yourself first")
    else:
        fname = engine.save_background(ACTIVE_USERS[message.chat.id].down(), "{}.jpg".format(message.chat.id))
        fname_handle = open(fname, 'rb')
        bot.send_photo(message.chat.id, fname_handle)
        fname_handle.close()
        os.remove(fname)

@bot.message_handler(commands=['end_game'])
def end_game(message):
    del ACTIVE_USERS[message.chat.id]
    bot.send_message(message.chat.id, "Game stopped")

bot.polling(none_stop=True)
