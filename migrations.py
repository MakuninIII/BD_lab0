import psycopg2
from psycopg2 import OperationalError

###  Миграция для создания таблиц

def create_tables():
    commands = (
        """
        CREATE TABLE Artist (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            country VARCHAR(255) NOT NULL,
            debut_year INT 
        )
        """,
        """
        CREATE TABLE Song (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            release_year INT,
            duration INT,
            artist_id INTEGER NOT NULL,
            FOREIGN KEY (artist_id)
                REFERENCES Artist (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE Genre (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE Song_Genre (
            song_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (song_id, genre_id),
            FOREIGN KEY (song_id)
                REFERENCES Song (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (genre_id)
                REFERENCES Genre (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
       
    conn = psycopg2.connect(dbname="Music", user="postgres", password=" ", host="localhost")
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    cur.close()
    conn.commit()
    conn.close()



### Миграция для первоначального наполнения данных

def insert_initial_data():
    artist_data = [
        ("Metallica", "USA", 1981),
        ("Iron Maiden", "UK", 1975),
        ("Pink Floyd", "UK", 1965),
        ("Nirvana", "USA", 1987),
        ("Black Sabbath", "UK", 1968),
        ("AC/DC", "Australia", 1973),
        ("Deep Purple", "UK", 1968),
        ("Megadeth", "USA", 1983),
        ("Pantera", "USA", 1981),
        ("Slipknot", "USA", 1995)
    ]
    
    song_data = [
        ("Unforgiven", 1, 1991, 388),
        ("The Trooper", 2, 1983, 256),
        ("Smells Like Teen Spirit", 4, 1991, 301),
        ("Something in the Way", 4, 1991, 232),
        ("Paranoid", 5, 1970, 171),
        ("Highway to Hell", 6, 1979, 208),
        ("Symphony of Destruction", 8, 1992, 290),
        ("Walk", 9, 1992, 330),
        ("Duality", 10, 2004, 240),
        ("Sic", 10, 1999, 193)
    ]
    
    genre_data = [
        ("Metal",),
        ("Heavy Metal",),
        ("Hard Rock",),
        ("Alternative Rock",),
        ("Grunge",),
        ("Classic Rock",),
        ("Thrash Metal",),
        ("Groove Metal",),
        ("Nu Metal",),
        ("Jazz",)
    ]
    
    song_genre_data = [
        (1, 1),  # Unforgiven - Metal
        (1, 3),  # Unforgiven - Hard Rock
        (2, 2),  # The Trooper - Heavy Metal
        (3, 5),  # Smells Like Teen Spirit - Grunge
        (3, 4),  # Smells Like Teen Spirit - Alternative Rock
        (4, 5),  # Something in the Way - Grunge
        (4, 4),  # Something in the Way - Alternative Rock
        (5, 2),  # Paranoid - Heavy Metal
        (5, 1),  # Paranoid - Metal
        (6, 3),  # Highway to Hell - Hard Rock
        (7, 7),  # Symphony of Destruction - Thrash Metal
        (8, 8),  # Walk - Groove Metal
        (9, 9),  # Duality - Nu Metal
        (9, 1),  # Duality - Metal
        (10, 9), # Sic - Nu Metal
        (10, 1)  # Sic - Metal
    ]   

    conn = psycopg2.connect(dbname="Music", user="postgres", password=" ", host="localhost")
    cur = conn.cursor()

    cur.executemany("INSERT INTO Artist (name, country, debut_year) VALUES (%s, %s, %s)", artist_data)
    cur.executemany("INSERT INTO Song (title, artist_id, release_year, duration) VALUES (%s, %s, %s, %s)", song_data)
    cur.executemany("INSERT INTO Genre (name) VALUES (%s)", genre_data)
    cur.executemany("INSERT INTO Song_Genre (song_id, genre_id) VALUES (%s, %s)", song_genre_data)

    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # create_tables()
    insert_initial_data()