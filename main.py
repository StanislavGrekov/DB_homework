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
            phone_ INTEGER UNIQUE
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
        INSERT INTO phone(phone_book_id, phone_)
        VALUES(%s,%s);
    ''', (id,phone_))
    conn.commit()
    print(f'Телефонный номер {phone_} клиенту {last_name_} добавлен.')


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
        SELECT phone_book_id, phone_ FROM phone ph
        INNER JOIN phone_book pb ON pb.id = ph.phone_book_id 
        WHERE pb.last_name = %s;
    ''', (last_name_,))
    answer = cursor.fetchall()
    phone_ = int(phone_)
    # answer_phone = [answer[0][1], answer[0][2]]
    for element in answer:
        if phone_ == element[1]:
            cursor.execute("""
                    DELETE FROM phone
                    WHERE phone_ = %s;
                    
                    """, (element[1],))
            conn.commit()
            print(f'Телефонный номер {phone_}  клиентa {last_name_} успешно удален.')


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


def find_client_name(cursor, last_name_):
    '''
    Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у).
    '''
    cursor.execute("""
                    SELECT last_name, first_name, email, date_insert, phone_ FROM phone_book pb
                    INNER JOIN phone p ON pb.id = p.phone_book_id
                    WHERE last_name = %s;
                    """, (last_name_,))
    answer = cursor.fetchall()
    list_phone = []
    for element in answer:
            list_phone.append(element[4])
    conn.commit()
    str_List_phone = [str(i) for i in list_phone]
    print(f'Фамилия: {answer[0][0]}, Имя: {answer[0][1]}, почта: {answer[0][2]}, дата занесения информации: {answer[0][3]}, '
                      f'тел.номера: {",".join(str_List_phone)}')



def find_client_phone(cursor, phone_):
    '''
    Функция, позволяющая найти клиента по его телефону.
    '''
    try:
        cursor.execute("""
            SELECT last_name, first_name, email, date_insert, phone_ FROM phone_book pb
            INNER JOIN phone p ON pb.id = p.phone_book_id
            WHERE phone_ = %s;
            """, (phone_,))
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
                key_next = input('Введите name, если хотите произвести поиск по фамилии или введите'
                                 ' phone, если хотите выполнить поиск по телефону. Можете ввести q для '
                                 'выхода в предыдущее меню.\n')
                while True:
                    if key_next == 'name':
                        last_name_ = input(
                            'Введите фамилию:\n')
                        find_client_name(cursor, last_name_)
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