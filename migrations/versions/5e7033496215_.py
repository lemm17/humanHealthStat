"""empty message

Revision ID: 5e7033496215
Revises: 32663ea34887
Create Date: 2019-11-19 15:15:17.713142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e7033496215'
down_revision = '32663ea34887'
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
