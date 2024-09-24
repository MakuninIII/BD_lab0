import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="Music",
        user="postgres",
        password="your_password",  # Замените на свой пароль
        host="localhost"
    )
    return conn

# Create - добавляет нового артиста
def ArtistCreate(name, country, debut_year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Artist (name, country, debut_year) VALUES (%s, %s, %s) RETURNING id",
        (name, country, debut_year)
    )
    artist_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"Artist created with ID: {artist_id}")

# RetrieveAll - получает всех артистов
def ArtistRetrieveAll():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artist")
    artists = cur.fetchall()
    for artist in artists:
        print(artist)
    cur.close()
    conn.close()

# Retrieve - получает одного артиста по первичному ключу
def ArtistRetrieve(artist_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Artist WHERE id = %s", (artist_id,))
    artist = cur.fetchone()
    if artist:
        print(artist)
    else:
        print(f"Artist with ID {artist_id} not found.")
    cur.close()
    conn.close()

# Update - обновляет информацию о конкретном артисте по его ID
def ArtistUpdate(artist_id, name, country, debut_year):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Artist SET name = %s, country = %s, debut_year = %s WHERE id = %s",
        (name, country, debut_year, artist_id)
    )
    conn.commit()
    if cur.rowcount:
        print(f"Artist with ID {artist_id} updated successfully.")
    else:
        print(f"Artist with ID {artist_id} not found.")
    cur.close()
    conn.close()

# Delete - удаляет артиста по его ID
def ArtistDelete(artist_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Artist WHERE id = %s", (artist_id,))
    conn.commit()
    if cur.rowcount:
        print(f"Artist with ID {artist_id} deleted successfully.")
    else:
        print(f"Artist with ID {artist_id} not found.")
    cur.close()
    conn.close()

# DeleteMany - удаляет несколько артистов по их ID
def ArtistDeleteMany(artist_ids):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Artist WHERE id IN %s", (tuple(artist_ids),))
    conn.commit()
    print(f"Artists with IDs {artist_ids} deleted successfully.")
    cur.close()
    conn.close()

# main
if __name__ == "__main__":
    while True:
        print("\n1. Create Artist")
        print("2. Retrieve All Artists")
        print("3. Retrieve Artist by ID")
        print("4. Update Artist")
        print("5. Delete Artist by ID")
        print("6. Delete Many Artists")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter artist name: ")
            country = input("Enter artist country: ")
            debut_year = input("Enter debut year: ")
            ArtistCreate(name, country, debut_year)
        elif choice == '2':
            ArtistRetrieveAll()
        elif choice == '3':
            artist_id = int(input("Enter artist ID: "))
            ArtistRetrieve(artist_id)
        elif choice == '4':
            artist_id = int(input("Enter artist ID: "))
            name = input("Enter new artist name: ")
            country = input("Enter new artist country: ")
            debut_year = input("Enter new debut year: ")
            ArtistUpdate(artist_id, name, country, debut_year)
        elif choice == '5':
            artist_id = int(input("Enter artist ID: "))
            ArtistDelete(artist_id)
        elif choice == '6':
            artist_ids = input("Enter artist IDs separated by commas: ")
            artist_ids = [int(x) for x in artist_ids.split(",")]
            ArtistDeleteMany(artist_ids)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")