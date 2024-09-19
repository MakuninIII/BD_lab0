import psycopg2


###  Миграция для создания таблиц

def create_tables():
    commands = (
        """
        CREATE TABLE Artist (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE Song (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
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
            track_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
            PRIMARY KEY (track_id, genre_id),
            FOREIGN KEY (track_id)
                REFERENCES Track (id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (genre_id)
                REFERENCES Genre (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

conn = psycopg2.connect()
cur = conn.cursor()
for command in commands:
            cur.execute(command)
cur.close()
conn.commit()
conn.close()

### Миграция для первоначального наполнения данных

def insert_initial_data():
    artist_data = [
        ("Metallica",),
        ("Iron Maiden",),
        ("Pink Floyd",),
        ("Nirvana",),
        ("Black Sabbath",),
        ("AC/DC",),
        ("Deep Purple",),
        ("Megadeth",),
        ("Pantera",),
        ("Slipknot",)
    ]
    
    song_data = [
        ("Unforgiven", 1),
        ("The Trooper", 2),
        ("Smells Like Teen Spirit", 4),
        ("Something in the Way", 4),
        ("Paranoid", 5),
        ("Highway to Hell", 6),
        ("Symphony of Destruction", 8),
        ("Walk", 9),
        ("Duality", 10),
        ("Sic", 10)
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

conn = psycopg2.connect()
cur = conn.cursor()

cur.executemany("INSERT INTO Artist (name) VALUES (%s)", artist_data)

cur.executemany("INSERT INTO Song (title, artist_id) VALUES (%s, %s)", song_data)

cur.executemany("INSERT INTO Genre (name) VALUES (%s)", genre_data)

cur.executemany("INSERT INTO Track_Genre (track_id, genre_id) VALUES (%s, %s)", track_genre_data)

cur.close()
conn.commit()
conn.close()