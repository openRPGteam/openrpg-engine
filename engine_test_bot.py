import telebot
import render
import os
from random import randint

bot = telebot.TeleBot("TOKEN")

USER_POS = {}
BACKGROUND = {}

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, "OpenRPG engine preview. Use /spawn to start")

@bot.message_handler(commands=['spawn'])
def spawn(message):
    back, curr_pos = render.get_background((1500, 850), 400), [1500, 850]
    back = render.fill_with_shit(back, randint(2, 11))
    BACKGROUND[message.chat.id] = back.copy()
    back = render.add_dynamic_sprites(back, ('hero.jpg', render.middle(back)))
    USER_POS[message.chat.id] = [curr_pos, render.middle(back)]
    tmp = render.tempfile(back, message)
    tmpi = open(tmp, 'rb')
    bot.send_photo(message.chat.id, tmpi)
    tmpi.close()
    os.remove(tmp)

@bot.message_handler(commands=['left'])
def left(message):
    pos = USER_POS[message.chat.id] if message.chat.id in USER_POS.keys() else None
    back = BACKGROUND[message.chat.id].copy() if message.chat.id in BACKGROUND.keys() else None
    if pos == None or back == None:
        bot.send_message(message.chat.id, 'Spawn yourself first')
    else:
        if pos[1][0] >= 20:
            pos[1][0] -= 20
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            USER_POS[message.chat.id] = pos
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        else:
            pos[0][0] -= 400
            back = render.get_background(pos[0], 400)
            pos[1][0] = 370
            USER_POS[message.chat.id] = pos
            back = render.fill_with_shit(back, randint(2, 11))
            BACKGROUND[message.chat.id] = back.copy()
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        back.close()

@bot.message_handler(commands=['right'])
def right(message):
    pos = USER_POS[message.chat.id] if message.chat.id in USER_POS.keys() else None
    back = BACKGROUND[message.chat.id].copy() if message.chat.id in BACKGROUND.keys() else None
    if pos == None or back == None:
        bot.send_message(message.chat.id, 'Spawn yourself first')
    else:
        if pos[1][0] <= 350:
            pos[1][0] += 20
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            USER_POS[message.chat.id] = pos
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        else:
            pos[0][0] += 400
            back = render.get_background(pos[0], 400)
            pos[1][0] = 0
            USER_POS[message.chat.id] = pos
            back = render.fill_with_shit(back, randint(2, 11))
            BACKGROUND[message.chat.id] = back.copy()
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        back.close()

@bot.message_handler(commands=['up'])
def up(message):
    pos = USER_POS[message.chat.id] if message.chat.id in USER_POS.keys() else None
    back = BACKGROUND[message.chat.id].copy() if message.chat.id in BACKGROUND.keys() else None
    if pos == None or back == None:
        bot.send_message(message.chat.id, 'Spawn yourself first')
    else:
        if pos[1][1] >= 20:
            pos[1][1] -= 20
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            USER_POS[message.chat.id] = pos
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        else:
            pos[0][1] -= 400
            back = render.get_background(pos[0], 400)
            pos[1][1] = 340
            USER_POS[message.chat.id] = pos
            back = render.fill_with_shit(back, randint(2, 11))
            BACKGROUND[message.chat.id] = back.copy()
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        back.close()

@bot.message_handler(commands=['down'])
def down(message):
    pos = USER_POS[message.chat.id] if message.chat.id in USER_POS.keys() else None
    back = BACKGROUND[message.chat.id].copy() if message.chat.id in BACKGROUND.keys() else None
    if pos == None or back == None:
        bot.send_message(message.chat.id, 'Spawn yourself first')
    else:
        if pos[1][1] <= 320:
            pos[1][1] += 20
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            USER_POS[message.chat.id] = pos
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        else:
            pos[0][1] += 400
            back = render.get_background(pos[0], 400)
            pos[1][1] = 0
            USER_POS[message.chat.id] = pos
            back = render.fill_with_shit(back, randint(2, 11))
            BACKGROUND[message.chat.id] = back.copy()
            back = render.add_dynamic_sprites(back, ('hero.jpg', tuple(pos[1])))
            tmp = render.tempfile(back, message)
            tmpi = open(tmp, 'rb')
            bot.send_photo(message.chat.id, tmpi)
            tmpi.close()
            os.remove(tmp)
        back.close()


bot.polling(none_stop=True)
