"""Add plugin.revision

Revision ID: d80f02824047
Revises: e7e633bd6fa2
Create Date: 2025-05-02 16:08:57.078114

"""

from alembic import op
import sqlalchemy as sa
from alembic import op
import sqlalchemy as sa
from zou.migrations.utils.base import BaseMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.session import Session


# revision identifiers, used by Alembic.
revision = "d80f02824047"
down_revision = "e7e633bd6fa2"
branch_labels = None
depends_on = None

base = declarative_base()


class Task(base, BaseMixin):
    """
    Describes a task done by a CG artist on an entity of the CG production.
    The task has a state and assigned to people. It handles notion of time like
    duration, start date and end date.
    """

    __tablename__ = "task"
    name = sa.Column(sa.String(80), nullable=False)
    description = sa.Column(sa.Text())

    priority = sa.Column(sa.Integer, default=0)
    difficulty = sa.Column(sa.Integer, default=3, nullable=False)
    duration = sa.Column(sa.Float, default=0)
    estimation = sa.Column(sa.Float, default=0)
    completion_rate = sa.Column(sa.Integer, default=0)
    retake_count = sa.Column(sa.Integer, default=0)
    sort_order = sa.Column(sa.Integer, default=0)
    start_date = sa.Column(sa.DateTime)
    due_date = sa.Column(sa.DateTime)
    real_start_date = sa.Column(sa.DateTime)
    end_date = sa.Column(sa.DateTime)
    done_date = sa.Column(sa.DateTime)
    last_comment_date = sa.Column(sa.DateTime)
    nb_assets_ready = sa.Column(sa.Integer, default=0)
    data = sa.Column(JSONB)
    nb_drawings = sa.Column(sa.Integer, default=0)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("plugin", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("revision", sa.String(length=12), nullable=True)
        )

    with op.batch_alter_table("salary_scale", schema=None) as batch_op:
        batch_op.alter_column(
            "position", existing_type=sa.VARCHAR(length=255), nullable=True
        )
        batch_op.alter_column(
            "seniority", existing_type=sa.VARCHAR(length=255), nullable=True
        )

    with op.batch_alter_table("task", schema=None) as batch_op:
        session = Session(bind=op.get_bind())
        session.query(Task).where(Task.difficulty == None).update(
            {
                Task.difficulty: 3,
            }
        )
        session.commit()
        batch_op.alter_column(
            "difficulty",
            existing_type=sa.INTEGER(),
            nullable=False,
            existing_server_default=sa.text("3"),
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("task", schema=None) as batch_op:
        batch_op.alter_column(
            "difficulty",
            existing_type=sa.INTEGER(),
            nullable=True,
            existing_server_default=sa.text("3"),
        )

    with op.batch_alter_table("salary_scale", schema=None) as batch_op:
        batch_op.alter_column(
            "seniority", existing_type=sa.VARCHAR(length=255), nullable=False
        )
        batch_op.alter_column(
            "position", existing_type=sa.VARCHAR(length=255), nullable=False
        )

    with op.batch_alter_table("plugin", schema=None) as batch_op:
        batch_op.drop_column("revision")

    # ### end Alembic commands ###
