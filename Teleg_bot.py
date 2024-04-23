from telebot import *
from paper import Text2ImageAPI
import base64
from PIL import Image

token='6753527005:AAFfepvf1idMjsbbS6W9U1d4RonDUuFIOX4'
bot = telebot.TeleBot(token)
style = ''
sent = ''

markup_1 = types.ReplyKeyboardMarkup()
markup_2 = types.ReplyKeyboardMarkup()


btn_1 = types.KeyboardButton('Кандинский', )
btn_2 = types.KeyboardButton('Детальное фото')
btn_3 = types.KeyboardButton('Аниме')
btn_4 = types.KeyboardButton('Свой стиль')

btn_2_1 = types.KeyboardButton('16:9')
btn_2_2 = types.KeyboardButton('3:2')
btn_2_3 = types.KeyboardButton('1:1')
btn_2_4 = types.KeyboardButton('2:3')
btn_2_5 = types.KeyboardButton('9:16')

markup_1.row(btn_1, btn_2, btn_3, btn_4)
markup_2.row(btn_2_1,btn_2_2,btn_2_3,btn_2_4,btn_2_5)

#Стартовые кнопки Телеграмм бота и реплеер на командное сообщение /start
@bot.message_handler(commands=['start'])
def start(message):
    markup_3 = types.ReplyKeyboardMarkup()
    btn_3_1 = types.KeyboardButton('Начать генерацию')
    markup_3.row(btn_3_1)
    bot.send_message(message.chat.id,'Здраствуй, это бот генерирующий фотографии по тексту имеющий различные стили генерирования\n\n'
                                     '<b>Этот бот будет в дальнейшем развиваться и добавляться еще большее количество стилей генерирования'
                                     '. За идеями и предложениями пишите --> @mgnbv.</b>\n\n', reply_markup=markup_3, parse_mode='html')


#Реплеер на командное сообщение /Help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,'Вы должны задать, стиль генерируемого рисунка, а уже после <b>написать текст</b>, по которому будет генерироваться текст.\n\n'
                                     'В случае выявлени проблем пишите --> @mgnbv', parse_mode='html' )


#Реплеер на сообщения от пользователя типа данных "ФОТО"
@bot.message_handler(content_types=['photo'])
def start(message):
    # markup = types.InlineKeyboardMarkup()
    # btn_1 = types.InlineKeyboardButton('еда', url='https://www.russianfood.com/')
    # btn_2 = types.InlineKeyboardButton('сон', url="https://www.fgu-obp.ru/news/novosti/10-sovetov-po-uluchsheniyu-sna/")
    # btn_3 = types.InlineKeyboardButton('спорт', url="https://www.sports.ru/")
    # markup.row(btn_1,btn_2,btn_3)
    bot.reply_to(message,'К сожалению бот еще не поддерживает функцию рисунка по фото😔')


#Реплайер текстовых сообщений Телеграмм бота
@bot.message_handler()
def message(message):
    global style, sent
    if message.text == 'Начать генерацию':
        bot.send_message(message.chat.id, 'Так, а теперь выбери стиль:', reply_markup=markup_1)
    if message.text == 'Кандинский':
        style = 'KANDINSKY'
        sent = bot.send_message(message.chat.id, 'Отлично, теперь напиши текст для генерации...')
        bot.register_next_step_handler(sent, generator)
    if message.text == 'Детальное фото':
        style = 'UHD'
        sent = bot.send_message(message.chat.id, 'Отлично, теперь напиши текст для генерации...')
        bot.register_next_step_handler(sent, generator)
    if message.text == 'Аниме':
        style = 'ANIME'
        sent = bot.send_message(message.chat.id, 'Отлично, теперь напиши текст для генерации...')
        bot.register_next_step_handler(sent, generator)
    if message.text == 'Свой стиль':
        style = 'DEFAULT'
        sent = bot.send_message(message.chat.id, 'Отлично, теперь напиши текст для генерации...')
        bot.register_next_step_handler(sent, generator)
    if message.text.lower() in ['привет', 'здраствуй']:
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, как дела')
    if message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}')



def generator(message):
    global style, sent
    bot.send_message(message.chat.id, 'Теперь придется подождать...')
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'CB68F40CEFD78AD5EE6A1018FDA46819', 'D120B2D968C4AB6BAE6B92B93FFA3EEB')
    model_id = api.get_model()
    uuid = api.generate(message.text, model_id, style='')
    images = api.check_generation(uuid)
    with open(r'C:\Users\Huawei\OneDrive\Рабочий стол\teleg\output_path' + message.from_user.username, 'wb') as f:
        for i in images:
            f.write(base64.b64decode(i))
        imj_obj = Image.open(r'C:\Users\Huawei\OneDrive\Рабочий стол\teleg\output_path' + message.from_user.username)
        bot.send_photo(message.chat.id,imj_obj)


#Запускатель измененений
bot.polling()
