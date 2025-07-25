"""empty message

Revision ID: ca3ebdcb79fa
Revises: 9470ece7683a
Create Date: 2025-07-18 17:29:52.410224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'ca3ebdcb79fa'
down_revision: Union[str, Sequence[str], None] = '9470ece7683a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('floor', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('FK__floor__building___72C60C4A'), type_='foreignkey')
        batch_op.drop_column('building_id')

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('floor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('building_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key(batch_op.f('FK__floor__building___72C60C4A'), 'building', ['building_id'], ['building_id'])

    # ### end Alembic commands ###
