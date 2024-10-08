"""Добваил поле description

Revision ID: 4fe7fecb15e8
Revises: 1450a44aa110
Create Date: 2024-08-21 09:54:40.680083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fe7fecb15e8'
down_revision: Union[str, None] = '1450a44aa110'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('description', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'description')
    # ### end Alembic commands ###
