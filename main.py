import psycopg2
import datetime
from my_config import user, password, database


def create_table(cursor):
    '''
    Функция, создающая структуру БД
    '''
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phone_book(
        	id SERIAL PRIMARY KEY,
            email VARCHAR(80) UNIQUE NOT NULL,
            last_name varchar(40) NOT NULL,
            first_name varchar(40) NOT NULL,
            date_insert DATE
            );
        CREATE TABLE IF NOT EXISTS phone(
        	id SERIAL PRIMARY KEY,
            phone_book_id INTEGER NOT NULL REFERENCES phone_book(id),
            phone_1 INTEGER,
            phone_2 INTEGER,
            phone_3 INTEGER,
            phone_4 INTEGER
            );
                ''')
    conn.commit()
    print('Структура успешно создана.')


def drop(cursor):
    '''
    Функция, удаляющая структуру в БД
    '''
    cursor.execute('''
            DROP TABLE phone;
            DROP TABLE phone_book;
        ''')
    conn.commit()
    print('Структура успешно удалена.')


def insert(cursor, last_name_, first_name_, email_):
        '''
        Функция, позволяющая добавить нового клиента в БД.
        '''
        date = datetime.datetime.now()
        current_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))
        cursor.execute('''
                INSERT INTO phone_book(email, last_name, first_name, date_insert)
                VALUES (%s, %s, %s, %s);
        ''', (email_, last_name_, first_name_, current_date))
        cursor.execute('''
                 SELECT id FROM phone_book
                 WHERE last_name = %s;
         ''', (last_name_,))
        answer = cursor.fetchall()
        cursor.execute('''
                INSERT INTO phone (phone_book_id, phone_1, phone_2, phone_3, phone_4)
                VALUES (%s, %s, %s, %s, %s);
        ''', (answer[0],0, 0, 0, 0))
        conn.commit()
        print(f'Запись с фамилией {last_name_} добавлена в базу.\n')


def add_phone(cursor, last_name_, phone_ ):
    '''
    Функция, позволяющая добавить телефон для существующего клиента.
    '''
    cursor.execute('''
        SELECT id FROM phone_book
        WHERE last_name = %s;
    ''', (last_name_,))
    id = cursor.fetchall()[0]
    cursor.execute('''
        SELECT phone_1, phone_2,phone_3, phone_4 FROM phone
        WHERE phone_book_id = %s;
    ''', (id,))
    answer = cursor.fetchall()
    phone_ = int(phone_)
    for element in answer:
        phone_1, phone_2, phone_3, phone_4 =element[0], element[1], element[2], element[3]
        if phone_1 == phone_  or phone_2 == phone_ or phone_3 == phone_ or phone_4 == phone_: # Проверка на совпадение номера телефона
            print('Такой телефон у данного клиента уже есть, введите другой!')
        else:
            if phone_1 == 0:
                cursor.execute("""
                      UPDATE phone SET phone_1 = %s WHERE phone_book_id=%s;
                      """, (phone_, id))
                print(f'Телефонный номер {phone_} клиенту {last_name_} добавлен.')
            elif phone_1 != 0 and phone_2 == 0:
                cursor.execute("""
                      UPDATE phone SET phone_2 = %s WHERE phone_book_id=%s;
                      """, (phone_, id))
                print(f'Телефонный номер {phone_} клиенту {last_name_} добавлен.')
            elif phone_1 != 0 and phone_2 != 0 and phone_3 == 0:
                cursor.execute("""
                      UPDATE phone SET phone_3 = %s WHERE phone_book_id=%s;
                      """, (phone_, id))
                print(f'Телефонный номер {phone_} клиенту {last_name_} добавлен.')
            elif phone_1 != 0 and phone_2 != 0 and phone_3 != 0 and phone_4 == 0:
                cursor.execute("""
                      UPDATE phone SET phone_4 = %s WHERE phone_book_id=%s;
                      """, (phone_, id))
                print(f'Телефонный номер {phone_} клиенту {last_name_} добавлен.')
            elif phone_1 != 0 and phone_2 != 0 and phone_3 != 0 and phone_4 != 0:
                print('К сожалению больше телефонов клиенту добавить нельзя.')
            conn.commit()


def change_clients(cursor, last_name_, last_name_new, first_name_new, email_new):
      '''
      Функция, позволяющая изменить данные о клиенте в БД, при этом тел.номера затронуты не будут.
      '''
      date = datetime.datetime.now()
      date_update = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))
      cursor.execute("""
            UPDATE phone_book SET email = %s, last_name=%s, first_name = %s, date_insert=%s WHERE last_name=%s;
            """, (email_new, last_name_new, first_name_new, date_update, last_name_))
      conn.commit()
      print(f'Данные по клиенту {last_name_} успешно изменены.')


def delete_phone(cursor, last_name_, phone_):
    '''
    Функция, позволяющая удалить телефон для существующего клиента.
    '''
    cursor.execute('''
        SELECT phone_book_id, phone_1, phone_2,phone_3, phone_4 FROM phone ph
        INNER JOIN phone_book pb ON pb.id = ph.phone_book_id 
        WHERE pb.last_name = %s;
    ''', (last_name_,))
    answer = cursor.fetchall()
    phone_ = int(phone_)
    answer_phone = [answer[0][1], answer[0][2], answer[0][3], answer[0][4]]
    list_ = []
    for element in answer_phone:
            if element != phone_:
                list_.append(element)
            else:
                list_.append('0')
    my_tuple = tuple(list_)
    if phone_ in answer_phone:
        cursor.execute("""
                UPDATE phone SET phone_1 = %s, phone_2 = %s, phone_3 = %s, phone_4 = %s WHERE phone_book_id = %s;
                """, (my_tuple[0], my_tuple[1], my_tuple[2], my_tuple[3], answer[0][0]))
        conn.commit()
        print(f'Телефонный номер {phone_}  клиентa {last_name_} успешно удален.')
    else:
        print(f'Телефона {phone_} у клиента {last_name_} нет.')


def delete_client(cursor, last_name_):
    '''
    Функция, позволяющая удалить информацию и телефонные номера из БД по клиенту.
    '''
    try:
        cursor.execute("""
            SELECT id, last_name FROM phone_book where last_name = %s;
            """, (last_name_,))
        answer = cursor.fetchall()
        cursor.execute("""
            DELETE FROM phone WHERE phone_book_id = %s
            """, (answer[0][0],))
        cursor.execute("""
            DELETE FROM phone_book WHERE last_name = %s
            """, (last_name_,))
        conn.commit()
        print(f'Сотрудник с фамилией {last_name_} успешно удален.')
    except: # Исключения нужно обрабатывать более грамотно, по коду ошибки.
        print(f'Сотрудника с фамилией {last_name_} не найдено.')


def find_client_name(cursor, last_name_, first_name_, email_):
    '''
    Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у).
    '''
    try:
        cursor.execute("""
                SELECT last_name, first_name, email, date_insert, phone_1,phone_2,phone_3,phone_4 FROM phone_book pb
                INNER JOIN phone p ON pb.id = p.phone_book_id
                WHERE last_name = %s AND first_name = %s AND email = %s;
                """, (last_name_, first_name_, email_))
        answer = cursor.fetchall()
        conn.commit()
        print(f'Фамилия: {answer[0][0]}, Имя: {answer[0][1]}, почта: {answer[0][2]}, дата занесения информации: {answer[0][3]}, '
                  f'тел.номер.№1: {answer[0][4]}, тел.номер.№2: {answer[0][5]}, тел.номер.№3: {answer[0][6]}, тел.номер.№4: {answer[0][7]} '
                  f'(Примечание - если телефонный номер - 0, значит он не задан.)')
    except:
        print('Информации по указанному сотруднику нет.')


def find_client_phone(cursor, phone_):
    '''
    Функция, позволяющая найти клиента по его телефону.
    '''
    try:
        cursor.execute("""
            SELECT last_name, first_name, email, date_insert, phone_1,phone_2,phone_3,phone_4 FROM phone_book pb
            INNER JOIN phone p ON pb.id = p.phone_book_id
            WHERE phone_1 = %s OR phone_2 = %s OR phone_3 = %s OR phone_4 = %s;
            """, (phone_, phone_, phone_, phone_))
        answer = cursor.fetchall()
        conn.commit()
        print(f'Фамилия: {answer[0][0]}, Имя: {answer[0][1]}, почта: {answer[0][2]}, дата занесения информации: {answer[0][3]},')
    except:
        print('Информации по указанному сотруднику нет.')

def end(cursor):
    conn.close()
    print('Мы закончили, спасибо за внимание.')
    exit()


if __name__ == '__main__':
    conn = psycopg2.connect(database=database, user=user, password=password)
    cursor = conn.cursor()
    print('Приветсвуем вас в сервисе по добавлению клиентов в базу данных PostgreSQL')
    def main():
        while True:
            key = input("Введите:\nс - для создания структуры в БД,\n"
                            "d - для удалиения структуры БД,\n"
                            "i - для внесения информации по клиенту в БД,\n"
                            "ap - для внесения номера телефона клиенту,\n"
                            "cc - для изменения данных по клиенту,\n"
                            "dp - для удаления номера телефона клиента,\n"
                            "dc - для удаления данных по клиенту из БД,\n"
                            "fc - для поиска сотрудника в БД,\n"
                            "q - выход из програмы.\n")
            key = key.lower()
            if key == 'c':
                create_table(cursor)
            elif key == 'd':
                drop(cursor)
            elif key == 'i':
                last_name_, first_name_, email_ = input(
                    'Введите через пробел фамилию,имя,э-почту (почта '
                    'должна быть уникальной для всех клиентов)\n').split()
                insert(cursor, last_name_, first_name_, email_)
            elif key == 'ap':
                last_name_, phone_ = input(
                    'Введите через пробел фамилию и номер телефона, который '
                    'вы хотите задать клиенту\n').split()
                add_phone(cursor, last_name_, phone_)
            elif key == 'cc':
                last_name_, last_name_new, first_name_new, email_new = input(
                    'Введите фамилию клиента, которому необхоидимо изменить данные, затем через пробел'
                    ' ведите новую фамилию, имя и электронный адрес.\n').split()
                change_clients(cursor, last_name_, last_name_new, first_name_new, email_new)
            elif key == 'dp':
                last_name_, phone_= input(
                    'Введите фамилию клиента и нормер телефона, который вы хотите удалить (через пробел)\n').split()
                delete_phone(cursor, last_name_, phone_)
            elif key == 'dc':
                last_name_ = input(
                    'Введите фамилию клиента, информацию по которому вы хотите удалить\n')
                delete_client(cursor, last_name_)
            elif key == 'fc':
                key_next = input('Введите name, если хотите произвести поиск по фамилии, имени и э.почте или введите'
                                 ' phone, если хотите выполнить поиск по телефону. Можете ввести q для '
                                 'выхода в предыдущее меню.\n')
                while True:
                    if key_next == 'name':
                        last_name_, first_name_, email_ = input(
                            'Введите фамилию, имя, эл. почту через пробел.\n').split()
                        find_client_name(cursor, last_name_, first_name_, email_)
                        break
                    elif key_next == 'phone':
                        phone_ = int(input(
                            'Введите телефонный номер\n'))
                        find_client_phone(cursor, phone_)
                        break
                    elif key_next == 'q':
                        break
            elif key == 'q':
                end(cursor)
    main()