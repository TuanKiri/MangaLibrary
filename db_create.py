import os
from app import create_app, db
from app.models import User, Manga, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

app_ctx = app.app_context()
app_ctx.push()
db.create_all()
Role.insert_roles()

user1 = User(email="admin@mail.ru", password="password", username="Человек в пакете", name="Артём")
user2 = User(email="artem@mail.ru", password="123", username="Haruko_Koike", name="██████")
user3 = User(email="roma@mail.ru", password="456", username="Te7Ro", name="Roma")
user4 = User(email="denis@mail.ru", password="789", username="Булочка♥", name="Никита")
user5 = User(email="dima@mail.ru", password="987", username="троеточие", name="Irana")
user6 = User(email="anna@mail.ru", password="anna", username="One03", name="Anna")

manga1 = Manga(title="Гармония", author="ITOU Keikaku", tags_string="Драма,Научная фантастика,Психология,Сёнэн,Юри")
manga2 = Manga(title="Эврика 7. Псалмы Планет", author="BONES", tags_string="Драма,Меха,Научная фантастика,Романтика")
manga3 = Manga(title="Всё, что тебе нужно — это убивать", author="TAKEUCHI Ryousuke", tags_string="Боевик,Драма,Психология,Сёнэн,\
                                                                                                    Трагедия,Фантастика,Меха,Мистика,\
                                                                                                    Романтика,Военные,Монстры,\
                                                                                                    Путешествие во времени,ГГ мужчина,Жестокий мир,\
                                                                                                    Завоевание мира,Спасение мира")
manga4 = Manga(title="Человек-бензопила", author="FUJIMOTO Tatsuki", tags_string="Комедия,Сверхъестественное,Трагедия,Ужасы,Фэнтези,Романтика,Боевик,\
                                                                                    Сёнэн,ГГ мужчина,Жестокий мир,Монстры,Насилие & жестокость,Зомби,\
                                                                                    Антигерой,Дружба,Огнестрельное оружие,Скрытие личности")
manga5 = Manga(title="Ванпанчмен", author="ONE", tags_string="Боевик,Боевые искусства,Комедия,Сверхъестественное,Сёнэн,Фантастика,Ниндзя,Самураи,\
                                                                Преступники & Криминал,Лоли,Монстр Девушки,Монстры,Боги,Апокалипсис,ГГ мужчина,\
                                                                Ранги силы,Навыки & способности,Насилие & жестокость,Пародия,Разумные расы,Роботы,\
                                                                Спасение мира,Супергерои,Учитель & ученик,Философия,Холодное оружие,Япония,ГГ имба")
manga6 = Manga(title="Психопаспорт. Грешники Системы", author="Ryo Yoshigami", tags_string="Боевик,Киберпанк,\
                                                                                                                                Научная фантастика,\
                                                                                                                                Психология,Сёнэн,Драма,\
                                                                                                                                Антиутопия,Будущее")
db.session.add_all([user1, user2, user3, user4, user5, user6, manga2, manga3, manga4, manga5, manga6])
db.session.commit()
app_ctx.pop()