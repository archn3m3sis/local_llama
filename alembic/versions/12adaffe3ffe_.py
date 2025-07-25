"""empty message

Revision ID: 12adaffe3ffe
Revises: ca3ebdcb79fa
Create Date: 2025-07-18 17:40:51.268031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '12adaffe3ffe'
down_revision: Union[str, Sequence[str], None] = 'ca3ebdcb79fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_name', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_column('room_name')

    # ### end Alembic commands ###
