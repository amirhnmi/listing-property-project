"""user and list model created

Revision ID: 74e8e356f45c
Revises: 
Create Date: 2023-09-13 13:10:59.229170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74e8e356f45c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('fullname', sa.String(length=250), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.Column('dateOfBirth', sa.Date(), nullable=True),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('token', sa.Integer(), nullable=True),
    sa.Column('createAt', sa.DateTime(), nullable=True),
    sa.Column('updateAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('availableNow', sa.Boolean(), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('createAt', sa.DateTime(), nullable=True),
    sa.Column('updateAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listings')
    op.drop_table('users')
    # ### end Alembic commands ###
