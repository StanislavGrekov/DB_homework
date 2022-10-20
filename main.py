import json
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from connect import name, password, name_DB   # Имя пользователя, пароль и названия БД лежат в другом файле


DSN = f'postgresql://{name}:{password}@localhost:5432/{name_DB}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/test_data.json', 'r') as fd:
    data = json.load(fd)

for element in data:
    if element['model'] == 'publisher':
        values_ = Publisher(id=element["pk"], name=element['fields']["name"])
        session.add(values_)
    elif element['model'] == 'book':
        values_ = Book(id=element["pk"], title=element['fields']["title"],
                       id_publisher=element['fields']["id_publisher"])
        session.add(values_)
    elif element['model'] == 'shop':
        values_ = Shop(id=element["pk"], name=element['fields']["name"])
        session.add(values_)
    elif element['model'] == 'stock':
        values_ = Stock(id=element["pk"], id_book=element['fields']["id_book"], id_shop=element['fields']["id_shop"],
                        count=element['fields']["count"])
        session.add(values_)
    elif element['model'] == 'sale':
        values_ = Sale(id=element["pk"], price=element['fields']["price"], date_sale=element['fields']["date_sale"],
                       id_stock=element['fields']["id_stock"], count=element['fields']["count"])
        session.add(values_)
session.commit()

input_ = input('Введите имя издателя или его идентификатор\n')
if input_.isdigit():
    q = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == input_)
    for s in q.all():
        print(s)
else:
    q = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == input_)
    for s in q.all():
        print(s)

session.close()





# publisher1 = Publisher(name="Ильф,Петров")
# publisher2 = Publisher(name="Ф.Достаевский")
#
# book1 = Book(title='12 стульев', id_publisher = 1)
# book2 = Book(title='Золотой теленок', id_publisher = 1)
# book3 = Book(title='Идиот', id_publisher=2)
# book4 = Book(title='Братья карамазовы', id_publisher=2)
#
# shop1 = Shop(name="Читай город")
# shop2 = Shop(name='Книжная лавка')
#
# stock1 = Stock(id_book=1, id_shop=1, count=5)
# stock2 = Stock(id_book=3, id_shop=2, count=4)
#
# sale1 = Sale(price=256.30, date_sale='2022-10-19', id_stock=1, count=1)
# sale2 = Sale(price=300.70, date_sale='2022-10-20', id_stock=2, count=2)

# session.add_all([publisher1, publisher2])
# session.add_all([book1, book2, book3, book4])
# session.add_all([shop1,shop2])
# session.add_all([stock1,stock2])
# session.add(sale1)
# session.add(sale2)
