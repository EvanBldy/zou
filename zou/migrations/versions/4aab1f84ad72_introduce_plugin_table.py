"""Introduce Plugin table

Revision ID: 4aab1f84ad72
Revises: d25118cddcaa
Create Date: 2025-04-14 15:18:29.346896

"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "4aab1f84ad72"
down_revision = "d25118cddcaa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plugin",
        sa.Column("plugin_id", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("maintainer_name", sa.String(length=200), nullable=False),
        sa.Column(
            "maintainer_email",
            sqlalchemy_utils.types.email.EmailType(length=255),
            nullable=True,
        ),
        sa.Column(
            "website", sqlalchemy_utils.types.url.URLType(), nullable=True
        ),
        sa.Column("license", sa.String(length=80), nullable=False),
        sa.Column(
            "id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("plugin", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_plugin_name"), ["name"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_plugin_plugin_id"), ["plugin_id"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("plugin", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_plugin_plugin_id"))
        batch_op.drop_index(batch_op.f("ix_plugin_name"))

    op.drop_table("plugin")
    # ### end Alembic commands ###
