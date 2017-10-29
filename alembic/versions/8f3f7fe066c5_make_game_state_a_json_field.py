"""Make game state a json field

Revision ID: 8f3f7fe066c5
Revises: 5e7b2ba3fc8d
Create Date: 2017-10-28 13:33:30.899258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3f7fe066c5'
down_revision = '5e7b2ba3fc8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('json', sa.JSON(), nullable=False))
    op.drop_column('games', 'state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('games', 'json')
    # ### end Alembic commands ###