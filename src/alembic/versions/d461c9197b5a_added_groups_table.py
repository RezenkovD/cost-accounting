"""Added groups table

Revision ID: d461c9197b5a
Revises: f5aaf1bf978b
Create Date: 2023-01-22 17:06:55.315270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d461c9197b5a"
down_revision = "f5aaf1bf978b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("group_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_groups_id"), "groups", ["id"], unique=False)
    op.create_index(op.f("ix_groups_title"), "groups", ["title"], unique=True)
    op.create_table(
        "users_group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_group_group_id"), "users_group", ["group_id"], unique=False
    )
    op.create_index(op.f("ix_users_group_id"), "users_group", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_group_user_id"), "users_group", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_group_user_id"), table_name="users_group")
    op.drop_index(op.f("ix_users_group_id"), table_name="users_group")
    op.drop_index(op.f("ix_users_group_group_id"), table_name="users_group")
    op.drop_table("users_group")
    op.drop_index(op.f("ix_groups_title"), table_name="groups")
    op.drop_index(op.f("ix_groups_id"), table_name="groups")
    op.drop_table("groups")
    # ### end Alembic commands ###
