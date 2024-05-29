"""data model

Revision ID: e8ed9ecc160c
Revises: 5cdca21e802b
Create Date: 2024-05-22 20:31:05.653747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8ed9ecc160c'
down_revision = '5cdca21e802b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('route',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('startStation', sa.Integer(), nullable=True),
    sa.Column('endStation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['endStation'], ['station.id'], name='fk_route_station_start'),
    sa.ForeignKeyConstraint(['startStation'], ['station.id'], name='fk_route_station_start'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('segment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('startStation', sa.Integer(), nullable=True),
    sa.Column('endStation', sa.Integer(), nullable=True),
    sa.Column('trackWidth', sa.Integer(), nullable=True),
    sa.Column('length', sa.Double(), nullable=True),
    sa.Column('maxSpeed', sa.Integer(), nullable=True),
    sa.Column('price', sa.Double(), nullable=True),
    sa.ForeignKeyConstraint(['endStation'], ['station.id'], name='fk_segment_end'),
    sa.ForeignKeyConstraint(['startStation'], ['station.id'], name='fk_segment_start'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routesegments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('segment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], name='fk_route_id'),
    sa.ForeignKeyConstraint(['segment_id'], ['segment.id'], name='fk_route_segment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('warning',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('validFrom', sa.DateTime(), nullable=True),
    sa.Column('validTo', sa.DateTime(), nullable=True),
    sa.Column('segment', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['segment'], ['segment.id'], name='fk_warning_segment_id'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warning')
    op.drop_table('routesegments')
    op.drop_table('segment')
    op.drop_table('route')
    # ### end Alembic commands ###
