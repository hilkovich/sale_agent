"""edit sentiment enum

Revision ID: ba2b6f18ee44
Revises: 8c4aae5662bd
Create Date: 2024-09-11 17:15:04.061519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba2b6f18ee44'
down_revision: Union[str, None] = '8c4aae5662bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute('ALTER TYPE sentimentenum ADD VALUE \'Neutral\';')


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
