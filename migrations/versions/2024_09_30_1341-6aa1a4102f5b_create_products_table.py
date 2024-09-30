"""create products table

Revision ID: 6aa1a4102f5b
Revises: 
Create Date: 2024-09-30 13:41:28.392453

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6aa1a4102f5b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"create schema backend")
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=255), nullable=True),
        sa.Column("price", sa.Numeric(precision=9, scale=2), nullable=True),
        sa.Column("is_purchased", sa.Boolean(), nullable=False),
        sa.Column("buy_date", sa.Date(), nullable=True),
        sa.Column("guarantee", sa.Integer(), nullable=False),
        sa.Column("guarantee_end_date", sa.Date(), nullable=True),
        sa.Column("receipt", sa.String(), nullable=True),
        sa.Column("shop", sa.String(length=255), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="backend",
    )


def downgrade() -> None:
    op.drop_table("products", schema="backend")
    op.execute("drop schema backend")
