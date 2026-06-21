"""Create phone number for user column

Revision ID: 2463d73f7e1d
Revises: 
Create Date: 2026-06-18 19:03:57.940497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2463d73f7e1d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: adds a user phone # column"""
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema: Removes user column for phone # from users table"""
    op.drop_column("users", "phone_number")
    pass
