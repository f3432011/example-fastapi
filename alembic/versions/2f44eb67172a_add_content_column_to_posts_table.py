"""add content column to posts table

Revision ID: 2f44eb67172a
Revises: 957a5b16c735
Create Date: 2025-09-08 12:12:25.607038

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f44eb67172a"
down_revision: Union[str, Sequence[str], None] = "957a5b16c735"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
