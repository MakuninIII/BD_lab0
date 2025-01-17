import psycopg2
import time
from prettytable import PrettyTable


def GenreCreate(conn):
    name = input("Введите название жанра: ").strip()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CALL genreCreate(%s)", [name])
            conn.commit()
        if conn.notices:
            for notice in conn.notices:
                print(f"{notice}")
            conn.notices.clear()
            # print(f"Жанр {name} создан.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"{e}")


def GenreRetrieveAll(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM genreRetrieveAll()")
            rows = cursor.fetchall()
            table = PrettyTable(["ID", "Название"])
            for row in rows:
                table.add_row(row)
            print(table)
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при получении всех жанров: {e}")


def GenreRetrieve(conn):
    genre_id = input("Введите ID жанра: ").strip()
    try:
        genre_id = int(genre_id)
        with conn.cursor() as cursor:
            cursor.callproc("genreRetrieve", [genre_id])
            row = cursor.fetchone()
            if row:
                table = PrettyTable(["ID", "Название"])
                table.add_row(row)
                print(table)
            else:
                print(f"Жанр с ID {genre_id} не найден.")
    except ValueError:
        print("Некорректный ввод ID.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"{e}")


def GenreUpdate(conn):
    genre_id = input("Введите ID жанра для обновления: ").strip()
    new_name = input("Введите новое название жанра: ").strip()
    try:
        genre_id = int(genre_id)
        with conn.cursor() as cursor:
            cursor.execute("CALL genreUpdate(%s, %s)", [genre_id, new_name])
            conn.commit()
        if conn.notices:
            for notice in conn.notices:
                print(f"{notice}")
            conn.notices.clear()
            # print(f"Жанр с ID {genre_id} обновлен.")
    except ValueError:
        print("Некорректный ввод ID.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"{e}")


def GenreDelete(conn):
    genre_id = input("Введите ID жанра для удаления: ").strip()
    try:
        genre_id = int(genre_id)
        with conn.cursor() as cursor:
            cursor.execute("CALL genreDelete(%s)", [genre_id])
            conn.commit()
        if conn.notices:
            for notice in conn.notices:
                print(f"{notice}")
            conn.notices.clear()
            # print('Жанр успешно удален.')
    except ValueError:
        print("Некорректный ввод ID.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"{e}")


def GenreDeleteMany(conn):
    ids = input("Введите ID жанров для удаления через запятую: ").strip()
    try:
        ids_list = [int(x.strip()) for x in ids.split(",")]
        ids_str = ",".join(map(str, ids_list))
        
        with conn.cursor() as cursor:
            cursor.execute("CALL genreDeleteMany(%s)", [ids_str])
            conn.commit()
        if conn.notices:
            for notice in conn.notices:
                print(f"{notice}")
            conn.notices.clear()

    except ValueError:
        print("Некорректный ввод ID.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"{e}")


# Main
if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="Test",
        user="postgres",
        password=" ",
        host="localhost"
    )

    while True:
        print("\n1. Создать жанр")
        print("2. Получить все жанры")
        print("3. Получить жанр по ID")
        print("4. Обновить жанр")
        print("5. Удалить жанр по ID")
        print("6. Удалить несколько жанров")
        print("7. Выход")
        choice = input("Введите ваш выбор: ")

        if choice == '1':
            GenreCreate(conn)
        elif choice == '2':
            GenreRetrieveAll(conn)
        elif choice == '3':
            GenreRetrieve(conn)
        elif choice == '4':
            GenreUpdate(conn)
        elif choice == '5':
            GenreDelete(conn)
        elif choice == '6':
            GenreDeleteMany(conn)
        elif choice == '7':
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

    conn.close()
