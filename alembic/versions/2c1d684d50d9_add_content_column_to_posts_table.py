"""add content column to posts table

Revision ID: 2c1d684d50d9
Revises: b650fe8620cf
Create Date: 2025-12-25 13:09:07.318424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c1d684d50d9'
down_revision: Union[str, Sequence[str], None] = 'b650fe8620cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
