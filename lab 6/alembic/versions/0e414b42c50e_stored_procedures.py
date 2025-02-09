"""stored procedures

Revision ID: 0e414b42c50e
Revises: a9087a7e4b07
Create Date: 2025-01-29 13:20:26.972061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e414b42c50e'
down_revision: Union[str, None] = 'a9087a7e4b07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""CREATE OR REPLACE PROCEDURE genreCreate(name_ varchar(255))
                    LANGUAGE plpgsql
                    AS $$
                    DECLARE
                        new_genre_id INT;
                    BEGIN
                        IF LENGTH(BTRIM(name_)) = 0 THEN
                            RAISE EXCEPTION 'Название жанра не может быть пустой строкой или состоять только из пробелов.';
                        END IF;
               
                        INSERT INTO genre(name)
                        VALUES (BTRIM(name_))
                        RETURNING id INTO new_genre_id;
                        RAISE NOTICE 'Жанр % успешно добавлен c ID %.', name_, new_genre_id; 

                    EXCEPTION
                        WHEN unique_violation THEN
                            RAISE EXCEPTION 'Ошибка уникальности: Жанр % уже существует.', name_;
                    END;     
                    $$;
               """)

    op.execute("""CREATE OR REPLACE FUNCTION genreRetrieveAll()
               RETURNS TABLE(id INT, name varchar(255))
               LANGUAGE plpgsql
               AS $$
               BEGIN
                    RETURN QUERY
                    SELECT * FROM genre;
               END;
               $$;
                """)
    
    op.execute(""" CREATE OR REPLACE FUNCTION genreRetrieve(genre_id integer)
                RETURNS TABLE(id INT, name varchar(255))
                LANGUAGE plpgsql
                As $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM genre g WHERE g.id = genre_id) THEN
                        RAISE EXCEPTION 'Жанр с ID % не существует.', genre_id;
                    END IF;
               
                    RETURN QUERY
                    SELECT g.id, g.name
                    FROM genre g
                    WHERE g.id = genre_id;
                END;
                $$;
                """)
    
    op.execute("""
        CREATE OR REPLACE PROCEDURE genreUpdate(genre_id INT, name_ varchar(255))
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF LENGTH(BTRIM(name_)) = 0 THEN
                RAISE EXCEPTION 'Название жанра не может быть пустым.';
            END IF;
            
            IF NOT EXISTS (SELECT 1 FROM genre WHERE genre.id = genre_id) THEN
                RAISE EXCEPTION 'Жанр с ID % не существует.', genre_id;
            END IF;
            
            UPDATE genre
            SET name = BTRIM(name_)
            WHERE genre.id = genre_id;
            RAISE NOTICE 'Жанр с ID % обновлен.', genre_id;
        END;
        $$;
    """)

    op.execute("""
        CREATE OR REPLACE PROCEDURE genreDelete(genre_id INT)
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM genre g WHERE g.id = genre_id) THEN
                RAISE EXCEPTION 'Жанр с ID % не существует.', genre_id;
            END IF;
            
            DELETE FROM genre
            WHERE genre.id = genre_id;
            RAISE NOTICE 'Жанр с ID % успешно удален.', genre_id;
        END;
        $$;
    """)

op.execute("""
            CREATE OR REPLACE PROCEDURE genreDeleteMany(ids text)
            LANGUAGE plpgsql
            AS $$
            DECLARE
                existing_ids text;
                nonexistent_ids text;
            BEGIN
                SELECT string_agg(id::text, ',') 
                INTO existing_ids
                FROM genre
                WHERE id = ANY(string_to_array(ids, ',')::int[]);

                SELECT string_agg(id::text, ',') 
                INTO nonexistent_ids
                FROM unnest(string_to_array(ids, ',')::int[]) id
                WHERE id::int NOT IN (SELECT id FROM genre);

                IF existing_ids IS NULL THEN
                    RAISE EXCEPTION 'Ни одного из указанных ID % не существует.', ids;
                    RETURN;
                END IF;

                EXECUTE 'DELETE FROM genre WHERE id IN (' || existing_ids || ')';

                IF nonexistent_ids IS NOT NULL THEN
                    RAISE NOTICE 'Удалены существующие ID: %. Не найдены ID: %.', existing_ids, nonexistent_ids;
                ELSE
                    RAISE NOTICE 'Удалены все указанные ID: %.', existing_ids;
                END IF;
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE EXCEPTION 'Произошла ошибка при удалении нескольких жанров: %', SQLERRM;
            END;
            $$;
           """)


def downgrade() -> None:
    op.execute("DROP PROCEDURE IF EXISTS genreCreate;")
    op.execute("DROP FUNCTION IF EXISTS genreRetrieveAll;")
    op.execute("DROP FUNCTION IF EXISTS genreRetrieve;")
    op.execute("DROP PROCEDURE IF EXISTS genreUpdate;")
    op.execute("DROP PROCEDURE IF EXISTS genreDelete;")
    op.execute("DROP PROCEDURE IF EXISTS genreDeleteMany;")
