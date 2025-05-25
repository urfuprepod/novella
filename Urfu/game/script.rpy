# Вы можете расположить сценарий своей игры в этом файле.

# Определение персонажей игры.
define e = Character('Эйлин', color="#e0b218")
define i = Character('Илья', color="#50c878")
define v = Character('Ваня', color="#00ffff")
define mc = None
define friend = None
define was_on_departament = False
define british_mark = -1
define do_war = False
define students = {
    '1985': False,
    '1986': False,
    '1987': False
}

default card_amount = 12
default card_rows = 3
default cards = []
default selected_cards = []
default hidden_cards = 0
default match_found = False
default associations = [{'text': 'Наполеон Бонапарт', 'value': 0}, {'text': 'Битве при Аустерлице', 'value': 0}, 
{'text': 'Гебхард Леберехт фон Блюхер', 'value': 1}, {'text': 'Битва при Ватерлоо', 'value': 1}, 
{'text': 'Ян Собеский', 'value': 2}, {'text': 'Битва при Вене', 'value': 2}, 
{'text': 'Сулейман I', 'value': 3}, {'text': 'Битва при Мохаче', 'value': 3},
{'text': 'Вильгельм Завоеватель', 'value': 4}, {'text': 'Битва при Гастингсе', 'value': 4},
# {'text': 'Густав II Адольф', 'value': 5,}, {'text': 'Битва при Брейтенфельде', 'value': 5},
{'text': 'Дмитрий Донской', 'value': 5}, {'text': 'Куликовская битва', 'value': 5}
]

init python:
    import csv
    import random

    def load_people_by_year(year):
        students = []
        with open(renpy.loader.transfn("data/students.csv"), 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                splitted = row[0].split(';')
                if (len(splitted) >= 3):
                    name = splitted[0]
                    student_year = splitted[2]
                    if (year == student_year):
                        students.append(name)
        return students

    def randomize_cards():
        global cards
        cards = []
        cards_top = list(range(int(card_amount / 2))) 
        random.shuffle(cards_top)
        for i in cards_top:
            filtered_list = [el for el in associations if el["value"] == i]
            cards.append([filtered_list[0]['text'], 'deselected', 'visible', i])
            cards.append([filtered_list[1]['text'], 'deselected', 'visible', i])
        renpy.random.shuffle(cards)

    def select_card(card_index):
        global selected_cards
        global match_found

        cards[card_index][1] = 'selected'
        selected_cards.append(card_index)
        if len(selected_cards) == 2 and cards[selected_cards[0]][3] == cards[selected_cards[1]][3]:
            match_found = True
    def deselect_cards():
        global selected_cards
        if len(selected_cards) == 2:
            for card in cards:
                if card[1] == 'selected':
                    card[1] = 'deselected'
        selected_cards = []
    def hide_matches():
        global selected_cards
        global match_found
        global hidden_cards

        cards[selected_cards[0]][2] = 'hidden'
        cards[selected_cards[1]][2] = 'hidden'
        hidden_cards +=2
        deselect_cards()
        match_found = False
    def reset_memory_game():
        global match_found
        global hidden_cards

        match_found = False
        hidden_cards = 0
        randomize_cards()



# Игра начинается здесь

label start:
    stop music
    scene istfuck

    play music "audio/rampart.mp3" loop

    "Исторический факультет Уральского Федерального университета. Знакомые вибрации"

    menu vibrations:
        "Ты улавливаешь их?"
        "Да, я чувствую":
            pass
        "Не понимаю, о чем ты говоришь":
            pass
        

    "Конец мая 2025 года. На истфаке наступает сессия"

    "На 4 этаж поднимается..."

    menu main_character:
        "Выберите главного героя"
        "Выпускник Томского государственного университета":
            $ mc = v
            $ friend = i
        "Выпускник радиофака":
            $ mc = i
            $ friend = v
        
    if mc == i:
        show papich1
        with fade
        mc "Ф5, сегодня же сессия"
    else:
        show vanya1
        with fade
        mc 'Блин, сегодня же начинается сессия'

    mc "На сегодня мне нужно сдать британский парламентаризм, военное искусство..."

    mc "Стоит также сходить на кафедру"
    
    mc "Там может быть что-то интересное"

    menu go:
        "Куда пойти?"
        "Схожу на кафедру":
            jump departament
        "Сдам британский парламентаризм":
            jump britain
        "Сдам военное искусство":
            jump war
    
    stop music
    return

label main:
    scene istfuck
    play music "audio/main.mp3" loop

    if mc == i:
        show papich_scared1
        with fade 
    else:
        show vanya_angry1
        with fade
    mc "Нужно скорее решить вопрос с сегодняшней сессией"
    mc "Чем бы заняться?"

    menu actions:
        "Куда пойти?"
        "Сходить на кафедру":
            jump departament
        "Сдать британский парламентаризм" if british_mark == -1:
            jump britain
        "Сдать военное искусство" if do_war == False:
            jump war
        "Уйти домой" if (british_mark > -1 and all(value is True for value in students.values()) and do_war == True):
            hide papich_scared1
            hide vanya_angry1
            if mc == i:
                show papich_happy1
            else:
                show vanya_happy1
            play music "audio/end.mp3" loop
            mc "Все мои дела сделаны, можно идти домой"
    return

label departament:
    scene departament

    play music 'audio/new.mp3' loop

    if mc == i:
        show papich_happy1
        with fade
    else:
        show vanya_happy1
        with fade
    
    if was_on_departament == False:
        mc "Кафедра новой и новейшей истории"
        mc "На 2 года она должна стать моим родным домом"
    mc "Хм..."
    mc "Можно посмотреть списки выпускников"

    $ was_on_departament = True
    $ renpy.sound.stop() 
    label archive:
        menu students:
            "За какой год будем смотреть списки?"
            "1985 год" if students['1985'] != True:
                mc "1985... год"
                mc "Антиутопия Оруэлла достигла своего апогея, став истфаком УрФУ"
                mc "Давай посмотрим"
                python:
                    chibises = load_people_by_year('1985')
                    chels = [chibises[i:i+4] for i in range(0, len(chibises), 4)]
                    for chel in chels:
                        people_text = "\n".join([p for p in chel])
                        renpy.say(mc, people_text)
                mc "Этот год закончен"
                $ students['1985'] = True
                jump archive
            "1986 год" if students['1986'] != True:
                mc "1986 год..."
                mc "В этом году не было ничего интересного"
                mc "Посмотрим..."
                python:
                    chibises = load_people_by_year('1986')
                    chels = [chibises[i:i+4] for i in range(0, len(chibises), 4)]
                    for chel in chels:
                        people_text = "\n".join([p for p in chel])
                        renpy.say(mc, people_text)
                mc "Этот год закончен"
                $ students['1986'] = True
                jump archive
            "1987 год" if students['1987'] != True:
                mc "1987 год..."
                mc "После него записи обрываются"
                mc "Посмотрим..."
                python:
                    chibises = load_people_by_year('1987')
                    chels = [chibises[i:i+4] for i in range(0, len(chibises), 4)]
                    for chel in chels:
                        people_text = "\n".join([p for p in chel])
                        renpy.say(mc, people_text)
                mc "Этот год закончен"
                $ students['1987'] = True
                jump archive
            "Нет смысла отвлекаться на списки выпускников, надо заняться сессией":
                jump main
        
label britain:
    play music 'audio/sorcesses.mp3' loop
    scene 474

    if mc == i:
        show papich_scared1 at left
        with fade 
    else:
        show vanya_angry1 at left
        with fade

    mc "Контрольная по британскому парламентаризму..."
    mc "Повезло, что в формате теста"
    mc "Если не знаешь правильный ответ, всегда выбирай второй"
    mc "Достаточно ответить на 4 вопроса из 10, чтобы получить зачет"

    if friend == i:
        show papich_happy1 at right
        friend "Мужик, удачи тебе на экзамене"
        hide papich_happy1
    else:
        show vanya_happy1 at right
        friend "Дружище, хорошего тебе экзамена"
        hide vanya_happy1

    hide papich_scared1
    hide vanya_angry1

    $ british_mark = 0
    menu question_1:
        "В советской историографии первым парламентом принято считать парламент, созванный графом Монфором. А в каком году?"
        "1264 год":
            pass
        "1265 год":
            $ british_mark +=1
        "1266 год":
            pass
        "1267 год":
            pass

    menu question_2:
        "В XIV веке короли Англии имели право приглашать в палату лордов своих приближенных не из числа титулованной знати. А как они назывались?"
        "Баннереты":
            $ british_mark +=1
        "Баронеты":
            pass
        "Бояре":
            pass
        "Бомжи":
            pass

    menu question_3:
        "К середина XIV века полный контроль вопроса прямого налогооблажения получила..."
        "Палата общин":
            $ british_mark +=1
        "Палата лордов":
            pass
    menu question_4:
        "Долгое время в парламенте присутствовала практика голосования по доверенности, из-за чего в свое время герцог Бекингем набрал 13 голосов на заседании. В 1626 году это правило решили ограничить - один лорд мог иметь не более ... голосов по доверенности"
        "1":
            pass
        "2":
            $ british_mark +=1
        "3":
            pass
        "4":
            pass
    menu question_5:
        "В 1430-м гг. впервые введен имущественный ценз на выборы в палату общин, право получили фригольдеры с доходом не менее ..."
        "100 шиллингов в год":
            pass
        "3 фунта в год":
            pass
        "40 шиллингов в год":
            $ british_mark += 1
        "3 коровы в год":
            pass

    menu question_6:
        "Во время конфликта короля Карла I Стюарта с парламентом был принят акт, запрещающий роспуск парламента без его согласия. В результате парламент принял решение о самороспуске 16 марта 1660 года, за что получил название долгий. А сколько лет он продержался?"
        "5 лет":
            pass
        "10 лет":
            pass
        "15 лет":
            pass
        "20 лет":
            $ british_mark +=1
    
    menu question_7:
        "Что такое парламент-конвент?"
        "Парламент, созванный без повеления монарха":
            $ british_mark +=1
        "Парламент, на заседании которого победила оппозиция":
            pass
        "Парламент, не принявший никаких законов":
            pass
        "Парламент, собранный не в Вестминстере":
            pass
    menu question_8:
        "Третий акт о присяге 1678 года полностью лишил ИХ возможности заседать в парламенте и занимать государсвтенные должности"
        "Иностранцам":
            pass
        "Католикам":
            $ british_mark +=1
        "Эти, ну как их там...":
            pass
        "Простолюдинам":
            pass
    menu question_9:
        "В каком году женщины впервые получили право избирательного голоса в парламент?"
        "1877 год":
            pass
        "1904 год":
            pass
        "1918 год":
            $ british_mark +=1
        "1927 год":
            pass
    menu question_10:
        "Несмотря на попытки премьер-министра Дэвида Кэмерона изменить ибирательную систему, она всю равно осталось именно ТАКОЙ"
        "Мажоритарной":
            $ british_mark +=1
        "Пропорциональной":
            pass
        "Смешанной":
            pass
        "Парламента к этому времени уже не существовало":
            "Ты че, дурак?"
            pass
    "Вы получили [british_mark]/10 за экзамен"
    if british_mark >= 4:
        "Вы сдали экзамен"
        if mc == i:
            show papich_happy1
            mc "Да-да я" 
        else:
            show vanya_happy1
            "Отлично, экзамен сдан"
    else:
        "Вы не сдали экзамен"
        if mc == i:
            show papich_scared1
            mc "Треш, чел" 
        else:
            show vanya_angry1 at left
            "Не повезло..."
    jump main

transform card_fadein:
    alpha 0.0
    easein 0.5 alpha 1.0

screen memory_mini_game:
    image "game_background.png"
    text "Соотнесите полководцев и их победы" align (0.05, 0.1) color "#000080" size 32
    grid int(card_amount / card_rows) card_rows:
        align(0.9, 0.5)
        spacing 5
        for i, card in enumerate(cards):
            if card[1] == 'deselected' and card[2] == 'visible':
                imagebutton idle 'card_back.png' sensitive If(len(selected_cards) !=2, True, False) action Function(select_card, card_index = i) at card_fadein
            elif card[1] == 'selected' and card[2] == 'visible':
                frame:
                    background "#ffffff"  # Цвет подложки
                    xysize (227, 293)     # Размер карточки (по необходимости)
                    align (0.5, 0.5)
                    text card[0] color "#000" size 32 xalign 0.5 yalign 0.5
            else:
                null
    if match_found:
        timer 1.0 action Function(hide_matches) repeat True
    elif len(selected_cards) == 2:
        timer 1.0 action Function(deselect_cards) repeat True
    elif hidden_cards == card_amount:
        timer 0.5 action Return()
label war:
    play music war
    scene war

    if mc == i:
        show papich_scared1
        with fade 
        mc "Экзаменослав по военному искусству"
        mc "Стыдно признаться, но я пропустил абсолютно все пары"
        mc "Надо как-то выкручиваться..."
        mc "Иначе повторю судьбу бедолаги справа"
    else:
        show vanya_happy1
        with fade
        mc "Что ж"
        mc "Пар по нему было немного"
        mc "Думаю, что экз должен быть простым"
    stop music
    $ randomize_cards()
    play music heart loop
    call screen memory_mini_game
    stop music
    play music 'audio.mp3' loop
    $ do_war = True
    hide papich_scared1
    if mc == i:
        show papich_happy1
        mc "В соло"
    else:
        mc "Изи для меня"
    jump main
    