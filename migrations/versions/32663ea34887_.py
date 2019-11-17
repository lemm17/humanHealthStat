"""empty message

Revision ID: 32663ea34887
Revises: e806d4be9d9c
Create Date: 2019-11-17 01:55:54.065200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32663ea34887'
down_revision = 'e806d4be9d9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publication', sa.Column('publication_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publication', 'publication_date')
    # ### end Alembic commands ###
