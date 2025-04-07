"""views_

Revision ID: 48cc4cf32d2e
Revises: 6aa061c1c6d4
Create Date: 2025-02-16 23:50:55.208691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48cc4cf32d2e'
down_revision: Union[str, None] = '6aa061c1c6d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



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

