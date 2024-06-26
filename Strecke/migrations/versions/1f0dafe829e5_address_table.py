"""address table

Revision ID: 1f0dafe829e5
Revises: e8ed9ecc160c
Create Date: 2024-05-22 20:42:39.628379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f0dafe829e5'
down_revision = 'e8ed9ecc160c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('street', sa.String(length=140), nullable=True),
    sa.Column('no', sa.Integer(), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=140), nullable=True),
    sa.Column('country', sa.String(length=140), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('route', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trackWidth', sa.Integer(), nullable=True))

    with op.batch_alter_table('routesegments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('segment_order', sa.Integer(), nullable=False))

    with op.batch_alter_table('station', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_station_address_id', 'address', ['address_id'], ['id'])
        batch_op.drop_column('country')
        batch_op.drop_column('zipcode')
        batch_op.drop_column('street')
        batch_op.drop_column('city')
        batch_op.drop_column('no')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_user_address_id', 'address', ['address_id'], ['id'])

    with op.batch_alter_table('warning', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=140), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=1500),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('warning', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=1500),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
        batch_op.drop_column('name')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_address_id', type_='foreignkey')
        batch_op.drop_column('address_id')

    with op.batch_alter_table('station', schema=None) as batch_op:
        batch_op.add_column(sa.Column('no', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('city', sa.VARCHAR(length=140), nullable=True))
        batch_op.add_column(sa.Column('street', sa.VARCHAR(length=140), nullable=True))
        batch_op.add_column(sa.Column('zipcode', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('country', sa.VARCHAR(length=140), nullable=True))
        batch_op.drop_constraint('fk_station_address_id', type_='foreignkey')
        batch_op.drop_column('address_id')

    with op.batch_alter_table('routesegments', schema=None) as batch_op:
        batch_op.drop_column('segment_order')

    with op.batch_alter_table('route', schema=None) as batch_op:
        batch_op.drop_column('trackWidth')

    op.drop_table('address')
    # ### end Alembic commands ###
