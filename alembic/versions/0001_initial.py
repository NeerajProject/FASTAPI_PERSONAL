"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-04-30 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=256), nullable=False),
        sa.Column("full_name", sa.String(length=256), nullable=False),
        sa.Column("password_hash", sa.String(length=256), nullable=False),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)

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
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
