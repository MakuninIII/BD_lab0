"""eav_to_supertable

Revision ID: 7b1e2598993b
Revises: b9dc56ebffae
Create Date: 2025-03-17 10:59:15.121656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b1e2598993b'
down_revision: Union[str, None] = 'b9dc56ebffae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    connection = op.get_bind()
    
    result = connection.execute(sa.text("SELECT DISTINCT attribute, value FROM eav"))
    attributes = {}
    
    for attr, value in result:
        if attr not in attributes:
            if value.isdigit():
                attributes[attr] = 'INTEGER'
            elif value.replace('.', '', 1).isdigit():
                attributes[attr] = 'FLOAT'
            else:
                attributes[attr] = 'TEXT'   
    
    columns = ["id INTEGER PRIMARY KEY", "title TEXT", "price TEXT", "battery_capacity INTEGER"]
    for attr, dtype in attributes.items():
        columns.append(f'"{attr}" {dtype}')
    
    op.execute(f"CREATE TABLE {SUPER_TABLE_NAME} ({', '.join(columns)})")
    
    op.execute(f"INSERT INTO {SUPER_TABLE_NAME} (id, title, price, battery_capacity) SELECT id, title, price, battery_capacity FROM product")
    
    for attr in attributes.keys():
        op.execute(f"UPDATE {SUPER_TABLE_NAME} SET \"{attr}\" = (SELECT value FROM eav WHERE eav.entity = {SUPER_TABLE_NAME}.id AND eav.attribute = '{attr}')")
    

def downgrade():    
    op.execute(f"DROP TABLE {SUPER_TABLE_NAME}")
