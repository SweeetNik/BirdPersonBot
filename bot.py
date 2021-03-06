# -*- coding: UTF-8 -*-
import traceback
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
from datetime import datetime
import time
import math
from PIL import Image, ImageDraw, ImageFont

vk_session = vk_api.VkApi(token='fckn token')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# database


bio = [('Литература', 'Штейнбах Анна Евгеньевна'),
       ('Математика', 'Мамий Виктория Владимировна'),
       ('Информатика', 'Лысенко Анна Витальевна'),
       ('Английский', 'Цатурян Мариам Ашотовна'),
       ('Обществознание', 'Петренко Инна Викторовна'),
       ('Экология', 'Мегес Руслан Киримович'),
       ('Физ-ра', 'Рыльщиков Дмитрий Юрьевич'),
       ('ОБЖ', 'Кладова Виктория Владимировна'),
       ('Химия', 'Базык Екатерина Васильевна'),
       ('Русский язык', 'Рыбалко Елена Ивановна'),
       ('Физика', 'Рощина Наталья Элькамовна')
       ]

timetable = [('Понедельник', 'Обществознание(13:10-14:40)-Аудитория 406', 'Обществознание(15:00-16:30)-Аудитория 407',
              'Экология(16:40-18:10)-Аудитория 404', ''),
             ('Вторник(жёл)', 'Литература(13:10-14:40)-Аудитория 503',
              'Физическая культура(15:00-16:30)-Ебурим на стадион',
              'Основы безопасности жизнедеятельности(16:40-18:10)-Аудитория 504', ''),
             ('Вторник(син)', 'Литература(13:10-14:40)-Аудитория 503',
              'Физическая культура(15:00-16:30)-Ебурим на стадион', '', ''),
             ('Среда(жёл)', 'Математика(13:10-14:40)-Аудитория 405', 'Математика(15:00-16:30)-Аудитория 405',
              'Основы безопасности жизнедеятельности(16:40-18:10)-Аудитория 603', ''),
             ('Среда(син)', 'Физическая культура(11:30-13:00)-Ебурим на стадион',
              'Математика(13:10-14:40)-Аудитория 405', 'Математика(15:00-16:30)-Аудитория 405',
              'Основы безопасности жизнедеятельности(16:40-18:10)-Аудитория 603'),
             ('Четверг', 'Русский язык(13:10-14:40)-Аудитория 507',
              'Информатика(15:00-16:30)-Аудитория 311/Иностранный язык(16:40-18:10)-Аудитория 407',
              'Иностранный язык(16:40-18:10)-Аудитория 407/Информатика(15:00-16:30)-Аудитория 311', ''),
             ('Пятница', 'Литература(13:10-14:40)-Аудитория 501', 'Физика(15:00-16:30)-Аудитория 603',
              'Математика(16:40-18:10)-Аудитория 405', ''),
             ('Суббота', 'Математика(13:10-14:40)-Аудитория 405', 'Химия(15:00-16:30)-Аудитория 406',
              'Биология(16:40-18:10)-Аудитория 401', ''),
             ]

bio_pks1 = [('Литература', 'Строцкая Светлана Владимировна'),
            ('Математика', 'Мамий Виктория Владимировна'),
            ('Информатика', 'Перов Андрей Георгиевич'),
            ('Английский', ' Григоревская Анна Сергеевна'),
            ('Обществознание', 'Перетрухин Илья Юрьевич'),
            ('Экология', 'Мегес Руслан Киримович'),
            ('Физ-ра', 'Рыльщиков Дмитрий Юрьевич'),
            ('ОБЖ', 'Кладова Виктория Владимировна'),
            ('Химия', 'Базык Екатерина Васильевна'),
            ('Русский язык', 'Рыбалко Елена Ивановна'),
            ('Физика', 'Рощина Наталья Элькамовна')
            ]

timetable_pks1 = [('Понедельник', 'Экология(13:10-14:40)-Аудитория 404', 'Экология(15:00-16:30)-Аудитория 404',
                   'ОБЖ(16:40-18:10)-Аудитория 401', ''),
                  ('Вторник(жёл)', 'Математика(13:10-14:40)-Аудитория 405',
                   'Математика(15:00-16:30)-405',
                   '', ''),
                  ('Вторник(син)', 'Математика(13:10-14:40)-Аудитория 405',
                   'Математика(15:00-16:30)-405', 'Основы безопасности жизнедеятельности(16:40-18:10)-Аудитория 504',
                   ''),
                  ('Среда(жёл)', 'Физическая культура(11:30-13:00)-Ебурим на стадион',
                   'Химия(13:10-14:40)-Аудитория 404',
                   'Обществознание(15:00-16:30)-Аудитория 506', 'Литература(16:40-18:10)-Аудитория 506'),
                  ('Среда(син)', 'Химия(13:10-14:40)-Аудитория 404',
                   'Обществознание(15:00-16:30)-Аудитория 506', 'Литература(16:40-18:10)-Аудитория 506',
                   ''),
                  ('Четверг', 'Физическая культура(11:30-13:00)-Ебурим на стадион',
                   'Информатика(13:10-14:40)-Аудитория 308/Иностранный язык(15:00-16:30)-Аудитория 404',
                   'Иностранный язык(13:10-14:40)-Аудитория 311/Информатика(15:00-16:30)-Аудитория 308', ''),
                  ('Пятница', 'Математика(11:30-13:00)-Аудитория 405', 'Физика(13:10-14:40)-Аудитория 405',
                   'Математика(15:00-16:30)-Аудитория 405', ''),
                  ('Суббота', 'Обществознание(8:00-9:30)-Актовый зал', 'Литература(9:40-11:10)-Актовый зал',
                   'Русский язык(11:30-13:00)-Актовый зал', ''),
                  ]

bio_pks3 = [('Литература', 'Строцкая Светлана Владимировна'),
            ('Математика', 'Мамий Виктория Владимировна'),
            ('Информатика', 'Перов Андрей Георгиевич'),
            ('Английский', 'Не располагаю данной информацией'),
            ('Обществознание', 'Кравцова Е. В.'),
            ('Экология', 'Отришко Марина Павловна'),
            ('Физ-ра', 'Не располагаю данной информацией'),
            ('ОБЖ', 'Кладова Виктория Владимировна'),
            ('Химия', 'Новоселецкая (не помню, как зовут)'),
            ('Русский язык', 'Строцкая Светлана Владимировна'),
            ('Физика', 'Не располагаю данной информацией')
            ]

timetable_pks3 = [('Понедельник', 'ОБЖ(8:00-9:30)-Аудитория 603',
                   'Информатика(9:40-11:10)-Аудитория 308/Иностранный язык(11:30-13:00)-Актовый зал',
                   'Иностранный язык(9:40-11:10)-Актовый зал/Информатика(11:30-13:00)-Аудитория 308', ''),
                  ('Вторник', 'Химия(8:00-9:30)-Аудитория 406',
                   'Общество(9:40-11:10)-404',
                   'Математика(11:30-13:00)-Аудитория 405', ''),
                  ('Среда(жёл)', 'Экология(8:00-9:30)-Аудитория 503',
                   'Литература(9:40-11:10)-Аудитория 507',
                   'ОБЖ(11:30-13:00)-Аудитория 603', ''),
                  ('Среда(син)', 'Экология(8:00-9:30)-Аудитория 503',
                   'Литература(9:40-11:10)-Аудитория 507',
                   'Физ-ра(11:30-13:00)-Ебурим на стадион', ''),
                  ('Четверг', 'Математика(8:00-9:30)-405',
                   'Математика(9:40-11:10)-Аудитория 405',
                   'Физ-ра(11:30-13:00)-Ебурим на стадион', ''),
                  ('Пятница', 'Общество(8:00-9:30)-Аудитория 406', 'Русский(9:40-11:10)-Аудитория 506',
                   'Литература(11:30-13:00)-Аудитория 506', ''),
                  ('Суббота', 'Экология(8:00-9:30)-Аудитория 506', 'Математика(9:40-11:10)-Аудитория 405',
                   'Физика(11:30-13:00)-Аудитория 404', ''),
                  ]

bio_pks4 = [('Литература', 'Штейнбах Анна Евгеньевна'),
            ('Математика', 'Качанова Ирина Александровна'),
            ('Информатика', 'Не располагаю данной информацией'),
            ('Английский', 'Не располагаю данной информацией'),
            ('Обществознание', 'Норкина Нелли Владимировна'),
            ('Экология', 'Отришко Марина Павловна'),
            ('Физ-ра', 'Не располагаю данной информацией'),
            ('ОБЖ', 'Кладова Виктория Владимировна'),
            ('Химия', 'Базык Екатерина Васильевна'),
            ('Русский язык', 'Рыбалко Елена Ивановна'),
            ('Физика', 'Рощина Наталья Элькамовна')
            ]

timetable_pks4 = [('Понедельник', 'Физика(8:00-9:30)-Аудитория 404', 'Математика(9:40-11:10)-Аудитория 403',
                   'Математика(9:40-11:10)-Аудитория 403', ''),
                  ('Вторник(син)', 'Общество(8:00-9:30)-Аудитория 404',
                   'Литература(9:40-11:10)-507',
                   'ОБЖ(11:30-13:00)-Аудитория 504', ''),
                  ('Вторник(жёл)', 'Общество(8:00-9:30)-Аудитория 404',
                   'Литература(9:40-11:10)-507',
                   'Физ-ра(11:30-13:00)-Аудитория 504', ''),
                  ('Среда', 'Обществознание(8:00-9:30)-Аудитория 504',
                   'Информатика(9:40-11:10)-Аудитория 308/Иностранный язык(11:30-13:00)-Аудитория 403',
                   'Иностранный язык(9:40-11:10)-Актовый зал/Информатика(11:30-13:00)-Аудитория 308', ''),
                  ('Четверг', 'ОБЖ(8:00-9:30)-603',
                   'Литература(9:40-11:10)-Аудитория 503',
                   'Русский язык(11:30-13:00)-Аудитория 507', ''),
                  ('Пятница', 'Математика(8:00-9:30)-Аудитория 401', 'Математика(9:40-11:10)-Аудитория 401',
                   'Химия(11:30-13:00)-Аудитория 404', ''),
                  ('Суббота', 'Экология(8:00-9:30)-Аудитория 603', 'Экология(9:40-11:10)-Актовый зал',
                   'Физ-ра(11:30-13:00)-Ебурим на стадион', ''),
                  ]


# cursor.executemany("INSERT INTO teachers_pks_1 VALUES (?,?)", bio_pks1)
# cursor.executemany("INSERT INTO timetable_pks_1 VALUES (?,?,?,?,?)", timetable_pks1)


# end of database --------------

# Functions of weekdays
def timetables():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 7:
        vk.messages.send(
            user_id=event.user_id,
            message="Сегодня ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        monday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 2:
        if week == 1:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Вторник(син)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            tuesday_y = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Вторник(жёл)'")
            tuesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 3:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 4:
        thursday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        friday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 6:
        saturday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def timetables_t():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 6:
        vk.messages.send(
            user_id=event.user_id,
            message="Завтра ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 7:
        monday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        if week == 1:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Вторник(син)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            tuesday_y = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Вторник(жёл)'")
            tuesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 2:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 3:
        thursday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 4:
        friday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        saturday = cursor.execute("SELECT * FROM timetable_pks_2 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def teachers():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.from_user:
                if not event.text:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                elif event.text == "Литература":
                    liter = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Литература'")
                    liter = liter.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(liter),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Информатика":
                    infor = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Информатика'")
                    infor = infor.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(infor),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Математика":
                    matem = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Математика'")
                    matem = matem.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(matem),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Английский":
                    angel = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Английский'")
                    angel = angel.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(angel),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Обществознание":
                    obsh = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Обществознание'")
                    obsh = obsh.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obsh),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Экология":
                    ecol = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Экология'")
                    ecol = ecol.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(ecol),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физ-ра":
                    fizra = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Физ-ра'")
                    fizra = fizra.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizra),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "ОБЖ":
                    obz = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='ОБЖ'")
                    obz = obz.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obz),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физика":
                    fizika = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Физика'")
                    fizika = fizika.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizika),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Русский":
                    russk = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Русский язык'")
                    russk = russk.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(russk),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Химия":
                    hell = cursor.execute("SELECT name FROM teachers_pks_2 WHERE subject ='Химия'")
                    hell = hell.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(hell),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break


def timetables_pks_1():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 7:
        vk.messages.send(
            user_id=event.user_id,
            message="Сегодня ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        monday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 2:
        if week == 1:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Вторник(син)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            tuesday_y = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Вторник(жёл)'")
            tuesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 3:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 4:
        thursday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        friday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 6:
        saturday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def timetables_t_pks_1():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 6:
        vk.messages.send(
            user_id=event.user_id,
            message="Завтра ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 7:
        monday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        if week == 1:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Вторник(син)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            tuesday_y = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Вторник(жёл)'")
            tuesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 2:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 3:
        thursday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 4:
        friday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        saturday = cursor.execute("SELECT * FROM timetable_pks_1 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def teachers_pks_1():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.from_user:
                if not event.text:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                elif event.text == "Литература":
                    liter = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Литература'")
                    liter = liter.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(liter),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Информатика":
                    infor = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Информатика'")
                    infor = infor.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(infor),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Математика":
                    matem = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Математика'")
                    matem = matem.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(matem),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Английский":
                    angel = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Английский'")
                    angel = angel.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(angel),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Обществознание":
                    obsh = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Обществознание'")
                    obsh = obsh.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obsh),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Экология":
                    ecol = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Экология'")
                    ecol = ecol.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(ecol),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физ-ра":
                    fizra = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Физ-ра'")
                    fizra = fizra.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizra),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "ОБЖ":
                    obz = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='ОБЖ'")
                    obz = obz.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obz),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физика":
                    fizika = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Физика'")
                    fizika = fizika.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizika),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Русский":
                    russk = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Русский язык'")
                    russk = russk.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(russk),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Химия":
                    hell = cursor.execute("SELECT name FROM teachers_pks_1 WHERE subject ='Химия'")
                    hell = hell.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(hell),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break


def timetables_pks_3():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 7:
        vk.messages.send(
            user_id=event.user_id,
            message="Сегодня ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        monday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 2:
        tuesday_b = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Вторник'")
        tuesday_b = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(tuesday_b)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 3:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 4:
        thursday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        friday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 6:
        saturday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def timetables_t_pks_3():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 6:
        vk.messages.send(
            user_id=event.user_id,
            message="Завтра ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 7:
        monday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        tuesday_b = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Вторник'")
        tuesday_b = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(tuesday_b)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )
    elif a == 2:
        if week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Среда(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            wednesday_y = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Среда(жёл)'")
            wednesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 3:
        thursday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 4:
        friday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        saturday = cursor.execute("SELECT * FROM timetable_pks_3 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def teachers_pks_3():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.from_user:
                if not event.text:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                elif event.text == "Литература":
                    liter = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Литература'")
                    liter = liter.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(liter),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Информатика":
                    infor = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Информатика'")
                    infor = infor.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(infor),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Математика":
                    matem = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Математика'")
                    matem = matem.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(matem),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Английский":
                    angel = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Английский'")
                    angel = angel.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(angel),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Обществознание":
                    obsh = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Обществознание'")
                    obsh = obsh.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obsh),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Экология":
                    ecol = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Экология'")
                    ecol = ecol.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(ecol),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физ-ра":
                    fizra = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Физ-ра'")
                    fizra = fizra.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizra),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "ОБЖ":
                    obz = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='ОБЖ'")
                    obz = obz.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obz),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физика":
                    fizika = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Физика'")
                    fizika = fizika.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizika),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Русский":
                    russk = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Русский язык'")
                    russk = russk.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(russk),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Химия":
                    hell = cursor.execute("SELECT name FROM teachers_pks_3 WHERE subject ='Химия'")
                    hell = hell.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(hell),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break


def timetables_pks_4():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 7:
        vk.messages.send(
            user_id=event.user_id,
            message="Сегодня ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        monday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 2:
        if week == 0:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Вторник(жёл)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 1:
            wednesday_b = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Вторник(син)'")
            wednesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(wednesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
    elif a == 3:
        wednesday_y = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Среда'")
        wednesday_y = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(wednesday_y)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 4:
        thursday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        friday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 6:
        saturday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def timetables_t_pks_4():
    week = int(datetime.now().strftime("%V")) % 2  # 1 == blue, 0 == yellow
    b = datetime.now()
    a = datetime.isoweekday(b)
    if a == 6:
        vk.messages.send(
            user_id=event.user_id,
            message="Завтра ВОСКРЕСЕНЬЕ, бро",
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 7:
        monday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Понедельник'")
        monday = monday.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(monday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 1:
        if week == 1:
            tuesday_b = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Вторник(син)'")
            tuesday_b = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_b)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )
        elif week == 0:
            tuesday_y = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Вторник(жёл)'")
            tuesday_y = cursor.fetchone()
            vk.messages.send(
                user_id=event.user_id,
                message=('\n'.join(tuesday_y)),
                random_id=randint(1, 1000000000000000000000000000000000),
                keyboard=keyboard.get_keyboard()
            )

    elif a == 2:
        wednesday_b = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Среда'")
        wednesday_b = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(wednesday_b)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 3:
        thursday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Четверг'")
        thursday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(thursday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 4:
        friday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Пятница'")
        friday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(friday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )

    elif a == 5:
        saturday = cursor.execute("SELECT * FROM timetable_pks_4 WHERE day ='Суббота'")
        saturday = cursor.fetchone()
        vk.messages.send(
            user_id=event.user_id,
            message=('\n'.join(saturday)),
            random_id=randint(1, 1000000000000000000000000000000000),
            keyboard=keyboard.get_keyboard()
        )


def teachers_pks_4():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.from_user:
                if not event.text:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                elif event.text == "Литература":
                    liter = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Литература'")
                    liter = liter.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(liter),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Информатика":
                    infor = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Информатика'")
                    infor = infor.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(infor),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Математика":
                    matem = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Математика'")
                    matem = matem.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(matem),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Английский":
                    angel = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Английский'")
                    angel = angel.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(angel),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Обществознание":
                    obsh = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Обществознание'")
                    obsh = obsh.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obsh),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Экология":
                    ecol = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Экология'")
                    ecol = ecol.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(ecol),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физ-ра":
                    fizra = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Физ-ра'")
                    fizra = fizra.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizra),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "ОБЖ":
                    obz = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='ОБЖ'")
                    obz = obz.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(obz),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Физика":
                    fizika = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Физика'")
                    fizika = fizika.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(fizika),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Русский":
                    russk = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Русский язык'")
                    russk = russk.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(russk),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                elif event.text == "Химия":
                    hell = cursor.execute("SELECT name FROM teachers_pks_4 WHERE subject ='Химия'")
                    hell = hell.fetchone()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=''.join(hell),
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                        random_id=randint(1, 1000000000000000000000000000000000),
                        keyboard=keyboard.get_keyboard()
                    )
                    break


def left():
    global x, y, manl, manr, z, g, num
    manl = man_pars[x:y]
    image1 = Image.open("tet.jpg")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("arial.ttf", size=39)
    draw.text((10, 5), manl, fill=(0, 33, 55), font=font)
    num += 1
    image1.save("img" + str(num) + ".jpg")
    x = y
    y += 1260
    manr = man_pars[x:y]
    if manr == str(''):
        print("Текста больше нет")
    else:
        print('Тут был текст')
        right()


def right():
    global x, y, manl, manr, z, g, num
    image1 = Image.open("tetrev.jpg")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("arial.ttf", size=39)
    draw.text((160, 5), manr, fill=(0, 33, 55), font=font)
    num += 1
    image1.save("img" + str(num) + ".jpg")
    x = y
    y += 1260
    manl = man_pars[x:y]
    if manl == str(''):
        print("Текста больше нет")
    else:
        print('Тут был текст')
        left()


def pars():
    global z, g, mann, lines
    while lines > 1:
        if str(man[z]) == ' ':
            mann += man[g:z] + str(" ") + "\n\n"
            z += 60
            g += 60
        elif str(man[z]) != ' ':
            mann += man[g:z] + str("-") + "\n\n"
            z += 60
            g += 60
        lines = lines - 1
    if cnt - g < 60:
        mann += man[g:]
    else:
        mann += man[g:z] + str("-") + "\n\n" + man[z:]
    return mann
    return mann


def left1():
    global x, y, manl, manr, z, g, num
    manl = man_pars[x:y]
    image1 = Image.open("tet1.jpg")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("eskal.ttf", size=25)
    draw.text((50, 15), manl, fill=(0, 33, 55), font=font)
    num += 1
    image1.save("img" + str(num) + ".jpg")
    x = y
    y += 1472
    manr = man_pars[x:y]
    if manr == str(''):
        print("Текста больше нет")
    else:
        print('Тут был текст')
        right1()


def right1():
    global x, y, manl, manr, z, g, num
    image1 = Image.open("tetrev1.jpg")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype("eskal.ttf", size=25)
    draw.text((85, 15), manr, fill=(0, 33, 55), font=font)
    num += 1
    image1.save("img" + str(num) + ".jpg")
    x = y
    y += 1472
    manl = man_pars[x:y]
    if manl == str(''):
        print("Текста больше нет")
    else:
        print('Тут был текст')
        left1()


def pars1():
    global z, g, mann, lines
    while lines > 1:
        if str(man[z]) == ' ':
            mann += man[g:z] + str(" ") + "\n\n"
            z += 64
            g += 64
        elif str(man[z]) != ' ':
            mann += man[g:z] + str("-") + "\n\n"
            z += 64
            g += 64
        lines = lines - 1
    if cnt - g < 64:
        mann += man[g:]
    else:
        mann += man[g:z] + str("-") + "\n\n" + man[z:]
    return mann



# Keyboard first

keyboard = VkKeyboard(one_time=False)
keyboard.add_button("Расписание на сегодня", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Расписание на завтра", color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button("Important", color=VkKeyboardColor.NEGATIVE)
keyboard.add_button("Узнать ФИО препода", color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()
keyboard.add_button("Материальная поддержка", color=VkKeyboardColor.PRIMARY)
keyboard.add_button("Сделать конспект", color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button("Сменить специальность", color=VkKeyboardColor.DEFAULT)

# Keyboard second

keyboards = VkKeyboard(one_time=True)
keyboards.add_button("ПКС-1", color=VkKeyboardColor.POSITIVE)
keyboards.add_button("ПКС-2", color=VkKeyboardColor.POSITIVE)
keyboards.add_line()
keyboards.add_button("ПКС-3", color=VkKeyboardColor.PRIMARY)
keyboards.add_button("ПКС-4", color=VkKeyboardColor.PRIMARY)

# keyboard third

keyboarddon = VkKeyboard(one_time=False)
keyboarddon.add_vkpay_button(hash="action=transfer-to-group&group_id=190666803")
keyboarddon.add_line()
keyboarddon.add_button("Назад", color=VkKeyboardColor.POSITIVE)

# keyboard fourth

keyboardteach = VkKeyboard(one_time=True)
keyboardteach.add_button("Литература", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_button("Информатика", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_line()
keyboardteach.add_button("Математика", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_button("Английский", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_line()
keyboardteach.add_button("Обществознание", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_button("Экология", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_line()
keyboardteach.add_button("Физ-ра", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_button("ОБЖ", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_line()
keyboardteach.add_button("Физика", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_button("Русский", color=VkKeyboardColor.PRIMARY)
keyboardteach.add_line()
keyboardteach.add_button("Химия", color=VkKeyboardColor.NEGATIVE)

# keyboard fifth

keyboardess = VkKeyboard(one_time=True)
keyboardess.add_button("1", color=VkKeyboardColor.DEFAULT)
keyboardess.add_button("2", color=VkKeyboardColor.DEFAULT)

# keyboard sixth

keyboardback = VkKeyboard(one_time=True)
keyboardback.add_button("Вернуться", color=VkKeyboardColor.POSITIVE)

print("Bot has been started")

while True:
    try:
        conn = sqlite3.connect("database/employee.db")
        cursor = conn.cursor()
        #        cursor.execute("""CREATE TABLE teachers_pks_4
        #        (subject text, name text
        #                      )
        #                    """)
        #
        #        cursor.execute("""CREATE TABLE timetable_pks_4
        #        (day text, subject_1 text, subject_2 text, subject_3 text, subject_4 text
        #                         )
        #                      """)
        #        cursor.executemany("INSERT INTO teachers_pks_4 VALUES (?,?)", bio_pks4)
        #        cursor.executemany("INSERT INTO timetable_pks_4 VALUES (?,?,?,?,?)", timetable_pks4)
        conn.commit()
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.from_user:
                    if not event.text:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                            random_id=randint(1, 1000000000000000000000000000000000),
                            keyboard=keyboard.get_keyboard()
                        )
                        break
                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                            random_id=randint(1, 1000000000000000000000000000000000),
                            keyboard=keyboards.get_keyboard()
                        )
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                if event.from_user:
                                    if event.text == "ПКС-1":
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Привет, студент из ПКС-1",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboard.get_keyboard()
                                        )
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                if event.from_user:
                                                    if not event.text:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Сменить специальность":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Будет по-твоему",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    elif event.text == "Расписание на сегодня":
                                                        timetables_pks_1()
                                                    elif event.text == "Расписание на завтра":
                                                        timetables_t_pks_1()
                                                    elif event.text == "Important":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Директор ИНСПО - Хлопова Татьяна Павловна (305 кабинет)\nЗаместитель директора – Рыбалко Елена Ивановна.\nНомер телефона : +7-861-267-22-80\nEmail: inspo@inspo.kubsu.ru\nИнформация взята с сайта www.kubsu.ru\nПолное расписание прилетит через пару секунд :)",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        photo = open('first.jpg', 'rb')
                                                        photo2 = open('second.jpg', 'rb')
                                                        method = vk_session.method("photos.getMessagesUploadServer")
                                                        request = requests.post(method['upload_url'],
                                                                                files={'photo': photo}).json()
                                                        uploadImage = vk_session.method('photos.saveMessagesPhoto',
                                                                                        {'photo': request['photo'],
                                                                                         'server': request['server'],
                                                                                         'hash': request['hash']})[0]
                                                        request2 = requests.post(method['upload_url'],
                                                                                 files={'photo': photo2}).json()
                                                        uploadImage2 = vk_session.method('photos.saveMessagesPhoto',
                                                                                         {'photo': request2['photo'],
                                                                                          'server': request2['server'],
                                                                                          'hash': request2['hash']})[0]
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="1 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="2 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage2["owner_id"]}_{uploadImage2["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Узнать ФИО препода":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Внимание! Имена являются вымышленными.\nВсе совпадения с реальными именами сотрудников учебного заведения или иными физическими лицами случайны!\nАвтор данного паблика не несёт ответственности за любые последствия от тех или иных совпадений.",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardteach.get_keyboard()
                                                        )
                                                        teachers_pks_1()
                                                    elif event.text == "Материальная поддержка":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Программисту заплатите\nЧеканой монетой...\nP.S. на Detroit: Become Human",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboarddon.get_keyboard()
                                                        )
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if not event.text:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                    elif event.text == "Назад":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                    elif event.text == "Сделать конспект":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Сделай выбор",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardess.get_keyboard()
                                                        )
                                                        zalupa = 1
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if event.text == '1':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == '2':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left1()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == "Вернуться":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Нажми \"Вернуться\", чтобы вернуться ",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboardback.get_keyboard()
                                                                        )
                                                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                    else:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                    elif event.text == "ПКС-2":
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Привет, студент из ПКС-2",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboard.get_keyboard()
                                        )
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                if event.from_user:
                                                    if not event.text:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Сменить специальность":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Будет по-твоему",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    elif event.text == "Расписание на сегодня":
                                                        timetables()
                                                    elif event.text == "Расписание на завтра":
                                                        timetables_t()
                                                    elif event.text == "Important":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Директор ИНСПО - Хлопова Татьяна Павловна (305 кабинет)\nЗаместитель директора – Рыбалко Елена Ивановна.\nНомер телефона : +7-861-267-22-80\nEmail: inspo@inspo.kubsu.ru\nИнформация взята с сайта www.kubsu.ru\nПолное расписание прилетит через пару секунд :)",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        photo = open('first.jpg', 'rb')
                                                        photo2 = open('second.jpg', 'rb')
                                                        method = vk_session.method("photos.getMessagesUploadServer")
                                                        request = requests.post(method['upload_url'],
                                                                                files={'photo': photo}).json()
                                                        uploadImage = vk_session.method('photos.saveMessagesPhoto',
                                                                                        {'photo': request['photo'],
                                                                                         'server': request['server'],
                                                                                         'hash': request['hash']})[0]
                                                        request2 = requests.post(method['upload_url'],
                                                                                 files={'photo': photo2}).json()
                                                        uploadImage2 = vk_session.method('photos.saveMessagesPhoto',
                                                                                         {'photo': request2['photo'],
                                                                                          'server': request2['server'],
                                                                                          'hash': request2['hash']})[0]
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="1 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="2 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage2["owner_id"]}_{uploadImage2["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Узнать ФИО препода":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Внимание! Имена являются вымышленными.\nВсе совпадения с реальными именами сотрудников учебного заведения или иными физическими лицами случайны!\nАвтор данного паблика не несёт ответственности за любые последствия от тех или иных совпадений.",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardteach.get_keyboard()
                                                        )
                                                        teachers()
                                                    elif event.text == "Материальная поддержка":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Программисту заплатите\nЧеканой монетой...\nP.S. на Detroit: Become Human",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboarddon.get_keyboard()
                                                        )
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if not event.text:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                    if event.text == "Назад":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                    elif event.text == "Сделать конспект":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Сделай выбор",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardess.get_keyboard()
                                                        )
                                                        zalupa = 1
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if event.text == '1':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == '2':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left1()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == "Вернуться":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Нажми \"Вернуться\", чтобы вернуться ",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboardback.get_keyboard()
                                                                        )

                                                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    else:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                    elif event.text == "ПКС-3":
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Привет, студент из ПКС-3",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboard.get_keyboard()
                                        )
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                if event.from_user:
                                                    if not event.text:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Сменить специальность":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Будет по-твоему",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    elif event.text == "Расписание на сегодня":
                                                        timetables_pks_3()
                                                    elif event.text == "Расписание на завтра":
                                                        timetables_t_pks_3()
                                                    elif event.text == "Important":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Директор ИНСПО - Хлопова Татьяна Павловна (305 кабинет)\nЗаместитель директора – Рыбалко Елена Ивановна.\nНомер телефона : +7-861-267-22-80\nEmail: inspo@inspo.kubsu.ru\nИнформация взята с сайта www.kubsu.ru\nПолное расписание прилетит через пару секунд :)",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        photo = open('first.jpg', 'rb')
                                                        photo2 = open('second.jpg', 'rb')
                                                        method = vk_session.method("photos.getMessagesUploadServer")
                                                        request = requests.post(method['upload_url'],
                                                                                files={'photo': photo}).json()
                                                        uploadImage = vk_session.method('photos.saveMessagesPhoto',
                                                                                        {'photo': request['photo'],
                                                                                         'server': request['server'],
                                                                                         'hash': request['hash']})[0]
                                                        request2 = requests.post(method['upload_url'],
                                                                                 files={'photo': photo2}).json()
                                                        uploadImage2 = vk_session.method('photos.saveMessagesPhoto',
                                                                                         {'photo': request2['photo'],
                                                                                          'server': request2['server'],
                                                                                          'hash': request2['hash']})[0]
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="1 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="2 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage2["owner_id"]}_{uploadImage2["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Узнать ФИО препода":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Внимание! Имена являются вымышленными.\nВсе совпадения с реальными именами сотрудников учебного заведения или иными физическими лицами случайны!\nАвтор данного паблика не несёт ответственности за любые последствия от тех или иных совпадений.",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardteach.get_keyboard()
                                                        )
                                                        teachers_pks_3()
                                                    elif event.text == "Материальная поддержка":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Программисту заплатите\nЧеканой монетой...\nP.S. на Detroit: Become Human",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboarddon.get_keyboard()
                                                        )
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if not event.text:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                    if event.text == "Назад":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboarddon.get_keyboard()
                                                                        )
                                                    elif event.text == "Сделать конспект":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Сделай выбор",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardess.get_keyboard()
                                                        )
                                                        zalupa = 1
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if event.text == '1':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == '2':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left1()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == "Вернуться":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Нажми \"Вернуться\", чтобы вернуться ",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboardback.get_keyboard()
                                                                        )
                                                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    else:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                    elif event.text == "ПКС-4":
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Привет, студент из ПКС-4",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboard.get_keyboard()
                                        )
                                        for event in longpoll.listen():
                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                if event.from_user:
                                                    if not event.text:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Сменить специальность":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Будет по-твоему",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    elif event.text == "Расписание на сегодня":
                                                        timetables_pks_4()
                                                    elif event.text == "Расписание на завтра":
                                                        timetables_t_pks_4()
                                                    elif event.text == "Important":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Директор ИНСПО - Хлопова Татьяна Павловна (305 кабинет)\nЗаместитель директора – Рыбалко Елена Ивановна.\nНомер телефона : +7-861-267-22-80\nEmail: inspo@inspo.kubsu.ru\nИнформация взята с сайта www.kubsu.ru\nПолное расписание прилетит через пару секунд :)",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        photo = open('first.jpg', 'rb')
                                                        photo2 = open('second.jpg', 'rb')
                                                        method = vk_session.method("photos.getMessagesUploadServer")
                                                        request = requests.post(method['upload_url'],
                                                                                files={'photo': photo}).json()
                                                        uploadImage = vk_session.method('photos.saveMessagesPhoto',
                                                                                        {'photo': request['photo'],
                                                                                         'server': request['server'],
                                                                                         'hash': request['hash']})[0]
                                                        request2 = requests.post(method['upload_url'],
                                                                                 files={'photo': photo2}).json()
                                                        uploadImage2 = vk_session.method('photos.saveMessagesPhoto',
                                                                                         {'photo': request2['photo'],
                                                                                          'server': request2['server'],
                                                                                          'hash': request2['hash']})[0]
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="1 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="2 смена:",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            attachment=f'photo{uploadImage2["owner_id"]}_{uploadImage2["id"]}',
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                                    elif event.text == "Узнать ФИО препода":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Внимание! Имена являются вымышленными.\nВсе совпадения с реальными именами сотрудников учебного заведения или иными физическими лицами случайны!\nАвтор данного паблика не несёт ответственности за любые последствия от тех или иных совпадений.",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardteach.get_keyboard()
                                                        )
                                                        teachers_pks_4()
                                                    elif event.text == "Материальная поддержка":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Программисту заплатите\nЧеканой монетой...\nP.S. на Detroit: Become Human",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboarddon.get_keyboard()
                                                        )
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if not event.text:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                    if event.text == "Назад":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboarddon.get_keyboard()
                                                                        )
                                                    elif event.text == "Сделать конспект":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Сделай выбор",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboardess.get_keyboard()
                                                        )
                                                        zalupa = 1
                                                        for event in longpoll.listen():
                                                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                                                if event.from_user:
                                                                    if event.text == '1':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == '2':
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Давай текст, который нужно законспектировать",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000)
                                                                        )
                                                                        while zalupa == 1:
                                                                            for event in longpoll.listen():
                                                                                if event.type == VkEventType.MESSAGE_NEW and event.to_me and zalupa == 1:
                                                                                    zalupa -= 1
                                                                                    if event.from_user:
                                                                                        if isinstance(event.text, str):
                                                                                            man = event.text
                                                                                            num = 0
                                                                                            g = 0
                                                                                            z = 60
                                                                                            x = 0
                                                                                            y = 1260
                                                                                            manr = str("")
                                                                                            manl = str("")
                                                                                            cnt = len(man)
                                                                                            lines = round(cnt / z)
                                                                                            mann = str("")
                                                                                            lastline = round(math.fabs(
                                                                                                (z * lines) - cnt))
                                                                                            if lastline >= 59:
                                                                                                lines += 1
                                                                                            man_pars = pars()
                                                                                            left1()
                                                                                            print(manl)

                                                                                            # Загружаем картинку на сервер и кидаем в грязную личку
                                                                                            while num > 0:
                                                                                                photo = open("img" + str(
                                                                                                    num) + ".jpg",
                                                                                                             'rb')
                                                                                                method = vk_session.method(
                                                                                                    "photos.getMessagesUploadServer")
                                                                                                request = requests.post(
                                                                                                    method['upload_url'],
                                                                                                    files={
                                                                                                        'photo': photo}).json()
                                                                                                uploadImage = \
                                                                                                vk_session.method(
                                                                                                    'photos.saveMessagesPhoto',
                                                                                                    {'photo': request[
                                                                                                        'photo'],
                                                                                                     'server': request[
                                                                                                         'server'],
                                                                                                     'hash': request[
                                                                                                         'hash']})[0]
                                                                                                vk.messages.send(
                                                                                                    user_id=event.user_id,
                                                                                                    message=str(
                                                                                                        num) + " фото",
                                                                                                    random_id=randint(1,
                                                                                                                      1000000000000000000000000000000000),
                                                                                                    attachment=f'photo{uploadImage["owner_id"]}_{uploadImage["id"]}',
                                                                                                    keyboard=keyboardback.get_keyboard()
                                                                                                )
                                                                                                num -= 1
                                                                                        else:
                                                                                            break
                                                                                else:
                                                                                    break
                                                                    elif event.text == "Вернуться":
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Всегда пожалуйста :)",
                                                                            random_id=randint(1,
                                                                                              100000000000000000000000000000000),
                                                                            keyboard=keyboard.get_keyboard()
                                                                        )
                                                                        break
                                                                    else:
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message="Нажми \"Вернуться\", чтобы вернуться ",
                                                                            random_id=randint(1,
                                                                                              1000000000000000000000000000000000),
                                                                            keyboard=keyboardback.get_keyboard()
                                                                        )
                                                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboards.get_keyboard()
                                                        )
                                                        break
                                                    else:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                                            random_id=randint(1, 1000000000000000000000000000000000),
                                                            keyboard=keyboard.get_keyboard()
                                                        )
                                    elif event.text.lower() == "start" or event.text.lower() == "начать" or event.text.lower() == "restart" or event.text.lower() == "update" or event.text.lower() == "обновить":
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Привет, Я - Птичья Личность, шпион, закрепленный за ИНСПО.\nЧтобы начать пользоваться мной, выбери свою специальность. Также, советую подписаться на рассылку, чтобы не пропускать никаких новостей\nhttps://vk.com/app5898182_-190666803#s=721649",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboards.get_keyboard()
                                        )
                                        break
                                    elif not event.text:
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message='Извините, ваше сообщение не распознано. Пожалуйста, используйте инструкции от бота или кнопки в меню\nЕсли подозреваете, что я сломался, то просто напишите в чат "Обновить"',
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboard.get_keyboard()
                                        )
                                    else:
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                                            random_id=randint(1, 1000000000000000000000000000000000),
                                            keyboard=keyboards.get_keyboard()
                                        )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message="Моя твоя не понимать...\nЕсли подозреваете, что я сломался, то просто напишите в чат 'Обновить'",
                            random_id=randint(1, 1000000000000000000000000000000000),
                        )
        conn.close()
    # THE END ------------------------------------------------------
    except Exception as E:
        print(traceback.format_exc())
        time.sleep(3)
