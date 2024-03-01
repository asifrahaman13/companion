"""Set enum types correctly

Revision ID: d7067d13464c
Revises: 4c08af871a9e
Create Date: 2024-02-27 10:09:10.976034

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "d7067d13464c"
down_revision = "4c08af871a9e"
branch_labels = None
depends_on = None

enum_type = sa.Enum("ADMIN", "USER", name="userscope")


def get_conn():
    return op.get_bind()


def get_inspector():
    return Inspector.from_engine(get_conn())


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = get_inspector()
    table_constraints = inspector.get_unique_constraints("user")
    constraint_names = {constraint["name"] for constraint in table_constraints}
    if "uq_user_id" not in constraint_names:
        op.create_unique_constraint("uq_user_id", "user", ["id"])
    op.alter_column("guideline", "creator_id", existing_type=sa.INTEGER(), nullable=False)
    table_constraints = inspector.get_foreign_keys("guideline")
    constraint_names = {constraint["name"] for constraint in table_constraints}
    if "fk_guideline_creator_id" not in constraint_names:
        op.create_foreign_key("fk_guideline_creator_id", "guideline", "user", ["creator_id"], ["id"])
    enum_type.create(op.get_bind(), checkfirst=True)
    op.execute(
        text("""
        ALTER TABLE "user"
        ALTER COLUMN scope TYPE userscope
        USING (CASE scope WHEN 'admin' THEN 'ADMIN'::userscope WHEN 'user' THEN 'USER'::userscope END)
    """)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = get_inspector()
    op.execute(
        text("""
        ALTER TABLE "user"
        ALTER COLUMN scope TYPE VARCHAR
        USING (CASE WHEN scope = 'ADMIN' THEN 'admin'::VARCHAR WHEN scope = 'USER' THEN 'user'::VARCHAR END)
    """)
    )
    enum_type.drop(get_conn(), checkfirst=True)
    table_constraints = inspector.get_foreign_keys("guideline")
    constraint_names = {constraint["name"] for constraint in table_constraints}
    if "fk_guideline_creator_id" in constraint_names:
        op.drop_constraint("fk_guideline_creator_id", "guideline", type_="foreignkey")
    op.alter_column("guideline", "creator_id", existing_type=sa.INTEGER(), nullable=True)
    table_constraints = inspector.get_unique_constraints("user")
    constraint_names = {constraint["name"] for constraint in table_constraints}
    if "uq_user_id" in constraint_names:
        op.drop_constraint("uq_user_id", "user", type_="unique")
    # ### end Alembic commands ###