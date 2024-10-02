"""Seed initial data

Revision ID: seed_data_id
Revises: unique_id_here
Create Date: 2024-10-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'seed_data_id'
down_revision = 'unique_id_here'
branch_labels = None
depends_on = None

def upgrade():
    op.bulk_insert(
        sa.table('artist',
            sa.column('name', sa.String),
            sa.column('country', sa.String),
            sa.column('debut_year', sa.Integer)
        ),
        [
            {'name': 'Metallica', 'country': 'USA', 'debut_year': 1981},
            {'name': 'Iron Maiden', 'country': 'UK', 'debut_year': 1975},
            {'name': 'Pink Floyd', 'country': 'UK', 'debut_year': 1965},
            {'name': 'Nirvana', 'country': 'USA', 'debut_year': 1987},
            {'name': 'Black Sabbath', 'country': 'UK', 'debut_year': 1968},
            {'name': 'AC/DC', 'country': 'Australia', 'debut_year': 1973},
            {'name': 'Deep Purple', 'country': 'UK', 'debut_year': 1968},
            {'name': 'Megadeth', 'country': 'USA', 'debut_year': 1983},
            {'name': 'Pantera', 'country': 'USA', 'debut_year': 1981},
            {'name': 'Slipknot', 'country': 'USA', 'debut_year': 1995}
        ]
    )

    op.bulk_insert(
        sa.table('genre',
            sa.column('name', sa.String)
        ),
        [
            {'name': 'Metal'},
            {'name': 'Heavy Metal'},
            {'name': 'Hard Rock'},
            {'name': 'Alternative Rock'},
            {'name': 'Grunge'},
            {'name': 'Classic Rock'},
            {'name': 'Thrash Metal'},
            {'name': 'Groove Metal'},
            {'name': 'Nu Metal'},
            {'name': 'Jazz'},
        ]
    )

    op.bulk_insert(
        sa.table('song',
            sa.column('title', sa.String),
            sa.column('release_year', sa.Integer),
            sa.column('duration', sa.Integer),
            sa.column('artist_id', sa.Integer)
        ),
        [
            {'title': 'Unforgiven', 'release_year': 1991, 'duration': 388, 'artist_id': 1},
            {'title': 'The Trooper', 'release_year': 1983, 'duration': 256, 'artist_id': 2},
            {'title': 'Smells Like Teen Spirit', 'release_year': 1991, 'duration': 301, 'artist_id': 4},
            {'title': 'Something in the Way', 'release_year': 1991, 'duration': 232, 'artist_id': 4},
            {'title': 'Paranoid', 'release_year': 1970, 'duration': 171, 'artist_id': 5},
            {'title': 'Highway to Hell', 'release_year': 1979, 'duration': 208, 'artist_id': 6},
            {'title': 'Symphony of Destruction', 'release_year': 1992, 'duration': 290, 'artist_id': 8},
            {'title': 'Walk', 'release_year': 1992, 'duration': 330, 'artist_id': 9},
            {'title': 'Duality', 'release_year': 2004, 'duration': 240, 'artist_id': 10},
            {'title': 'Sic', 'release_year': 1999, 'duration': 193, 'artist_id': 10}

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

def downgrade():
    op.execute("DELETE FROM song_genre")
    op.execute("DELETE FROM song")
    op.execute("DELETE FROM genre")
    op.execute("DELETE FROM artist")
