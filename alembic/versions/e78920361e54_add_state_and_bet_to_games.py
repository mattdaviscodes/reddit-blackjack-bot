"""add state and bet to games

Revision ID: e78920361e54
Revises: a536d2ef991a
Create Date: 2017-10-01 07:27:14.683746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78920361e54'
down_revision = 'a536d2ef991a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('bet', sa.Integer(), nullable=False))
    op.add_column('games', sa.Column('state', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'state')
    op.drop_column('games', 'bet')
    # ### end Alembic commands ###