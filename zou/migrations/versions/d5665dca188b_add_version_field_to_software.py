"""add version field to software

Revision ID: d5665dca188b
Revises: 9683bd840dee
Create Date: 2025-07-14 12:44:29.378444

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d5665dca188b"
down_revision = "9683bd840dee"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("software", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("version", sa.String(length=20), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("software", schema=None) as batch_op:
        batch_op.drop_column("version")

    # ### end Alembic commands ###
