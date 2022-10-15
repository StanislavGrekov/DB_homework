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
            last_name varchar(40) NOT NULL,
            first_name varchar(40) NOT NULL,
            phone varchar(40), -- Сделал 40, чтобы вошло побольше номеров. Взял varchar, чтобы можно было использовать -.
            email varchar(40) UNIQUE NOT NULL,
            date_insert DATE
            );
        ''')
    conn.commit()
    print('Структура успешно создана.')


def drop(cursor):
    '''
    Функция, удаляющая структуру в БД
    '''
    cursor.execute('''
            DROP TABLE phone_book;
        ''')
    conn.commit()
    print('Структура успешно удалена.')

def insert(cursor):
    try:
        '''
        Функция, позволяющая добавить нового клиента в БД.
        '''
        last_name_, first_name_, phone_, email_ = input('Введите через пробел фамилию,имя,телефон,э-почту (почта '
                                                        'должна быть уникальной для всех клиентов), если номера '
                                                        'телефона нет, введите -\n').split() # нужно сделать проверку по почте, хотябы есть ли там @
        date = datetime.datetime.now()
        current_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day)) # Эта переменная str, а я ее смог вставить в таблицу в ячейку с типом DATE. Непонятно.
        cursor.execute('''
                INSERT INTO phone_book(last_name, first_name, phone, email, date_insert)
                VALUES (%s, %s, %s, %s, %s) RETURNING last_name;
        ''', (last_name_, first_name_, phone_, email_, current_date))
        conn.commit()
        print(f'Запись с фамилией {cursor.fetchone()[0]} добавлена в базу.\n')
    except ValueError:
        print('Возникла ошибка!\nНесоответствие аргументов количеству столбцов в таблице. Попробуйте снова.')
        insert(cursor)
    except: # Здесь можно обрабатывать другие ислючения, надо только знать их типы.
         print('Возникла ошибка!\nПопробуйте снова.')
         insert(cursor)


def add_phone(cursor):
    '''
    Функция, позволяющая добавить телефон для существующего клиента.
    '''
    last_name_, phone_ = input('Введите через пробел фамилию клиента и номер телефона, который вы хотите добавить.\n').split() # нужно сделать проверку номера телефона, цифры ли это
    cursor.execute('''
        SELECT phone FROM phone_book
        WHERE last_name = %s;
    ''', (last_name_,))
    response_phone = cursor.fetchone()[0]
    if response_phone == '-':
        cursor.execute('''
            UPDATE phone_book SET phone = %s
            WHERE last_name = %s;
            ''', (phone_, last_name_))
    else: #Нужно сделать проверку на случай, если номер повторяется
        new_phone = (str(response_phone)+', '+str(phone_))
        cursor.execute('''
            UPDATE phone_book SET phone = %s
            WHERE last_name = %s;
            ''', (new_phone, last_name_))
    conn.commit()
    print(f'Номер телефона {phone_} успешно добавлен в базу для клиента {last_name_}.')

def change_clients(cursor):
      '''
      Функция, позволяющая изменить данные о клиенте в БД.
      '''
      date = datetime.datetime.now()
      current_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))
      last_name_ = input('Введите фамилию сотрудника, данные о котором необходимо изменить\n')
      cursor.execute("""
            SELECT * FROM phone_book WHERE last_name=%s;
            """, (last_name_,))
      for element in cursor.fetchall():
          print(f'По указанному сотруднику есть следующая информация:\nФамилия: {element[1]}, '
                 f'Имя: {element[2]}, телефон: {element[3]}, э-почта: {element[4]}, '
                 f'дата внесения информации: {element[5]}')
      first_name_, phone_, email_ = input('Введите новую информацию (имя, телефон, почтовый адрес) через пробел:').split()
      cursor.execute("""
            UPDATE phone_book SET first_name = %s, phone = %s, email = %s, date_insert = %s WHERE last_name=%s;
            """, (first_name_, phone_, email_, current_date, last_name_))
      conn.commit()
      print(f'Данные по клиенту {last_name_} успешно изменены.')

def delete_phone(cursor):
    '''
    Функция, позволяющая удалить телефон для существующего клиента
    '''
    last_name_ = input('Введите фамилию клиента, телефонный номер которого необходимо удалить\n')
    cursor.execute("""
        UPDATE phone_book SET phone = '-' WHERE last_name=%s;
        """, (last_name_,))
    conn.commit()
    print(f'Телефонный номер по клиенту {last_name_} успешно удален.')

def delete_client(cursor):
    '''
    Функция, позволяющая удалить существующего клиента из БД
    '''
    last_name_ = input('Введите фамилию клиента, которого требуется удалить из БД\n')
    cursor.execute("""
        DELETE FROM phone_book WHERE last_name=%s;
        """, (last_name_,))
    conn.commit()
    print(f'Сотрудник с фамилией {last_name_} успешно удален.')


def find_client(cursor):
    '''
    Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    '''
    field = str(input(
        "n - поиск по столбцу с именем,\n"
        "f - поиск по столбцу с фамилией,\n"
        "e - поиск по столбцу с э-почтой,\n"
        "p - поиск по столбцу с телефоном.\n"))
    field = field.lower()
    condition = str(input("Теперь введите параметр поиска соответствующий столбцу:"))
    if field == 'n':
        cursor.execute("""SELECT * FROM phone_book WHERE first_name=%s;""", (condition,))
    elif field == 'f':
        cursor.execute("""SELECT * FROM phone_book WHERE last_name=%s;""", (condition,))
    elif field == 'p':
        cursor.execute("""SELECT * FROM phone_book WHERE phone=%s;""", (condition,))
    elif field == 'e':
        cursor.execute("""SELECT * FROM phone_book WHERE email=%s;""", (condition,))
    for element in cursor.fetchall():
        print(f'По указанному сотруднику есть следующая информация:\nФамилия: {element[1]}, '
              f'Имя: {element[2]}, телефон: {element[3]}, э-почта: {element[4]}, '
              f'дата внесения информации: {element[5]}')
    conn.commit()

# Данное решение не работает, не смог разобраться. Проблема в передачи кавычек в условие.
    # def execute(a,b):
    #     cursor.execute("""
    #   SELECT * FROM phone_book WHERE %s=%s;
    #   """, (a,b))
    #     print(f'По указанному сотруднику есть следующая информация {cursor.fetchall()}')
    #     conn.commit()
    # if field == 'n':
    #     execute('first_name', condition)
    # elif field == 'f':
    #     execute('last_name', condition)
    # elif field == 'p':
    #     execute('phone', condition)
    # elif field == 'e':
    #     execute('phone', condition)

def end(cursor):
    conn.close()
    print('Мы закончили.')
    exit()


dict_commands = {
    'c': create_table,
    'd': drop,
    'i': insert,
    'ap': add_phone,
    'cc': change_clients,
    'dp': delete_phone,
    'dc': delete_client,
    'fc': find_client,
    'q': end
}

if __name__ == '__main__':
    print('Приветсвуем вас в сервисе по добавлению клиентов в базу данных PostgreSQL')
    def main():
        while True:
            key = input("Введите:\nс - для создания структуры в БД,\n"
                            "d - для удалиения структуры БД,\n"
                            "i - для внесения информации по клиенту в БД,\n"
                            "ap - для внесения номера телефона клиенту,\n"
                            "cc - для изменения данных по клиенту,\n"
                            "dp - для удаления номера телефона клиента (функция удалит все имеющиеся номера клиента),\n"
                            "dc - для удаления данных по клиенту из БД,\n"
                            "fc - для поиска сотрудника в БД,\n"
                            "q - выход из програмы.\n")
            key = key.lower()
            processing(key)


    def processing(command):
        dict_commands[command](cursor)
    conn = psycopg2.connect(database=database, user=user, password=password)
    cursor = conn.cursor()
    main()

