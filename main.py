import random
import telebot
from telebot import types
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен из переменных окружения
token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

# Хранение выбранного языка для каждого чата
# Значения: 'ru' или 'en'
user_lang = {}

# Метки/подписи на двух языках (RU/EN)
LABELS = {
    'ru': {
        'choose_language': 'Выберите язык / Choose language:',
        'lang_ru': 'Русский',
        'lang_en': 'English',
        'profession': 'Профессия',
        'age': 'Возраст',
        'gender': 'Пол',
        'sickness': 'Болезнь',
        'phobia': 'Фобия',
        'hobby': 'Хобби',
        'item': 'Багаж',
        'card': 'Карта',
        'image_not_found': 'Изображение не найдено',
        'lang_set': 'Язык установлен: Русский',
    },
    'en': {
        'choose_language': 'Choose your language / Выберите язык:',
        'lang_ru': 'Русский',
        'lang_en': 'English',
        'profession': 'Profession',
        'age': 'Age',
        'gender': 'Gender',
        'sickness': 'Sickness',
        'phobia': 'Phobia',
        'hobby': 'Hobby',
        'item': 'Baggage',
        'card': 'Card',
        'image_not_found': 'Image not found',
        'lang_set': 'Language set: English',
    },
}

# Языковые наборы значений
PROFESSIONS = {
    'ru': [
        "Инженер", "Врач", "Солдат", "Психолог", "Программист", "Астроном", "Повар",
        "Археолог", "Биолог", "Строитель", "Электрик", "Взломщик", "Писатель",
        "Гидролог", "Лётчик", "Охранник", "Художник", "Детектив", "Спасатель",
        "Ведущий ТВ", "Дизайнер игр", "Оружейник", "Фермер", "Криминалист",
        "Радиотехник", "Бармен", "Клоун"
    ],
    'en': [
        "Engineer", "Doctor", "Soldier", "Psychologist", "Programmer", "Astronomer", "Chef",
        "Archaeologist", "Biologist", "Construction worker", "Electrician", "Hacker", "Writer",
        "Hydrologist", "Pilot", "Security guard", "Artist", "Detective", "Rescuer",
        "TV host", "Game designer", "Gunsmith", "Farmer", "Forensic expert",
        "Radio technician", "Bartender", "Clown"
    ],
}

GENDERS = {
    'ru': ["Мужчина", "Женщина"],
    'en': ["Male", "Female"],
}

FERTILITY = {
    'ru': ["Плодн(ая/ый)", "Бесплодн(ая/ый)"],
    'en': ["Fertile", "Infertile"],
}

SICKNESSES = {
    'ru': [
        "Грипп", "ОРВИ", "Ангина", "Бронхит", "Пневмония", "Тонзиллит", "Отит",
        "Гастрит", "Язва желудка", "Колит", "Геморрой", "Аппендицит", "Гипертония",
        "Ишемическая болезнь сердца", "Аритмия", "Инсульт", "Инфаркт миокарда",
        "Остеохондроз", "Артрит", "Остеопороз", "Подагра", "Сахарный диабет 1 типа",
        "РАК", "Аутизм", "Гепатит C", "Цирроз печени", "Почечная недостаточность",
        "Мигрень", "Анемия", "Псориаз", "Идеально здоров", "Идеально здоров",
        "Идеально здоров", "Идеально здоров", "Идеально здоров"
    ],
    'en': [
        "Flu", "Acute respiratory infection", "Sore throat", "Bronchitis", "Pneumonia",
        "Tonsillitis", "Otitis (ear infection)", "Gastritis", "Stomach ulcer", "Colitis",
        "Hemorrhoids", "Appendicitis", "Hypertension", "Coronary heart disease", "Arrhythmia",
        "Stroke", "Myocardial infarction", "Osteochondrosis", "Arthritis", "Osteoporosis",
        "Gout", "Type 1 diabetes", "Cancer", "Autism", "Hepatitis C", "Liver cirrhosis",
        "Kidney failure", "Migraine", "Anemia", "Psoriasis", "Perfectly healthy",
        "Perfectly healthy", "Perfectly healthy", "Perfectly healthy", "Perfectly healthy"
    ],
}

PHOBIAS = {
    'ru': [
        "Боязнь замкнутых пространств", "Боязнь темноты", "Боязнь воды", "Боязнь высоты",
        "Боязнь громких звуков", "Боязнь толпы", "Боязнь женщин", "Боязнь мужчин",
        "Боязнь собак", "Боязнь кошек", "Нет фобий", "Нет фобий", "Нет фобий", "Нет фобий"
    ],
    'en': [
        "Claustrophobia", "Fear of darkness", "Fear of water", "Fear of heights",
        "Fear of loud sounds", "Fear of crowds", "Fear of women", "Fear of men",
        "Fear of dogs", "Fear of cats", "No phobias", "No phobias", "No phobias", "No phobias"
    ],
}

HOBBIES = {
    'ru': [
        "Рыбалка", "Охота", "Выращивание растений (садоводство, гидропоника)",
        "Кулинария и приготовление еды на костре", "Фермерство и разведение животных",
        "Оказание первой медицинской помощи", "Травничество (знание лечебных растений)",
        "Ремонт и починка техники", "Столярное дело", "Кузнечное дело", "Рукоделие и шитьё",
        "Изготовление оружия и ловушек", "Стрельба (лук, арбалет, огнестрельное оружие)",
        "Боевые искусства и самооборона", "Химия (изготовление полезных веществ, фильтрация воды)",
        "Физическая подготовка (бег, кроссфит, турники)", "Электроника и пайка",
        "Сбор и очистка воды", "Ориентирование на местности (чтение карт, компас)",
        "Строительство и ремонт зданий", "Психология (управление стрессом, работа в коллективе)",
        "Шахтёрское дело и добыча ресурсов", "Программирование и работа с автоматизированными системами",
        "Живопись и рисование (для морального духа)", "Игры и карточные фокусы (развлечение для группы)",
        "Коллекционирование марок", "Составление гороскопов", "Скоростной сбор кубика Рубика",
        "Просмотр сериалов", "Разгадывание кроссвордов", "Стендап-комедия", "Косплей",
        "Скоростной поедатель еды", "Ведение блога о моде", "Игры на телефон",
        "Плетение браслетов из бисера", "Танцы K-Pop", "Сочинение стихов о любви",
        "Разведение редких пород кошек", "Выставочные соревнования по собакам"
    ],
    'en': [
        "Fishing", "Hunting", "Growing plants (gardening, hydroponics)",
        "Cooking and campfire meals", "Farming and animal husbandry",
        "First aid", "Herbalism (medicinal plants)", "Repairing and fixing equipment",
        "Carpentry", "Blacksmithing", "Handcrafts and sewing", "Making weapons and traps",
        "Shooting (bow, crossbow, firearms)", "Martial arts and self-defense",
        "Chemistry (useful substances, water filtration)", "Physical training (running, calisthenics)",
        "Electronics and soldering", "Water collection and purification",
        "Navigation (maps, compass)", "Construction and building repair",
        "Psychology (stress management, teamwork)", "Mining and resource extraction",
        "Programming and automated systems", "Painting and drawing (morale)",
        "Games and card tricks (group entertainment)",
        "Stamp collecting", "Horoscopes", "Speedcubing",
        "Binge-watching series", "Crosswords", "Stand-up comedy", "Cosplay",
        "Competitive eating", "Fashion blogging", "Mobile gaming",
        "Bead bracelet weaving", "K-Pop dancing", "Writing love poetry",
        "Breeding rare cat breeds", "Dog show competitions"
    ],
}

ITEMS = {
    'ru': [
        "Аптечка первой помощи", "Набор инструментов (молоток, отвертки, плоскогубцы)",
        "Многофункциональный нож", "Спальный мешок и одеяло", "Запас консервированной еды",
        "Фильтр для воды или таблетки для очистки", "Фонарь и запас батареек", "Зажигалки и огниво",
        "Рация или спутниковый телефон", "Верёвка (паракорд)", "Тёплая одежда и обувь",
        "Канистра с чистой водой", "Геологический компас и карта местности",
        "Учебник по медицине и выживанию", "Энергетические батончики и сухпайки",
        "Защитные очки и перчатки", "Генератор или солнечная батарея",
        "Противогаз или респиратор", "Радио с ручным динамо-зарядом",
        "Гигиенические средства (мыло, зубная паста, туалетная бумага)",
        "Набор для шитья и ремонта одежды", "Запасной комплект аккумуляторов",
        "Оружие для самообороны (если разрешено)", "Запас соли, сахара и специй",
        "Небольшая печка или примус", "Коллекция виниловых пластинок", "Глянцевые журналы",
        "Фигурки из комиксов", "Свадебное платье", "Селфи-палка", "Диск с установкой Windows XP",
        "Настольная лампа без электричества", "Плюшевые игрушки", "Книга о моде 2010 года",
        "Топовый геймерский ПК без источника питания", "Старая кассета с музыкой 90-х",
        "Настольная игра без фишек и кубиков", "Диплом о высшем образовании",
        "Плакат любимой музыкальной группы", "Шампунь для окрашенных волос",
        "Флакон дорогих духов", "Годовой запас косметики", "Альбом с фотографиями из отпуска",
        "Набор кисточек для макияжа", "Чековая книжка и кредитная карта"
    ],
    'en': [
        "First aid kit", "Tool set (hammer, screwdrivers, pliers)", "Multitool knife",
        "Sleeping bag and blanket", "Stock of canned food",
        "Water filter or purification tablets", "Flashlight and spare batteries", "Lighters and firesteel",
        "Radio or satellite phone", "Rope (paracord)", "Warm clothing and boots",
        "Canister of clean water", "Compass and map",
        "Survival and medical handbook", "Energy bars and rations",
        "Safety goggles and gloves", "Generator or solar panel",
        "Gas mask or respirator", "Hand-crank radio",
        "Hygiene supplies (soap, toothpaste, toilet paper)", "Sewing and clothing repair kit",
        "Spare battery pack", "Self-defense weapon (where allowed)", "Stock of salt, sugar, spices",
        "Small stove or camping burner", "Vinyl record collection", "Glossy magazines",
        "Comic figurines", "Wedding dress", "Selfie stick", "Windows XP install disc",
        "Desk lamp without electricity", "Plush toys", "Fashion book from 2010",
        "High-end gaming PC without power source", "Old 90s music cassette",
        "Board game without pieces and dice", "University diploma",
        "Poster of favorite band", "Shampoo for dyed hair",
        "Bottle of expensive perfume", "Year-long cosmetics stock",
        "Vacation photo album", "Makeup brush set", "Checkbook and credit card"
    ],
}

CARDS = {
    'ru': [
        "Отменить последнее действие",
        "2 голоса в этом раунде",
        "Взлом информации – Посмотрите любую характеристику другого игрока",
        "Обмен ролями – Поменяйтесь с любым игроком характеристиками",
        "Дуэль – Аргументативный поединок с игроком, победителя выбирают другие",
        "Второе дыхание – Вернуть выбывшего игрока на 1 раунд",
        "Запрет на голосование – Лишить игрока права голосовать в этом раунде",
        "Запрет на разговор – Лишить игрока права говорить в этом раунде",
        "Хаос – Все игроки получают новые профессии",
        "Анархия – Голосуют только номинированные на вылет",
        "Запасной выход – Пропустить одно голосование",
        "Абсурд – Если вылетит игрок справа от вас, в следующем раунде можно говорить только слова на букву 'П'"
    ],
    'en': [
        "Undo the last action",
        "2 votes this round",
        "Info breach – Peek any one characteristic of another player",
        "Role swap – Exchange characteristics with any player",
        "Duel – Argument duel with a player, others choose winner",
        "Second wind – Bring back an eliminated player for 1 round",
        "Voting ban – Remove a player's right to vote this round",
        "Speech ban – Forbid a player from speaking this round",
        "Chaos – All players receive new professions",
        "Anarchy – Only nominated players may vote",
        "Emergency exit – Skip one voting",
        "Absurd – If the player to your right is eliminated, next round you may speak only words starting with 'P'"
    ],
}

def send_language_selection(chat_id: int):
    labels = LABELS['ru']  # подписи на кнопках показываем двуязычно
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(LABELS['ru']['lang_ru'], callback_data='lang_ru'),
        types.InlineKeyboardButton(LABELS['en']['lang_en'], callback_data='lang_en'),
    )
    bot.send_message(chat_id, 'Выберите язык / Choose language:', reply_markup=markup)

def send_characteristics(chat_id: int, lang: str):
    labels = LABELS.get(lang, LABELS['ru'])

    profession_line = f"{labels['profession']}: {profession_generator(lang)}"
    age_line = f"{labels['age']}: {age_generator()}"
    gender_line = f"{labels['gender']}: {gender_generator(lang)}, {apple(lang)}"

    sickness_line = f"{labels['sickness']}: {sickness_generator(lang)}, {sickness_generator_procent()}%"
    phobia_line = f"{labels['phobia']}: {phobia_generator(lang)}"

    hobby_line = f"{labels['hobby']}: {hobby_generator(lang)}"
    item_line = f"{labels['item']}: {item_generator(lang)}"
    card_line = f"{labels['card']}: {card_generator(lang)}"

    bot.send_message(
        chat_id,
        f"{profession_line}\n{age_line}\n{gender_line}\n{sickness_line}\n{phobia_line}\n{hobby_line}\n{item_line}\n{card_line}"
    )

def profession_generator(lang: str = 'ru'):
    return random.choice(PROFESSIONS.get(lang, PROFESSIONS['ru']))

def age_generator():
    return random.randint(9, 70)

def gender_generator(lang: str = 'ru'):
    return random.choice(GENDERS.get(lang, GENDERS['ru']))

def apple(lang: str = 'ru'):
    return random.choice(FERTILITY.get(lang, FERTILITY['ru']))

def sickness_generator(lang: str = 'ru'):
    return random.choice(SICKNESSES.get(lang, SICKNESSES['ru']))
def sickness_generator_procent():
    return random.randint(0, 100)

def phobia_generator(lang: str = 'ru'):
    return random.choice(PHOBIAS.get(lang, PHOBIAS['ru']))

def hobby_generator(lang: str = 'ru'):
    return random.choice(HOBBIES.get(lang, HOBBIES['ru']))

def item_generator(lang: str = 'ru'):
    return random.choice(ITEMS.get(lang, ITEMS['ru']))

def card_generator(lang: str = 'ru'):
    return random.choice(CARDS.get(lang, CARDS['ru']))

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    # Если язык уже выбран — сразу шлём характеристики, иначе предлагаем выбор
    if chat_id in user_lang:
        send_characteristics(chat_id, user_lang[chat_id])
    else:
        send_language_selection(chat_id)

@bot.callback_query_handler(func=lambda c: c.data in ['lang_ru', 'lang_en'])
def on_language_selected(call):
    chat_id = call.message.chat.id
    lang = 'ru' if call.data == 'lang_ru' else 'en'
    user_lang[chat_id] = lang
    # Короткое подтверждение
    bot.answer_callback_query(call.id, '✓')
    bot.send_message(chat_id, LABELS[lang]['lang_set'])
    send_characteristics(chat_id, lang)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text != '/start':
        try:
            with open('leo.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        except FileNotFoundError:
            lang = user_lang.get(message.chat.id, 'ru')
            bot.send_message(message.chat.id, LABELS[lang]['image_not_found'])

# Запускаем цикл опроса сообщений
bot.polling()
