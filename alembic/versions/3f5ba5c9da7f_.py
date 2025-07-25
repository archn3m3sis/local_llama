"""empty message

Revision ID: 3f5ba5c9da7f
Revises: bb427c7ef7da
Create Date: 2025-07-18 14:14:14.846611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '3f5ba5c9da7f'
down_revision: Union[str, Sequence[str], None] = 'bb427c7ef7da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sysarchitecture',
    sa.Column('sysarchitecture_id', sa.Integer(), nullable=False),
    sa.Column('sys_architecture', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('sysarchitecture_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sysarchitecture')
    # ### end Alembic commands ###
