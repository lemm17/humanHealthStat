"""empty message

Revision ID: b05969701a0e
Revises: 7f7f8f69b7cb
Create Date: 2019-10-30 21:31:41.649619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b05969701a0e'
down_revision = '7f7f8f69b7cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    # ### end Alembic commands ###