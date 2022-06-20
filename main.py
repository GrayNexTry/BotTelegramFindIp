import telebot
import socket
import requests

bot = telebot.TeleBot("***")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}! \nКак пользоваться ботом? \nЛегко, пишешь /search (IP) или (Домен) и все!")

@bot.message_handler(commands=['search'])
def search(message):
    ip = message.text.split()[1]
    chek_IP(ip=ip, message=message)
    
def chek_IP(ip, message):
    try:
        responce = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        
        answer = bot.send_message(message.chat.id, "Запрос обрабатывается...")
        bot.edit_message_text(f"Страна: {responce.get('country')} \nРегион: {responce.get('regionName')} \nГород: {responce.get('city')} \nПочтовый индекс: {responce.get('zip')} \nЧасовой пояс: {responce.get('timezone')} \nПровайдер: {responce.get('isp')}", chat_id=message.chat.id, message_id=answer.id)
        bot.send_location(message.chat.id, latitude=responce.get('lat'), longitude=responce.get('lon'))
        
    except socket.error:
        try:
            myHostName = socket.gethostname(ip)
        
            answer = bot.send_message(message.chat.id, "Запрос обрабатывается...")
            bot.edit_message_text(f"Страна: {responce.get('country')} \nРегион: {responce.get('regionName')} \nГород: {responce.get('city')} \nПочтовый индекс: {responce.get('zip')} \nЧасовой пояс: {responce.get('timezone')} \nПровайдер: {responce.get('isp')}", chat_id=message.chat.id, message_id=answer.id)
            bot.send_location(message.chat.id, latitude=responce.get('lat'), longitude=responce.get('lon'))
            
        except socket.error:
            bot.send_message(message.chat.id, "Не правильный домен или IP")
    
bot.polling(non_stop=True)
