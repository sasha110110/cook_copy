import telebot
import bs4
import browsersay7
from telebot import apihelper

#bot = telebot.TeleBot(config.telebot_token)
#apihelper.proxy = {
  #'http', 'socks5://login:pass@12.11.22.33:8000',
  #'https', 'socks5://login:pass@12.11.22.33:8000'
}

TOKEN = ""
bot = telebot.TeleBot(TOKEN)

overall=[]

isRunning = 0

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
  global overall
  overall.clear()
  #global isRunning
  #if not isRunning:
  chat_id = message.chat.id
  text = message.text
  msg = bot.send_message(chat_id, 'Привет, называй блюдо!')
  bot.register_next_step_handler(msg, ask) #askSource
    #isRunning = True

def ask(message): #РЕЗУЛЬТАТ - ПЕРЕЧЕНЬ РЕЦЕПТОВ
  #global isRunning
  #global browser

  chat_id = message.chat.id
  q = message.text
  qq=q.replace(" ", "+")
  url = "https://www.say7.info/search.html?q="+q
  browser.get(url) #navigate to the page
  soup = bs(browser.page_source, 'html.parser') #Get the Page Source
  anchors = soup.find_all("a", class_ = "gs-title")
  global overall
  for link in anchors:
    r=link.get_attribute_list("href")
    try:
      if r[0].endswith("html") and "Следующие" not in link.text:
        overall.append([r[0], link.text])
    except AttributeError:
     pass
  for i, el in enumerate(overall):
    
    msg = bot.send_message(chat_id, i, "...", el)
  msg = bot.send_message(chat_id, 'Пожалуйста, выбирай, какой больше по вкусу?')
  bot.register_next_step_handler(msg, give_result)

def give_result(message): #РЕЗУЛЬТАТ - ОДИН РЕЦЕПТ 
  #global isRunning
  global overall
  #global browser
  chat_id = message.chat.id
  choice = int(message.text)

  url=overall[choice][0]
  browser.get(url) #Connect to the News Link, and extract it's Page Source
  sub_soup = bs(browser.page_source, 'html.parser')
  rec=[]
  recepie=sub_soup.find("div", {'class' : "article h-recipe"})
  name=sub_soup.find("h1", {'itemprop' : "name"}).get_text()
  temp=[]
  ingr=sub_soup.find_all("li", {'class' : "p-ingredient"})
  for i in ingr:
    temp.append(i.get_text())
  inst=sub_soup.find("div", {'class' : "stepbystep e-instructions"}).get_text().replace("\n", " ").replace("\xa0", " ")
  rec.append([name, temp, inst])
  msg = bot.send_message(chat_id, rec)
  #isRunning = False
  msg_1 = bot.send_message(chat_id, 'Or do you want check another one?')
  bot.register_next_step_handler(msg, give_result)
  return

#bot.polling(none_stop=True)
if __name__ == '__main__':
  bot.infinity_polling()
