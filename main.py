import telebot
import datetime
import json

# initialize bot
token_file = open("data/token.txt", 'r')
token = token_file.read()
token_file.close()
bot = telebot.TeleBot(token)

lessons_to_add = dict()

WEEKDAYS = {"Понедельник" : "monday",
            "Вторник" : "tuesday",
            "Среда" : "wednesday",
            "Четверг" : "thursday",
            "Пятница" : "friday",
            "Суббота" : "saturday",
            "Воскресенье" : "sunday"}

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, "Darova, all work")

@bot.message_handler(commands = ['add_lesson'])
def start_add_lesson(message):
    lessons_to_add[message.from_user.username] = []
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
    if message.text in WEEKDAYS:
        lessons_to_add[message.from_user.username].append(WEEKDAYS[message.text])
        bot.send_message(message.chat.id, "Во сколько у тебя пара ? (Введи в формета 08:45)", reply_markup = telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_time)
    else:
        bot.send_message(message.chat.id, "Неверный день недели, попробуй ещё раз")
        bot.register_next_step_handler(message, add_weekday)

def add_time(message):
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
        lesson_time = datetime.time(hour = hours, minute = minutes)
        lessons_to_add[message.from_user.username].append(lesson_time)
        bot.send_message(message.chat.id, "Напиши название пары")
        bot.register_next_step_handler(message, add_lesson_name)

def add_lesson_name(message):
    lessons_to_add[message.from_user.username].append(message.text)
    bot.send_message(message.chat.id, "Напиши название аудиторию, в которой проводится пара")
    bot.register_next_step_handler(message, add_lesson_place)

def add_lesson_place(message):
    lessons_to_add[message.from_user.username].append(message.text)
    bot.send_message(message.chat.id, f"Твоя пара, под названием {lessons_to_add[message.from_user.username][2]}"
                     " добавлена в базу и теперь ты будешь получать уведомления о ней за 5 минут до начала (на самом деле не будешь, даже иформация о твоей паре пока никуда не добавляется, бот ещё находится на этапе разработки, спасибо, что помогаешь в его тестировании)")


@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, "Тут буит помощь")
    print(message)

@bot.message_handler()
def info(message):
    bot.send_message(message.chat.id, "Не пишите мне, пожалуйста, ничего кроме команд. Я глупенький, обычные сообщения не обрабатываю🥺. Да и не за чем мне это."
                     " Для какого-либо фидбека лучше напишите напрямую моему папе @VEymas")

def get_weekday(weekday):
    return WEEKDAYS[weekday]

def add_lesson(id, lesson, weekday, time, place, data):
    if not (id in data):
        data[id]["sunday"] = []
        data[id]["monday"] = []
        data[id]["tuesday"] = []
        data[id]["wednesday"] = []
        data[id]["thursday"] = []
        data[id]["friday"] = []
        data[id]["saturday"] = []
    data[id][weekday.lower()].append({time : [lesson, place]})




data = json.load(open("data/database.json"))




bot.polling(none_stop = True)