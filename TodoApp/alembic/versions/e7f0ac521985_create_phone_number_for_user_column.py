"""Create phone number for user column

Revision ID: e7f0ac521985
Revises: 
Create Date: 2026-10-23 12:17:50.281347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7f0ac521985'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','phone_number')
