"""Create Tree table

Revision ID: 632a3427406c
Revises: 
Create Date: 2024-11-13 12:08:37.263675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '632a3427406c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'neighbor_tree',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('parent_id', sa.Integer, sa.ForeignKey('neighbor_tree.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True),
        sa.CheckConstraint('LENGTH(BTRIM(title)) > 0', name='check_title_not_empty_string'),
        sa.CheckConstraint('BTRIM(title) = title', name='check_title_without_spaces'),
    )

def downgrade():
    op.drop_table('neighbor_tree')
