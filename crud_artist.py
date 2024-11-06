import psycopg2
import time
from datetime import datetime
from prettytable import PrettyTable

def get_connection():
    conn = psycopg2.connect(
        dbname="Test",
        user="postgres",
        password=" ",
        host="localhost"
    )
    return conn

# 1.Create - добавляет нового артиста
def ArtistCreate(conn):
    while True:
        name = input("Enter artist name: ")
        name = name.strip()
        
        if not name:
            print("Error: name cannot be empty.")
            continue
        else:
            break

    while True:
        country = input("Enter artist country: ")
        if not country.isalpha():
            print("Error: country should only contain letters.")
        else:
            break

    current_year = datetime.now().year
    while True:
        try:
            debut_year = int(input("Enter debut year: "))
            if debut_year < 1860 or debut_year > current_year:
                print(f"Error: debut year must be between 1860 and {current_year}.")
            else:
                break
        except ValueError:
            print("Error: debut year must be a valid number.")

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Artist (name, country, debut_year) VALUES (%s, %s, %s) RETURNING id",
        (name, country, debut_year)
    )
    artist_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    print(f"Artist created with ID: {artist_id}")
    time.sleep(1)

# 2.RetrieveAll - получает всех артистов
def ArtistRetrieveAll(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artist")
    artists = cur.fetchall()
    
    if not artists:
        print("No artists found.")
    else:
        table = PrettyTable()
        table.field_names = ["id", "Name", "Country", "Debut Year"]
        for artist in artists:
            table.add_row(artist)
        print(table)
    cur.close()

# 3.Retrieve - получает одного артиста по первичному ключу
def ArtistRetrieve(conn):
    while True:
        try:
            artist_id = int(input("Enter artist ID: "))
            break 
        except ValueError:
            print("Error: Artist ID must be an integer. Please try again.")

    cur = conn.cursor()
    cur.execute("SELECT * FROM Artist WHERE id = %s", (artist_id,))
    artist = cur.fetchone()

    if artist:
        table = PrettyTable()
        table.field_names = ["id", "Name", "Country", "Debut Year"]
        table.add_row(artist)
        print(table)
    else:
        print(f"Artist with ID {artist_id} not found.")
        time.sleep(1)

    cur.close()


# 4.Update - обновляет информацию о конкретном артисте по его ID
def ArtistUpdate(conn):
    while True:
        try:
            artist_id = int(input("Enter artist ID: "))
            break 
        except ValueError:
            print("Error: Artist ID must be an integer. Please try again.")

    cur = conn.cursor()
    cur.execute("SELECT name, country, debut_year FROM Artist WHERE id = %s", (artist_id,))
    artist = cur.fetchone()

    if artist is None:
        print(f"Artist with ID {artist_id} not found.")
        cur.close()
        time.sleep(1)
        return
    
    current_name, current_country, current_debut_year = artist

    while True:
        name = input(f"Enter new artist name (or leave empty to keep current - '{current_name}'): ")
        if not name:
            name = current_name
            break
        elif name.strip() == "":
            print("Error: name can't be empty.")
        else:
            name = name.strip()
            break

    while True:
        country = input(f"Enter new artist country (or leave empty to keep current - '{current_country}'): ")
        if not country:
            country = current_country
            break
        elif not country.isalpha():
            print("Error: country should only contain letters.")
        else:
            break

    current_year = datetime.now().year

    while True:
        debut_year = input(f"Enter new debut year (or leave empty to keep current - '{current_debut_year}'): ")
        if not debut_year:
            debut_year = current_debut_year
            break
        try:
            debut_year = int(debut_year)
            if debut_year < 1860 or debut_year > current_year:
                print(f"Error: debut year must be between 1860 and {current_year}.")
            else:
                break
        except ValueError:
            print("Error: debut year must be a valid number.")

    cur = conn.cursor()
    cur.execute(
        "UPDATE Artist SET name = %s, country = %s, debut_year = %s WHERE id = %s",
        (name, country, debut_year, artist_id)
    )
    conn.commit()
    if cur.rowcount:
        print(f"Artist with ID {artist_id} updated successfully.")
        cur.execute("SELECT * FROM Artist WHERE id = %s", (artist_id,))
        updated_artist = cur.fetchone()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Country", "Debut Year"]
        table.add_row(updated_artist)
        print(f"Updated artist data: \n{table}")
    else:
        print(f"Artist with ID {artist_id} not found.")

    cur.close() 


# 5.Delete - удаляет артиста по его ID
def ArtistDelete(conn):
    while True:
        try:
            artist_id = int(input("Enter artist ID: "))
            break 
        except ValueError:
            print("Error: Artist ID must be an integer. Please try again.")

    cur = conn.cursor()

    cur.execute("DELETE FROM Artist WHERE id = %s", (artist_id,))
    conn.commit()
    if cur.rowcount > 0:
        print(f"Artist with ID {artist_id} deleted successfully.")
        time.sleep(1)
    else:
        print(f"Artist with ID {artist_id} not found.")
        time.sleep(1)
    
    cur.close()


# 6.DeleteMany - удаляет несколько артистов по их ID
def ArtistDeleteMany(conn):
    while True:
        artist_ids = input("Enter artist IDs separated by commas: ")
        artist_ids = [x.strip() for x in artist_ids.split(",")]

        if all(x.isdigit() for x in artist_ids):
            artist_ids = [int(x) for x in artist_ids]
            break
        else:
            print("Error: Please enter valid artist IDs separated by commas. Only numeric IDs are allowed.")

    cur = conn.cursor()
    cur.execute("SELECT id FROM Artist WHERE id = any(%s)", ([artist_ids],))
    existing_ids = [row[0] for row in cur.fetchall()]

    if not existing_ids:
        print("No artists found with the provided IDs.")
        cur.close()
        time.sleep(1)
        return

    cur.execute("DELETE FROM Artist WHERE id = any(%s)", ([existing_ids],))
    conn.commit()

    not_found_ids = set(artist_ids) - set(existing_ids)

    if existing_ids:
        print(f"Artists with IDs {set(existing_ids)} deleted successfully.")
    if not_found_ids:
        print(f"No artists found with IDs: {not_found_ids}")

    cur.close()
    time.sleep(1)


# лаб. 2 // 7.Search - поиск экземпляров сущности по указанным пользователем значениям атрибутов
def ArtistSearch(conn, name=None, country=None, debut_year=None, limit=5, offset=0):
    cur = conn.cursor()

    query = "SELECT * FROM Artist WHERE 1=1"
    params = []

    if name is not None:
        query += " AND name ILIKE %s"
        params.append(f"%{name.lower()}%")
    if country is not None:
        query += " AND LOWER(country) = LOWER(%s)"
        params.append(country.strip())
    if debut_year is not None:
        query += " AND debut_year = %s"
        params.append(debut_year)

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cur.execute(query, params)
    artists = cur.fetchall()

    if artists:
        for artist in artists:
            print(artist)
    else:
        print("No artists found matching the criteria.")

    cur.close()


# main
if __name__ == "__main__":

    conn = psycopg2.connect(
        dbname="Test",
        user="postgres",
        password=" ",
        host="localhost"
    )
        
    while True:
        print("\n1. Create Artist")
        print("2. Retrieve All Artists")
        print("3. Retrieve Artist by ID")
        print("4. Update Artist")
        print("5. Delete Artist by ID")
        print("6. Delete Many Artists")
        print("7. Search Artist by attributes")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ArtistCreate(conn)
        elif choice == '2':
            ArtistRetrieveAll(conn)
        elif choice == '3':
            ArtistRetrieve(conn)
        elif choice == '4':
            ArtistUpdate(conn)
        elif choice == '5':
            ArtistDelete(conn)
        elif choice == '6':
            ArtistDeleteMany(conn)
        elif choice == '7':
            name = input(str("Enter name (or press Enter to skip): ")) or None
            country = input("Enter artist's country (or press Enter to skip): ") or None
            debut_year = input("Enter debut year (or press Enter to skip): ") or None
            try:
                limit_count = input("Enter number of output results (default 5): ")
                if limit_count:
                    limit_count = int(limit_count)
                    if limit_count < 0:
                        limit_count = None
                        print("Limit can't be negative. The default value (5) has been assigned.")
                limit_count = int(limit_count) if limit_count else 5
            except ValueError:
                print("Invalid input. The default value (5) has been assigned.")
                limit_count = 5
            
            try:
                offset_count = input("Enter offset (default 0): ")
                if offset_count:
                    offset_count = int(offset_count)
                    if int(offset_count) < 0:
                        offset_count = None
                        print("Offset can't be negative. The default value (0) has been assigned.")
                offset_count = int(offset_count) if offset_count else 0
            except ValueError:
                print("Invalid input. The default value (0) has been assigned.")
                offset_count = 0

            time.sleep(0.5)
            ArtistSearch(conn, name, country, debut_year, limit_count, offset_count)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()