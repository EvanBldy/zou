"""For DepartmentLink index person_id / department_id

Revision ID: 539a3a00c417
Revises: 9d3bb33c6fc6
Create Date: 2025-01-14 12:19:52.699322

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "539a3a00c417"
down_revision = "9d3bb33c6fc6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("department_link", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "department_link_uc", ["person_id", "department_id"]
        )
        batch_op.create_index(
            batch_op.f("ix_department_link_department_id"),
            ["department_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_department_link_person_id"),
            ["person_id"],
            unique=False,
        )
        batch_op.create_primary_key(
            "department_link_pkey", ["person_id", "department_id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("department_link", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_department_link_person_id"))
        batch_op.drop_index(batch_op.f("ix_department_link_department_id"))
        batch_op.drop_constraint("department_link_uc", type_="unique")
        batch_op.drop_constraint("department_link_pkey", type_="primary")

    # ### end Alembic commands ###
