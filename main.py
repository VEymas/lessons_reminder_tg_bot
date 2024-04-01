import telebot
import datetime
import json
import multiprocessing
import threading
import time

DATA_FILE_NAME = "data/database.json"

today_lessons = dict()

# initialize bot
token_file = open("data/token.txt", 'r')
token = token_file.read()
token_file.close()
bot = telebot.TeleBot(token)

data_fd = open(DATA_FILE_NAME, 'r+')
data = json.load(data_fd)
data_fd.close()

lessons_to_add = dict()

WEEKDAYS = {"понедельник" : "monday",
            "вторник" : "tuesday",
            "среда" : "wednesday",
            "четверг" : "thursday",
            "пятница" : "friday",
            "суббота" : "saturday",
            "воскресенье" : "sunday"}

WEEKDAYS_NUMBER = {0 : "monday",
            1 : "tuesday",
            2 : "wednesday",
            3 : "thursday",
            4 : "friday",
            5 : "saturday",
            6 : "sunday"}

def time_handler():
    global today_lessons
    
    while(1):
        current_time = datetime.datetime.now()
        print(current_time)


def add_user(id, username):
    data[id] = dict()
    data[id]["monday"] = []
    data[id]["tuesday"] = []
    data[id]["wednesday"] = []
    data[id]["thursday"] = []
    data[id]["friday"] = []
    data[id]["saturday"] = []
    data[id]["sunday"] = []
    data[id]["username"] = username

@bot.message_handler(commands = ['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("Добавить пару")
    btn2 = telebot.types.KeyboardButton("Помощь")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "Привет, благодаря мне ты можешь получать уведомления о своих" 
                     "парах и месте их проведения незадолго до их начала", reply_markup = markup)

@bot.message_handler(commands = ['add_lesson'])
def start_add_lesson(message):
    if str(message.chat.id) not in data:
        print(f"user {message.chat.id} not in data")
        add_user(str(message.chat.id), message.from_user.username)

    lessons_to_add[str(message.chat.id)] = []
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("Понедельник")
    btn2 = telebot.types.KeyboardButton("Вторник")
    markup.row(btn1, btn2)
    btn3 = telebot.types.KeyboardButton("Среда")
    btn4 = telebot.types.KeyboardButton("Четверг")
    markup.row(btn3, btn4)
    btn5 = telebot.types.KeyboardButton("Пятница")
    btn6 = telebot.types.KeyboardButton("Суббота")
    markup.row(btn5, btn6)
    btn7 = telebot.types.KeyboardButton("Воскресенье???")
    markup.row(btn7)
    bot.send_message(message.chat.id, "В какой день недели у тебя пара?", reply_markup = markup)
    bot.register_next_step_handler(message, add_weekday)

def add_weekday(message):
    if message.text.lower() in WEEKDAYS:
        lessons_to_add[str(message.chat.id)].append(WEEKDAYS[message.text.lower()])
        bot.send_message(message.chat.id, "Во сколько у тебя пара ? (Введи в формета 08:45)", reply_markup = telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_time)
    else:
        bot.send_message(message.chat.id, "Неверный день недели, попробуй ещё раз")
        bot.register_next_step_handler(message, add_weekday)

def add_time(message):
    # TODO think about time
    if len(message.text) != 5 or message.text[2] != ':':
        bot.send_message(message.chat.id, "Неверный формат, попробуй ещё раз")
        bot.register_next_step_handler(message, add_time)
    else:
        try:
            hours = int(message.text[:2])
            minutes = int(message.text[3:])
        except:
            bot.send_message(message.chat.id, "Неверный формат, попробуй ещё раз")
            bot.register_next_step_handler(message, add_time)
        # lesson_time = datetime.time(hour = hours, minute = minutes)
        lessons_to_add[str(message.chat.id)].append(message.text)
        bot.send_message(message.chat.id, "Напиши название пары")
        bot.register_next_step_handler(message, add_lesson_name)

def add_lesson_name(message):
    lessons_to_add[str(message.chat.id)].append(message.text)
    bot.send_message(message.chat.id, "Напиши название аудитории, в которой проводится пара")
    bot.register_next_step_handler(message, add_lesson_place)

def add_lesson_place(message):
    lessons_to_add[str(message.chat.id)].append(message.text)
    add_lesson(str(message.chat.id))
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("Добавить пару")
    btn2 = telebot.types.KeyboardButton("Помощь")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f"Твоя пара, под названием {lessons_to_add[str(message.chat.id)][2]}"
                     " добавлена в базу и теперь ты будешь получать уведомления о ней за 5 минут до начала "
                     "(на самом деле не будешь, но информация о твоей паре добавилась, бот"
                      " ещё находится на этапе разработки, спасибо, что помогаешь в его тестировании)", reply_markup = markup)
    del lessons_to_add[str(message.chat.id)]


def add_lesson(chat_id):
    weekday = lessons_to_add[chat_id][0]
    time = lessons_to_add[chat_id][1]
    lesson_name = lessons_to_add[chat_id][2]
    lesson_place = lessons_to_add[chat_id][3]
    data[chat_id][weekday].append({time : [lesson_name, lesson_place]})
    data_fd = open(DATA_FILE_NAME, "w")
    json.dump(data, data_fd, indent = 4)
    data_fd.close()


@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, "Тут буит помощь")

@bot.message_handler()
def info(message):
    if message.text == "Добавить пару":
        start_add_lesson(message)
    elif message.text == "Помощь":
        help(message)
    else:
        bot.send_message(message.chat.id, "Не пишите мне, пожалуйста, ничего кроме команд. Я глупенький, обычные сообщения не обрабатываю🥺. Да и не за чем мне это."
                     " Для какого-либо фидбека лучше напишите напрямую моему папе @VEymas")
        
# t1 = threading.Thread(target = time_handler) 
# t1.start()

bot.polling(none_stop = True)