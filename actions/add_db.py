import os
import sqlite3
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Clothes
                 (id INT AUTO_INCREMENT, clothes_name VARCHAR(100), clothes_2 VARCHAR(100))''')
    cursor.execute("CREATE TABLE IF NOT EXISTS User (user_id integer, clothes_id integer)")


def insert_words(file, cursor):
    words = file.readlines()

    id_ = 0
    for word in words:

        p = morph.parse(word.split(': ')[0])[0].normal_form
        cursor.execute("INSERT INTO Clothes (id, clothes_name, clothes_2) VALUES (?, ?, ?)", (id_, p, word.split(': ')[1]))
        id_ += 1


def write():
    relative = os.path.join(os.curdir, "clothes.txt")
    absolute_path = os.path.abspath(relative)
    with open(absolute_path, "r",encoding='UTF-8') as elements,  sqlite3.connect("clothes.db") as conn:
        cursor = conn.cursor()

        create_tables(cursor)
        conn.commit()

        insert_words(elements, cursor)
        conn.commit()

        print()


if __name__ == "__main__":
    write()