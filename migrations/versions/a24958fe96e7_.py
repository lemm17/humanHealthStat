"""empty message

Revision ID: a24958fe96e7
Revises: 5e7033496215
Create Date: 2019-11-25 12:08:26.307539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24958fe96e7'
down_revision = '5e7033496215'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_comment_id'), 'comment', ['id'], unique=False)
    op.create_index(op.f('ix_notification_id'), 'notification', ['id'], unique=False)
    op.create_index(op.f('ix_publication_id'), 'publication', ['id'], unique=False)
    op.create_index(op.f('ix_settings_id_user'), 'settings', ['id_user'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.drop_index('ix_user_phone_number', table_name='user')
    op.drop_column('user', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone_number', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.create_index('ix_user_phone_number', 'user', ['phone_number'], unique=True)
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_settings_id_user'), table_name='settings')
    op.drop_index(op.f('ix_publication_id'), table_name='publication')
    op.drop_index(op.f('ix_notification_id'), table_name='notification')
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    # ### end Alembic commands ###