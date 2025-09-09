"""create posts table

Revision ID: 957a5b16c735
Revises:
Create Date: 2025-09-08 11:17:54.072640

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "957a5b16c735"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    # # Users table
    # op.create_table(
    #     "users",
    #     sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    #     sa.Column("email", sa.String, nullable=False, unique=True),
    #     sa.Column("password", sa.String, nullable=False),
    #     sa.Column(
    #         "created_at",
    #         sa.TIMESTAMP(timezone=True),
    #         server_default=sa.text("now()"),
    #         nullable=False,
    #     ),
    # )

    # # Posts table
    # op.create_table(
    #     "posts",
    #     sa.Column("id", sa.Integer, primary_key=True, nullable=False),
    #     sa.Column("title", sa.String, nullable=False),
    #     sa.Column("content", sa.String, nullable=False),
    #     sa.Column("published", sa.Boolean, nullable=False, server_default="True"),
    #     sa.Column(
    #         "created_at",
    #         sa.TIMESTAMP(timezone=True),
    #         server_default=sa.text("now()"),
    #         nullable=False,
    #     ),
    #     sa.Column(
    #         "owner_id",
    #         sa.Integer,
    #         sa.ForeignKey("users.id", ondelete="CASCADE"),
    #         nullable=False,
    #     ),
    # )

    # # Votes table
    # op.create_table(
    #     "votes",
    #     sa.Column(
    #         "post_id",
    #         sa.Integer,
    #         sa.ForeignKey("posts.id", ondelete="CASCADE"),
    #         primary_key=True,
    #         nullable=False,
    #     ),
    #     sa.Column(
    #         "user_id",
    #         sa.Integer,
    #         sa.ForeignKey("users.id", ondelete="CASCADE"),
    #         primary_key=True,
    #         nullable=False,
    #     ),
    # )

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
    )
    pass


def downgrade():
    # op.drop_table("votes")
    # op.drop_table("posts")
    # op.drop_table("users")

    op.drop_table("posts")
