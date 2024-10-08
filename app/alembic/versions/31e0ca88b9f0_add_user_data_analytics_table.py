"""add user, data, analytics table

Revision ID: 31e0ca88b9f0
Revises: ba2b6f18ee44
Create Date: 2024-09-13 02:03:38.081855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31e0ca88b9f0'
down_revision: Union[str, None] = 'ba2b6f18ee44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('created_on', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tg_id')
    )
    op.create_table('analytics_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('request_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('input_data', sa.String(), nullable=True),
    sa.Column('output_data', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_table')
    op.drop_table('analytics_table')
    op.drop_table('user_table')
    # ### end Alembic commands ###
