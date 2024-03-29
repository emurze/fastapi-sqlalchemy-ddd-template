"""empty message

Revision ID: ff594bd0d569
Revises: 4867d2db76c7
Create Date: 2024-03-17 15:38:48.620380

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ff594bd0d569"
down_revision: Union[str, None] = "4867d2db76c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "post",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("content", sa.String(length=256), nullable=False),
        sa.Column("draft", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("client")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "client",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column(
            "title",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.VARCHAR(length=256),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("draft", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="client_pkey"),
    )
    op.drop_table("post")
    # ### end Alembic commands ###
