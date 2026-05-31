import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

# 1. BOT_TOKEN ni shu yerga yozing
BOT_TOKEN = "8640370469:AAH4dk_AVz7bkj1AOf_Mbh4BNz4LDcr5OgM"
bot = telebot.TeleBot(BOT_TOKEN)

# Render uchun web-server
app = Flask(__name__)

@app.route('/')
def index():
    return "Talaba AI Boti 10 ta tilda muvaffaqiyatli ishlayapti!"

# Foydalanuvchilarning tilini va holatini saqlash xotirasi
user_data = {}

# --- 10 TA TIL UCHUN LUG'AT ---
LANGS = {
    'uz': {
        'choose_lang': "Assalomu alaykum! Tilni tanlang:",
        'main_menu': "Asosiy menyu. Qanday yordam bera olaman?",
        'slide': "📊 Slayd yaratish",
        'site': "🌐 Sayt yaratish",
        'course': "📚 Kurs ishi konspekti",
        'diploma': "🎓 Diplom ishi konspekti",
        'slide_prompt': "Slayd mavzusini batafsil yozing.\n(Masalan: Mushak to'qimalari bo'yicha 10 ta slayd tayyorlab ber)",
        'course_prompt': "Kurs ishi mavzusini va qaysi adabiyotdan foydalanishni yozing.",
        'site_prompt': "Qanday sayt yaratmoqchisiz? Maqsadini yozing.",
        'diploma_prompt': "Diplom ishining mavzusi va rejasini yuboring.",
        'wait': "⏳ Ma'lumot tayyorlanmoqda, biroz kuting...",
        'author': "Dasturchi: Alimqulov Shukurullo (25-04 guruh)"
    },
    'ru': {
        'choose_lang': "Здравствуйте! Выберите язык:",
        'main_menu': "Главное меню. Чем могу помочь?",
        'slide': "📊 Создать слайды",
        'site': "🌐 Создать сайт",
        'course': "📚 Курсовая работа",
        'diploma': "🎓 Дипломная работа",
        'slide_prompt': "Напишите тему слайда детально.",
        'course_prompt': "Напишите тему курсовой работы и литературу.",
        'site_prompt': "Какой сайт вы хотите создать?",
        'diploma_prompt': "Отправьте тему и план дипломной работы.",
        'wait': "⏳ Данные готовятся, подождите...",
        'author': "Разработчик: Алимкулов Шукурулло (группа 25-04)"
    },
    'en': {
        'choose_lang': "Hello! Choose your language:",
        'main_menu': "Main menu. How can I help you?",
        'slide': "📊 Create Slides",
        'site': "🌐 Create Website",
        'course': "📚 Coursework notes",
        'diploma': "🎓 Diploma work notes",
        'slide_prompt': "Write the slide topic in detail.",
        'course_prompt': "Write the coursework topic and preferred literature.",
        'site_prompt': "What kind of website do you want to create?",
        'diploma_prompt': "Send the topic and plan of your diploma work.",
        'wait': "⏳ Preparing data, please wait...",
        'author': "Developer: Alimkulov Shukurullo (Group 25-04)"
    },
    'kz': {
        'choose_lang': "Сәлеметсіз бе! Тілді таңдаңыз:",
        'main_menu': "Басты мәзір. Қандай көмек көрсете аламын?",
        'slide': "📊 Слайд жасау",
        'site': "🌐 Сайт жасау",
        'course': "📚 Курстық жұмыс",
        'diploma': "🎓 Дипломдық жұмыс",
        'slide_prompt': "Слайд тақырыбын толық жазыңыз.",
        'course_prompt': "Курстық жұмыс тақырыбын жазыңыз.",
        'site_prompt': "Қандай сайт жасағыңыз келеді?",
        'diploma_prompt': "Дипломдық жұмыстың тақырыбы мен жоспарын жіберіңіз.",
        'wait': "⏳ Мәлімет дайындалуда, күте тұрыңыз...",
        'author': "Әзірлеуші: Алимкулов Шукурулло (25-04 топ)"
    },
    'tj': {
        'choose_lang': "Салом! Забонро интихоб кунед:",
        'main_menu': "Менюи асосӣ. Чӣ тавр кӯмак карда метавонам?",
        'slide': "📊 Сохтани слайдҳо",
        'site': "🌐 Сохтани сайт",
        'course': "📚 Кори курсӣ",
        'diploma': "🎓 Кори дипломӣ",
        'slide_prompt': "Мавзӯи слайдро муфассал нависед.",
        'course_prompt': "Мавзӯи кори курсиро нависед.",
        'site_prompt': "Шумо чӣ гуна сайт сохтан мехоҳед?",
        'diploma_prompt': "Мавзӯъ ва нақшаи кори дипломиро фиристед.",
        'wait': "⏳ Маълумот омода мешавад, лутфан интизор шавед...",
        'author': "Таҳиягар: Алимкулов Шукурулло (гурӯҳи 25-04)"
    },
    'tm': {
        'choose_lang': "Salam! Dili saýlaň:",
        'main_menu': "Esasy menýu. Nädip kömek edip bilerin?",
        'slide': "📊 Slaýd ýaratmak",
        'site': "🌐 Saýt ýaratmak",
        'course': "📚 Kurs işi",
        'diploma': "🎓 Diplom işi",
        'slide_prompt': "Slaýdyň mowzugyny giňişleýin ýazyň.",
        'course_prompt': "Kurs işiniň mowzugyny ýazyň.",
        'site_prompt': "Nähili saýt döretmek isleýärsiňiz?",
        'diploma_prompt': "Diplom işiniň mowzugyny we meýilnamasyny iberiň.",
        'wait': "⏳ Maglumat taýýarlanýar, garaşmagyňyzy haýyş edýäris...",
        'author': "Taýýarlan: Alimqulov Shukurullo (25-04 topar)"
    },
    'kg': {
        'choose_lang': "Салам! Тилди тандаңыз:",
        'main_menu': "Башкы меню. Кандай жардам бере алам?",
        'slide': "📊 Слайд жасоо",
        'site': "🌐 Сайт жасоо",
        'course': "📚 Курстук иш",
        'diploma': "🎓 Дипломдук иш",
        'slide_prompt': "Слайддын темасын толук жазыңыз.",
        'course_prompt': "Курстук иштин темасын жазыңыз.",
        'site_prompt': "Кандай сайт түзгүңүз келет?",
        'diploma_prompt': "Дипломдук иштин темасын жана планын жибериңиз.",
        'wait': "⏳ Маалымат даярдалууда, күтө туруңуз...",
        'author': "Иштеп чыккан: Alimqulov Shukurullo (25-04 тайпа)"
    },
    'tr': {
        'choose_lang': "Merhaba! Dil seçin:",
        'main_menu': "Ana menü. Nasıl yardımcı olabilirim?",
        'slide': "📊 Slayt Oluştur",
        'site': "🌐 Site Oluştur",
        'course': "📚 Dönem Ödevi",
        'diploma': "🎓 Bitirme Tezi",
        'slide_prompt': "Slayt konusunu detaylıca yazın.",
        'course_prompt': "Dönem ödevi konusunu yazın.",
        'site_prompt': "Nasıl bir site kurmak istiyorsunuz?",
        'diploma_prompt': "Tez konunuzu ve planınızı gönderin.",
        'wait': "⏳ Veriler hazırlanıyor, lütfen bekleyin...",
        'author': "Geliştirici: Alimqulov Shukurullo (25-04 grup)"
    },
    'ar': {
        'choose_lang': "مرحباً! اختر لغتك:",
        'main_menu': "القائمة الرئيسية. كيف يمكنني مساعدتك؟",
        'slide': "📊 إنشاء عرض تقديمي",
        'site': "🌐 إنشاء موقع",
        'course': "📚 بحث دراسي",
        'diploma': "🎓 رسالة تخرج",
        'slide_prompt': "اكتب موضوع العرض التقديمي بالتفصيل.",
        'course_prompt': "اكتب موضوع البحث الدراسي.",
        'site_prompt': "ما نوع الموقع الذي تريد إنشاءه؟",
        'diploma_prompt': "أرسل موضوع وخطة رسالة التخرج.",
        'wait': "⏳ جاري تحضير البيانات، يرجى الانتظار...",
        'author': "المطور: Alimqulov Shukurullo (مجموعة 25-04)"
    },
    'zh': {
        'choose_lang': "你好！请选择语言：",
        'main_menu': "主菜单。我能怎么帮您？",
        'slide': "📊 创建幻灯片",
        'site': "🌐 创建网站",
        'course': "📚 课程作业",
        'diploma': "🎓 毕业论文",
        'slide_prompt': "请详细写下幻灯片主题。",
        'course_prompt': "请写下课程作业主题。",
        'site_prompt': "您想创建什么样的网站？",
        'diploma_prompt': "发送您的毕业论文主题和计划。",
        'wait': "⏳ 数据准备中，请稍候...",
        'author': "开发者：Alimqulov Shukurullo（25-04 组）"
    }
}

# --- BUYRUQLAR ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'lang': 'uz', 'state': 'menu'} 
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz"),
        InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj"),
        InlineKeyboardButton("🇹🇲 Türkmençe", callback_data="lang_tm"),
        InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg"),
        InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
        InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
        InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh")
    )
    
    bot.send_message(chat_id, "Tilni tanlang / Choose language / Выберите язык:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    chat_id = call.message.chat.id
    lang = call.data.split('_')[1]
    user_data[chat_id] = {'lang': lang, 'state': 'menu'}
    
    bot.delete_message(chat_id, call.message.message_id)
    show_main_menu(chat_id, lang)

def show_main_menu(chat_id, lang):
    t = LANGS[lang]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(t['slide']), KeyboardButton(t['site']),
        KeyboardButton(t['course']), KeyboardButton(t['diploma'])
    )
    
    text = f"{t['main_menu']}\n\n{t['author']}"
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    lang = user_data.get(chat_id, {}).get('lang', 'uz')
    t = LANGS[lang]
    text = message.text

    if text == t['slide']:
        user_data[chat_id]['state'] = 'waiting_slide'
        bot.send_message(chat_id, t['slide_prompt'])
    elif text == t['site']:
        user_data[chat_id]['state'] = 'waiting_site'
        bot.send_message(chat_id, t['site_prompt'])
    elif text == t['course']:
        user_data[chat_id]['state'] = 'waiting_course'
        bot.send_message(chat_id, t['course_prompt'])
    elif text == t['diploma']:
        user_data[chat_id]['state'] = 'waiting_diploma'
        bot.send_message(chat_id, t['diploma_prompt'])
    else:
        state = user_data.get(chat_id, {}).get('state', 'menu')
        if state != 'menu':
            # Foydalanuvchi so'rovni yuborgan holat
            bot.send_message(chat_id, t['wait'])
            
            # HOZIRCHA API ULANMAGANLIGI UCHUN FAKE JAVOB:
            javob = f"✅ [{text}]\n\nBu funksiya tez orada sun'iy intellekt orqali to'liq ishga tushadi!"
            bot.send_message(chat_id, javob)
            user_data[chat_id]['state'] = 'menu'
        else:
            show_main_menu(chat_id, lang)

# --- ISHGA TUSHIRISH ---
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
