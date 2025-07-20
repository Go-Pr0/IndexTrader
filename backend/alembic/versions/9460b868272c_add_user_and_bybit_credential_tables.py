"""Add user and bybit_credential tables

Revision ID: 9460b868272c
Revises: 9f1f6988ed65
Create Date: 2025-07-21 08:28:24.513467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9460b868272c'
down_revision: Union[str, Sequence[str], None] = '9f1f6988ed65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
