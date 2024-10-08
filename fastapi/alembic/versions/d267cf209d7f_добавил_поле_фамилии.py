"""Добавил поле фамилии

Revision ID: d267cf209d7f
Revises: b072a3a7a42b
Create Date: 2024-08-21 09:24:29.879626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd267cf209d7f'
down_revision: Union[str, None] = 'b072a3a7a42b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###
