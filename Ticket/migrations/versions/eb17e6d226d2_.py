"""empty message

Revision ID: eb17e6d226d2
Revises: f149aa7a79f6
Create Date: 2024-06-02 11:57:16.351087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb17e6d226d2'
down_revision = 'f149aa7a79f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.alter_column('route',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('promotion', schema=None) as batch_op:
        batch_op.alter_column('route',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###
