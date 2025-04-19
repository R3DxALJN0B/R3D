import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import subprocess

TOKEN = '7789954056:AAHolpwolU7T2DiYwgwV6oelbqTnH2cZTrA'
bot = telebot.TeleBot(TOKEN)

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🔍 البحث عن رقم جوال"),
        KeyboardButton("🔍 البحث عن اسم أو اسم مستخدم"),
        KeyboardButton("🔍 البحث عن بريد إلكتروني"),
        KeyboardButton("🔓 البحث عن تسريبات")
    )
    bot.send_message(message.chat.id, "مرحبًا بك في بوت جمع المعلومات!
اختر نوع البحث المطلوب:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "🔍 البحث عن رقم جوال":
        user_states[chat_id] = "phone"
        bot.send_message(chat_id, "أرسل رقم الجوال الآن:")
    elif text == "🔍 البحث عن اسم أو اسم مستخدم":
        user_states[chat_id] = "username"
        bot.send_message(chat_id, "أرسل الاسم أو اسم المستخدم الآن:")
    elif text == "🔍 البحث عن بريد إلكتروني":
        user_states[chat_id] = "email"
        bot.send_message(chat_id, "أرسل البريد الإلكتروني الآن:")
    elif text == "🔓 البحث عن تسريبات":
        user_states[chat_id] = "leaks"
        bot.send_message(chat_id, "أرسل البريد أو اسم المستخدم أو الرقم:")
    else:
        state = user_states.get(chat_id)
        if state == "phone":
            bot.send_message(chat_id, "جارٍ البحث باستخدام PhoneInfoga...")
            result = subprocess.getoutput(f"cd phoneinfoga && python3 phoneinfoga.py -n {text} --recon")
            bot.send_message(chat_id, f"النتيجة:\n{result[:4000]}")
        elif state == "username":
            bot.send_message(chat_id, "جارٍ البحث باستخدام Sherlock...")
            result = subprocess.getoutput(f"cd sherlock && python3 sherlock.py {text} --print-found")
            bot.send_message(chat_id, f"النتيجة:\n{result[:4000]}")
        elif state == "email":
            bot.send_message(chat_id, "جارٍ البحث باستخدام Holehe وSocialscan...")
            holehe = subprocess.getoutput(f"cd holehe && python3 holehe.py {text}")
            socialscan = subprocess.getoutput(f"cd socialscan && python3 socialscan.py --email {text}")
            bot.send_message(chat_id, f"[Holehe]
{holehe[:1000]}

[Socialscan]
{socialscan[:2800]}")
        elif state == "leaks":
            bot.send_message(chat_id, "جارٍ البحث عن التسريبات باستخدام عدة أدوات...")
            email_info = ""
            phone_info = ""
            other_info = ""

            # theHarvester
            try:
                harvester = subprocess.getoutput(f"cd theHarvester && python3 theHarvester.py -d {text} -b all")
                other_info += "[theHarvester]\n" + harvester[:1000] + "\n"
            except Exception as e:
                other_info += f"[theHarvester] خطأ: {e}\n"

            # Holehe
            try:
                holehe = subprocess.getoutput(f"cd holehe && python3 holehe.py {text}")
                email_info += "[Holehe]\n" + holehe[:1000] + "\n"
            except Exception as e:
                email_info += f"[Holehe] خطأ: {e}\n"

            # HaveIBeenPwned (Scraping)
            try:
                import requests
                hbp = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{text}", headers={"User-Agent": "Mozilla/5.0"})
                if hbp.status_code == 200 and "Domain found" not in hbp.text:
                    email_info += "[HaveIBeenPwned] تم العثور على تسريبات.\n"
                else:
                    email_info += "[HaveIBeenPwned] لا يوجد تسريبات.\n"
            except Exception as e:
                email_info += f"[HIBP] خطأ: {e}\n"

            # BreachDirectory (Scraping)
            try:
                bd = requests.get(f"https://breachdirectory.org/?search={text}", headers={"User-Agent": "Mozilla/5.0"})
                if "Results found" in bd.text or "pwned" in bd.text:
                    email_info += "[BreachDirectory] تم العثور على تسريبات.\n"
                else:
                    email_info += "[BreachDirectory] لا يوجد نتائج.\n"
            except Exception as e:
                email_info += f"[BreachDirectory] خطأ: {e}\n"

            result_message = "**النتائج:**\n\n"
            result_message += "البريد الإلكتروني:\n" + email_info + "\n"
            result_message += "رقم الجوال:\n" + (phone_info if phone_info else "لا توجد نتائج حالياً.") + "\n"
            result_message += "تسريبات أخرى:\n" + (other_info if other_info else "لا توجد نتائج حالياً.") + "\n"

            bot.send_message(chat_id, result_message)
            bot.send_message(chat_id, "جارٍ البحث عن التسريبات باستخدام theHarvester...")
            result = subprocess.getoutput(f"cd theHarvester && python3 theHarvester.py -d {text} -b all")
            bot.send_message(chat_id, f"النتيجة:\n{result[:4000]}")
        else:
            bot.send_message(chat_id, "يرجى اختيار نوع البحث أولاً من الأزرار.")

bot.infinity_polling()