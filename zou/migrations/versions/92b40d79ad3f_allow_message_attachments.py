"""allow attachment on messages

Revision ID: 92b40d79ad3f
Revises: 23122f290ca2
Create Date: 2024-03-08 01:35:16.127135

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "92b40d79ad3f"
down_revision = "23122f290ca2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("chat", schema=None) as batch_op:
        batch_op.drop_index("ix_chat_person_id")
        batch_op.drop_constraint("chat_person_id_fkey", type_="foreignkey")
        batch_op.drop_column("person_id")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    """
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('person_id', sa.UUID(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('chat_person_id_fkey', 'person', ['person_id'], ['id'])
        batch_op.create_index('ix_chat_person_id', ['person_id'], unique=False)
    """

    # ### end Alembic commands ###
