"""seed_initial_data

Revision ID: b9dc56ebffae
Revises: 0f8a9cafc62e
Create Date: 2025-03-17 10:00:43.817229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9dc56ebffae'
down_revision: Union[str, None] = '0f8a9cafc62e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("TRUNCATE TABLE eav RESTART IDENTITY CASCADE")
    op.execute("TRUNCATE TABLE product RESTART IDENTITY CASCADE")

    op.bulk_insert(
        sa.table('product',
            sa.column('id', sa.Integer),
            sa.column('title', sa.String),
            sa.column('price', sa.String),
            sa.column('battery_capacity', sa.SmallInteger)
        ),
        [
            {'id': 1, 'title': 'Google Pixel 9', 'price': '900', 'battery_capacity': 4700},
            {'id': 2, 'title': 'Ninebot KickScooter E2', 'price': '250', 'battery_capacity': 10200},
            {'id': 3, 'title': 'Kugoo Kirin G1 Pro', 'price': '1100', 'battery_capacity': 23400},
            {'id': 4, 'title': 'Ninebot Kickscooter MAX G2', 'price': '600', 'battery_capacity': 15300},
            {'id': 5, 'title': 'Iphone 15', 'price': '700', 'battery_capacity': 3349},
            {'id': 6, 'title': 'JBL PARTYBOX 310', 'price': '500', 'battery_capacity': 1040},
            {'id': 7, 'title': 'Marshall Middleton', 'price': '350', 'battery_capacity': 3200},
            {'id': 8, 'title': 'Samsung Galaxy S24 Ultra', 'price': '1200', 'battery_capacity': 5000},
            {'id': 9, 'title': 'Xiaomi 14 Pro', 'price': '850', 'battery_capacity': 4880},
            {'id': 10, 'title': 'Sony Xperia 1 V', 'price': '1100', 'battery_capacity': 5000},
        ]
    )

    op.bulk_insert(
        sa.table('eav',
            sa.column('entity', sa.Integer),
            sa.column('attribute', sa.String),
            sa.column('value', sa.String),
        ),
        [
            {'enitity': 1, 'attribute': 'diagonal', 'value': '6.3'},
            {'enitity': 1, 'attribute': 'camera_in_megapixels', 'value': '50+48'},
            {'enitity': 1, 'attribute': 'central_processor_unit', 'value': 'Google Tensor G4'},
            {'enitity': 1, 'attribute': 'operating_system', 'value': 'Android 14'},

            {'enitity': 2, 'attribute': 'max_speed', 'value': '20'},
            {'enitity': 2, 'attribute': 'wheel_size', 'value': '8.1'},
            {'enitity': 2, 'attribute': 'max_weight', 'value': '90'},
            {'enitity': 2, 'attribute': 'drive', 'value': 'Front wheel'},

            {'entity': 3, 'attribute': 'max_speed', 'value': '70'},
            {'entity': 3, 'attribute': 'wheel_size', 'value': '11'},
            {'entity': 3, 'attribute': 'max_weight', 'value': '150'},
            {'entity': 3, 'attribute': 'drive', 'value': 'Full'},

            {'entity': 4, 'attribute': 'max_speed', 'value': '25'},
            {'entity': 4, 'attribute': 'wheel_size', 'value': '10'},
            {'entity': 4, 'attribute': 'max_weight', 'value': '120'},
            {'entity': 4, 'attribute': 'drive', 'value': 'Rear wheel'},

            {'entity': 5, 'attribute': 'diagonal', 'value': '6.1'},
            {'entity': 5, 'attribute': 'camera_in_megapixels', 'value': '48+12'},
            {'entity': 5, 'attribute': 'central_processor_unit', 'value': 'Apple A16 Bionic'},
            {'entity': 5, 'attribute': 'operating_system', 'value': 'iOS 17'},

            {'entity': 6, 'attribute': 'power_output', 'value': '240'},
            {'entity': 6, 'attribute': 'water_resistance', 'value': 'IPX4'},
            {'entity': 6, 'attribute': 'bluetooth_version', 'value': '5.1'},
            {'entity': 6, 'attribute': 'weight', 'value': '17.42'},

            {'entity': 7, 'attribute': 'power_output', 'value': '50'},
            {'entity': 7, 'attribute': 'water_resistance', 'value': 'IP67'},
            {'entity': 7, 'attribute': 'bluetooth_version', 'value': '5.1'},
            {'entity': 7, 'attribute': 'weight', 'value': '1.8'},

            {'entity': 8, 'attribute': 'diagonal', 'value': '6.8'},
            {'entity': 8, 'attribute': 'camera_in_megapixels', 'value': '200+50+12+10'},
            {'entity': 8, 'attribute': 'central_processor_unit', 'value': 'Snapdragon 8 Gen 3'},
            {'entity': 8, 'attribute': 'operating_system', 'value': 'Android 14'},

            {'entity': 9, 'attribute': 'diagonal', 'value': '6.73'},
            {'entity': 9, 'attribute': 'camera_in_megapixels', 'value': '50+50+50'},
            {'entity': 9, 'attribute': 'central_processor_unit', 'value': 'Snapdragon 8 Gen 3'},
            {'entity': 9, 'attribute': 'operating_system', 'value': 'HyperOS (Android 14)'},

            {'entity': 10, 'attribute': 'diagonal', 'value': '6.5'},
            {'entity': 10, 'attribute': 'camera_in_megapixels', 'value': '52+12+12'},
            {'entity': 10, 'attribute': 'central_processor_unit', 'value': 'Snapdragon 8 Gen 2'},
            {'entity': 10, 'attribute': 'operating_system', 'value': 'Android 13'},

        ]
    )


def downgrade() -> None:
    pass
