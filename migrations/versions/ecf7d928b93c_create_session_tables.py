"""creat_session_tables

Revision ID: ecf7d928b93c
Revises: 7a917825c189
Create Date: 2024-06-04 20:16:00.978676

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ecf7d928b93c"
down_revision: Union[str, None] = "7a917825c189"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "session",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by", sa.BigInteger(), nullable=False),
        sa.Column(
            "session_type",
            sa.Enum("SELF_PRACTICE", "GROUP", name="sessiontype"),
            server_default="SELF_PRACTICE",
            nullable=True,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "is_deleted", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_session_created_by"), "session", ["created_by"], unique=False
    )
    op.create_table(
        "self_practice_session",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("session_id", sa.Text(), nullable=False),
        sa.Column("topic_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "media_type",
            sa.Enum("AUDIO", "VIDEO", name="sessionmediatype"),
            server_default="AUDIO",
            nullable=True,
        ),
        sa.Column("session_recording_url", sa.Text(), nullable=True),
        sa.Column(
            "is_deleted", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["session.id"],
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topic.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("self_practice_session")
    op.drop_index(op.f("ix_session_created_by"), table_name="session")
    op.drop_table("session")
    sa.Enum(name="sessiontype").drop(op.get_bind())
    sa.Enum(name="sessionmediatype").drop(op.get_bind())
    # ### end Alembic commands ###
