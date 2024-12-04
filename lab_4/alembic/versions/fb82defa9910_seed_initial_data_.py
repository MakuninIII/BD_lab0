"""seed_initial_data_

Revision ID: fb82defa9910
Revises: 8535e30abe75
Create Date: 2024-11-27 09:50:11.336990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb82defa9910'
down_revision: Union[str, None] = '8535e30abe75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("TRUNCATE TABLE path_enum RESTART IDENTITY")

    op.bulk_insert(
        sa.table('path_enum',
            sa.Column('id', sa.Integer),
            sa.Column('title', sa.String),
            sa.Column('path', sa.String,)
        ),
        [
            {'id': 1, 'title': 'Кибератаки', 'path': '1/'},
            {'id': 2, 'title': 'Пассивные', 'path': '1/2/'},
            {'id': 3, 'title': 'Активные', 'path': '1/3/'},
            {'id': 4, 'title': 'Анализ трафика', 'path': '1/2/4/'},
            {'id': 5, 'title': 'Пассивное сканирование', 'path': '1/2/5/'},
            {'id': 6, 'title': 'Наблюдение за сетевыми соединениями', 'path': '1/2/6/'},
            {'id': 7, 'title': 'Активный сбор информации', 'path': '1/3/7/'},
            {'id': 8, 'title': 'Нарушение работы (служб, узлов, сетей)', 'path': '1/3/8/'},
            {'id': 9, 'title': 'Без последствий', 'path': '1/3/9/'},
            {'id': 10, 'title': 'Работа со службой', 'path': '1/3/7/10/'},
            {'id': 11, 'title': 'Сканирование', 'path': '1/3/7/11/'},
            {'id': 12, 'title': 'Атака для получения информации', 'path': '1/3/7/12/'},
            {'id': 13, 'title': 'Открытое сканирование', 'path': '1/3/7/10/13/'},
            {'id': 14, 'title': 'Полуоткрытое сканирование', 'path': '1/3/7/10/14/'},
            {'id': 15, 'title': 'Открытое сканирование', 'path': '1/3/7/11/15/'},
            {'id': 16, 'title': 'Полуоткрытое сканирование', 'path': '1/3/7/11/16/'},
            {'id': 17, 'title': 'Фишинг', 'path': '1/3/7/12/17/'},
            {'id': 18, 'title': 'Социальная инженерия', 'path': '1/3/7/12/18/'},
            {'id': 19, 'title': 'Спуфинг', 'path': '1/3/7/12/19/'},
            {'id': 20, 'title': 'Изменение алгоритма функционирования', 'path': '1/3/8/20/'},
            {'id': 21, 'title': 'Отказ в обслуживании', 'path': '1/3/8/21/'},
            {'id': 22, 'title': 'Подмена конфигурации', 'path': '1/3/8/22/'},
            {'id': 23, 'title': 'Подмена данных', 'path': '1/3/8/20/23/'},
            {'id': 24, 'title': 'Внедрение вредоносного ПО', 'path': '1/3/8/20/24/'},
            {'id': 25, 'title': 'DDoS атака', 'path': '1/3/8/21/25/'},
            {'id': 26, 'title': 'SQL-инъекция', 'path': '1/3/8/21/26/'},
            {'id': 27, 'title': 'XML-бомба', 'path': '1/3/8/21/27/'},
            {'id': 28, 'title': 'Изменение сетевых маршрутов', 'path': '1/3/8/22/28/'},
            {'id': 29, 'title': 'Изменение параметров служб', 'path': '1/3/8/22/29/'},
            {'id': 30, 'title': 'Тестирование безопасности', 'path': '1/3/9/30/'},
            {'id': 31, 'title': 'Проверка уязвимостей', 'path': '1/3/9/31/'},
            {'id': 32, 'title': 'Анализ настроек', 'path': '1/3/9/32/'},
        ]
    )


    op.execute("SELECT SETVAL(pg_get_serial_sequence('path_enum', 'id'), MAX(id)) FROM path_enum")          


def downgrade() -> None:
    op.execute("DELETE FROM path_enum")