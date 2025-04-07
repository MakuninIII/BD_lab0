"""create_table

Revision ID: 0f8a9cafc62e
Revises: 
Create Date: 2025-03-17 09:46:18.547502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f8a9cafc62e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('price', sa.String(255), nullable=False),
        sa.Column('battery_capacity', sa.Integer, nullable=False),
        sa.CheckConstraint('LENGTH(BTRIM(title)) > 0', name='check_title_not_empty_string'),
        sa.CheckConstraint('BTRIM(title) = title', name='check_title_without_spaces'),
        sa.CheckConstraint('battery_capacity > 0', name='check_battery_capacity'),
    )

    op.create_table(
        'eav',
        sa.Column('entity', sa.Integer, sa.ForeignKey('product.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
        sa.Column('attribute', sa.String(255), nullable=False),
        sa.Column('value', sa.String(255), nullable=False),
        sa.CheckConstraint('entity > 0', name='check_entity'),
    )
    

def downgrade() -> None:
      op.drop_table('eav')
      op.drop_table('product')