"""views

Revision ID: a0dd5760c882
Revises: 0e414b42c50e
Create Date: 2025-01-29 13:21:06.127659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0dd5760c882'
down_revision: Union[str, None] = '0e414b42c50e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


#убрать {} и кавычки
def upgrade():
    op.execute("""
        CREATE VIEW artist_info AS
        SELECT 
            a.id AS artist_id,
            a.name AS artist_name,
            a.country AS country,
            a.debut_year AS debut_year,
            COALESCE(STRING_AGG(DISTINCT g.name, ', '), '') AS genres
        FROM 
            artist a
        LEFT JOIN 
            song s ON a.id = s.artist_id
        LEFT JOIN 
            song_genre sg ON s.id = sg.song_id
        LEFT JOIN 
            genre g ON sg.genre_id = g.id
        GROUP BY 
            a.id, a.name, a.country, a.debut_year;
    """)

#null заменить на 0
    op.execute("""
        CREATE MATERIALIZED VIEW song_stats AS
        SELECT 
            a.id AS artist_id,
            a.name AS artist_name,
            COUNT(s.id) AS total_songs,
            COALESCE(ROUND(AVG(s.duration),1), 0) AS avg_duration,
            RANK() OVER (ORDER BY COALESCE(AVG(s.duration), 0) DESC NULLS LAST) AS rank_by_duration
            FROM 
            artist a
        LEFT JOIN 
            song s ON a.id = s.artist_id
        GROUP BY 
            a.id, a.name;
    """)

def downgrade():
    op.execute("DROP VIEW artist_info;")
    op.execute("DROP MATERIALIZED VIEW song_stats;")

