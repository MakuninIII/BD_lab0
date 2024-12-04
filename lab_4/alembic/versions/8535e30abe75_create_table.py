"""create_table

Revision ID: 8535e30abe75
Revises: 
Create Date: 2024-11-27 09:49:31.460757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8535e30abe75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
            'path_enum',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('path', sa.String(length=255), nullable=False),
            sa.CheckConstraint('LENGTH(BTRIM(title)) > 0', name='check_title_not_empty_string'),
            sa.CheckConstraint('BTRIM(title) = title', name='check_title_without_spaces'),
        )

def downgrade() -> None:
    op.drop_table('path_enum')