"""Create tables

Revision ID: unique_id_here
Revises: 
Create Date: 2024-10-02 23:38:11.776309

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'unique_id_here'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'artist',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('country', sa.String(255), nullable=False),
        sa.Column('debut_year', sa.SmallInteger, nullable=False),
        sa.CheckConstraint('debut_year >= 1860 AND debut_year <= EXCTRACT(YEAR FROM CURRENT_YEAR)', name='check_artist_debut_year')
    )

    op.create_table(
        'song',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('release_year', sa.SmallInteger, nullable=False),
        sa.Column('duration', sa.SmallInteger, nullable=False),
        sa.Column('artist_id', sa.Integer, sa.ForeignKey('artist.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        sa.CheckConstraint('release_year >= 1860 release_year <= EXCTRACT(YEAR FROM CURRENT_YEAR)', name='check_song_release_year'),
        sa.CheckConstraint('duration >= 0', name='check_song_duration')
    )

    op.create_table(
        'genre',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

    op.create_table(
        'song_genre',
        sa.Column('song_id', sa.Integer, sa.ForeignKey('song.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        sa.Column('genre_id', sa.Integer, sa.ForeignKey('genre.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint('song_id', 'genre_id')
    )

def downgrade():
    op.drop_table('song_genre')
    op.drop_table('genre')
    op.drop_table('song')
    op.drop_table('artist')
