"""add food_items table

Revision ID: 0002_food_master
Revises: 0001_initial
Create Date: 2026-04-30 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_food_master"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "food_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=False),
        sa.Column("qty_gram", sa.Float(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
    )
    op.create_index(op.f("ix_food_items_id"), "food_items", ["id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_food_items_id"), table_name="food_items")
    op.drop_table("food_items")
