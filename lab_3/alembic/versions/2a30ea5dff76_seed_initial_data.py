"""Seed initial data

Revision ID: 2a30ea5dff76
Revises: 632a3427406c
Create Date: 2024-11-13 12:17:01.025870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a30ea5dff76'
down_revision: Union[str, None] = '632a3427406c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("TRUNCATE TABLE neighbor_tree RESTART IDENTITY")

    op.bulk_insert(
        sa.table('neighbor_tree',
            sa.Column('id', sa.Integer),
            sa.Column('title', sa.String),
            sa.Column('parent_id', sa.Integer,)
        ),
        [
            {'id': 1, 'title': 'Кибератаки', 'parent_id': None},
            {'id': 2, 'title': 'Пассивные', 'parent_id': 1},
            {'id': 3, 'title': 'Активные', 'parent_id': 1},
            {'id': 4, 'title': 'Анализ трафика', 'parent_id': 2},
            {'id': 5, 'title': 'Пассивное сканирование', 'parent_id': 2},
            {'id': 6, 'title': 'Наблюдение за сетевыми соединениями', 'parent_id': 2},
            {'id': 7, 'title': 'Активный сбор информации', 'parent_id': 3},
            {'id': 8, 'title': 'Нарушение работы (служб, узлов, сетей)', 'parent_id': 3},
            {'id': 9, 'title': 'Без последствий', 'parent_id': 3},
            {'id': 10, 'title': 'Работа со службой', 'parent_id': 7},
            {'id': 11, 'title': 'Сканирование', 'parent_id': 7},
            {'id': 12, 'title': 'Атака для получения информации', 'parent_id': 7},
            {'id': 13, 'title': 'Открытое сканирование', 'parent_id': 10},
            {'id': 14, 'title': 'Полуоткрытое сканирование', 'parent_id': 10},
            {'id': 15, 'title': 'Открытое сканирование', 'parent_id': 11},
            {'id': 16, 'title': 'Полуоткрытое сканирование', 'parent_id': 11},
            {'id': 17, 'title': 'Фишинг', 'parent_id': 12},
            {'id': 18, 'title': 'Социальная инженерия', 'parent_id': 12},
            {'id': 19, 'title': 'Спуфинг', 'parent_id': 12},
            {'id': 20, 'title': 'Изменение алгоритма функционирования', 'parent_id': 8},
            {'id': 21, 'title': 'Отказ в обслуживании', 'parent_id': 8},
            {'id': 22, 'title': 'Подмена конфигурации', 'parent_id': 8},
            {'id': 23, 'title': 'Подмена данных', 'parent_id': 20},
            {'id': 24, 'title': 'Внедрение вредоносного ПО', 'parent_id': 20},
            {'id': 25, 'title': 'DDoS атака', 'parent_id': 21},
            {'id': 26, 'title': 'SQL-инъекция', 'parent_id': 21},
            {'id': 27, 'title': 'XML-бомба', 'parent_id': 21},
            {'id': 28, 'title': 'Изменение сетевых маршрутов', 'parent_id': 22},
            {'id': 29, 'title': 'Изменение параметров служб', 'parent_id': 22},
            {'id': 30, 'title': 'Тестирование безопасности', 'parent_id': 9},
            {'id': 31, 'title': 'Проверка уязвимостей', 'parent_id': 9},
            {'id': 32, 'title': 'Анализ настроек', 'parent_id': 9},
        ]
    )


    op.execute("SELECT SETVAL(pg_get_serial_sequence('neighbor_tree', 'id'), MAX(id)) FROM neighbor_tree")          

def downgrade():
    op.execute("DELETE FROM neighbor_tree")


