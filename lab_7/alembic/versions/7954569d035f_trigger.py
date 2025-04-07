"""trigger

Revision ID: 7954569d035f
Revises: 48cc4cf32d2e
Create Date: 2025-02-16 23:51:02.665805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7954569d035f'
down_revision: Union[str, None] = '48cc4cf32d2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION normalize_artist_name() 
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.name := INITCAP(TRIM(BOTH FROM REGEXP_REPLACE(NEW.name, '\s+', ' ', 'g')));
            
            NEW.country := UPPER(TRIM(BOTH FROM REGEXP_REPLACE(REGEXP_REPLACE(NEW.country, '[0-9]', '', 'g'), '\s+', ' ', 'g')));

            IF NEW.debut_year < 1860 THEN
               NEW.debut_year := 1860;
            ELSIF NEW.debut_year > EXTRACT(YEAR FROM CURRENT_DATE) THEN
               NEW.debut_year := EXTRACT(YEAR FROM CURRENT_DATE);
            END IF;
               
            RETURN NEW;
            
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER artist_name_format
        BEFORE INSERT OR UPDATE ON artist
        FOR EACH ROW EXECUTE FUNCTION normalize_artist_name();
    """)
    
def downgrade() -> None:
    op.execute("""
        DROP TRIGGER IF EXISTS artist_name_format ON artist;
        DROP FUNCTION IF EXISTS normalize_artist_name;
    """)