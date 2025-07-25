"""empty message

Revision ID: 0efa150e1d21
Revises: 93b841d2894d
Create Date: 2025-07-20 15:56:23.762098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '0efa150e1d21'
down_revision: Union[str, Sequence[str], None] = '93b841d2894d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datupdate',
    sa.Column('datupdate_id', sa.Integer(), nullable=False),
    sa.Column('date_of_update', sa.DateTime(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('datversion_id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('datfile_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('update_result', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('update_comments', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.asset_id'], ),
    sa.ForeignKeyConstraint(['datversion_id'], ['datversion.datversion_id'], ),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.project_id'], ),
    sa.PrimaryKeyConstraint('datupdate_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('datupdate')
    # ### end Alembic commands ###
