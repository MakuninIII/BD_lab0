"""seed_initial_data

Revision ID: 8c181b9bae6a
Revises: 4c24cf36d150
Create Date: 2025-02-16 23:50:10.598439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c181b9bae6a'
down_revision: Union[str, None] = '4c24cf36d150'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("TRUNCATE TABLE artist RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE TABLE genre RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE TABLE song RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE TABLE song_genre RESTART IDENTITY CASCADE")

    op.bulk_insert(
        sa.table('artist',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('country', sa.String),
            sa.column('debut_year', sa.SmallInteger)
        ),
        [
            {'id': 1, 'name': 'Metallica', 'country': 'USA', 'debut_year': 1981},
            {'id': 2, 'name': 'Iron Maiden', 'country': 'UK', 'debut_year': 1975},
            {'id': 3, 'name': 'Pink Floyd', 'country': 'UK', 'debut_year': 1965},
            {'id': 4, 'name': 'Nirvana', 'country': 'USA', 'debut_year': 1987},
            {'id': 5, 'name': 'Black Sabbath', 'country': 'UK', 'debut_year': 1968},
            {'id': 6, 'name': 'AC/DC', 'country': 'Australia', 'debut_year': 1973},
            {'id': 7, 'name': 'Deep Purple', 'country': 'UK', 'debut_year': 1968},
            {'id': 8, 'name': 'Megadeth', 'country': 'USA', 'debut_year': 1983},
            {'id': 9, 'name': 'Pantera', 'country': 'USA', 'debut_year': 1981},
            {'id': 10, 'name': 'Slipknot', 'country': 'USA', 'debut_year': 1995}
        ]
    )

    op.bulk_insert(
        sa.table('genre',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String)
        ),
        [
            {'id': 1, 'name': 'Metal'},
            {'id': 2, 'name': 'Heavy Metal'},
            {'id': 3, 'name': 'Hard Rock'},
            {'id': 4, 'name': 'Alternative Rock'},
            {'id': 5, 'name': 'Grunge'},
            {'id': 6, 'name': 'Classic Rock'},
            {'id': 7, 'name': 'Thrash Metal'},
            {'id': 8, 'name': 'Groove Metal'},
            {'id': 9, 'name': 'Nu Metal'},
            {'id': 10, 'name': 'Jazz'}
        ]
    )

    op.bulk_insert(
        sa.table('song',
            sa.column('id', sa.Integer),
            sa.column('title', sa.String),
            sa.column('release_year', sa.SmallInteger),
            sa.column('duration', sa.SmallInteger),
            sa.column('artist_id', sa.Integer)
        ),
        [
            {'id': 1, 'title': 'Unforgiven', 'release_year': 1991, 'duration': 388, 'artist_id': 1},
            {'id': 2, 'title': 'The Trooper', 'release_year': 1983, 'duration': 256, 'artist_id': 2},
            {'id': 3, 'title': 'Smells Like Teen Spirit', 'release_year': 1991, 'duration': 301, 'artist_id': 4},
            {'id': 4, 'title': 'Something in the Way', 'release_year': 1991, 'duration': 232, 'artist_id': 4},
            {'id': 5, 'title': 'Paranoid', 'release_year': 1970, 'duration': 171, 'artist_id': 5},
            {'id': 6, 'title': 'Highway to Hell', 'release_year': 1979, 'duration': 208, 'artist_id': 6},
            {'id': 7, 'title': 'Symphony of Destruction', 'release_year': 1992, 'duration': 290, 'artist_id': 8},
            {'id': 8, 'title': 'Walk', 'release_year': 1992, 'duration': 330, 'artist_id': 9},
            {'id': 9, 'title': 'Duality', 'release_year': 2004, 'duration': 240, 'artist_id': 10},
            {'id': 10, 'title': 'Sic', 'release_year': 1999, 'duration': 193, 'artist_id': 10}
        
        ]
    )

    op.bulk_insert(
        sa.table('song_genre',
            sa.column('song_id', sa.Integer),
            sa.column('genre_id', sa.Integer)
        ),
        [
            {'song_id': 1, 'genre_id': 1},
            {'song_id': 1, 'genre_id': 3},
            {'song_id': 2, 'genre_id': 2},
            {'song_id': 3, 'genre_id': 5},
            {'song_id': 3, 'genre_id': 4},
            {'song_id': 4, 'genre_id': 5},
            {'song_id': 4, 'genre_id': 4},
            {'song_id': 5, 'genre_id': 2},
            {'song_id': 5, 'genre_id': 1},
            {'song_id': 6, 'genre_id': 3},
            {'song_id': 7, 'genre_id': 7},
            {'song_id': 8, 'genre_id': 8},
            {'song_id': 9, 'genre_id': 9},
            {'song_id': 9, 'genre_id': 1},
            {'song_id': 10, 'genre_id': 9},
            {'song_id': 10, 'genre_id': 1}
        ]
    )


    op.execute("SELECT setval(pg_get_serial_sequence('artist', 'id'), (SELECT MAX(id) FROM artist))")
    op.execute("SELECT setval(pg_get_serial_sequence('genre', 'id'), (SELECT MAX(id) FROM genre))")
    op.execute("SELECT setval(pg_get_serial_sequence('song', 'id'), (SELECT MAX(id) FROM song))")

def downgrade():
    op.execute("DELETE FROM song_genre")
    op.execute("DELETE FROM song")
    op.execute("DELETE FROM genre")
    op.execute("DELETE FROM artist")
