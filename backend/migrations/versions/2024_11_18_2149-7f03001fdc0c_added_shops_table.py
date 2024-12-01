"""added: shops table

Revision ID: 7f03001fdc0c
Revises: 
Create Date: 2024-11-18 21:49:55.233116

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7f03001fdc0c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create schema backend")
    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="backend",
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=256), nullable=True),
        sa.Column("price", sa.Numeric(precision=9, scale=2), nullable=True),
        sa.Column("is_purchased", sa.Boolean(), nullable=False),
        sa.Column("buy_date", sa.Date(), nullable=True),
        sa.Column("guarantee", sa.Integer(), nullable=False),
        sa.Column("guarantee_end_date", sa.Date(), nullable=True),
        sa.Column("receipt", sa.String(length=1024), nullable=True),
        sa.Column("product_link", sa.String(length=2048), nullable=True),
        sa.Column("shop_id", sa.Integer(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shop_id"],
            ["backend.shops.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="backend",
    )


def downgrade() -> None:
    op.drop_table("products", schema="backend")
    op.drop_table("shops", schema="backend")
    op.execute("drop schema backend")
