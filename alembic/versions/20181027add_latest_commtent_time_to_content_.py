"""add latest commtent time to content table

Revision ID: 50de723247d1
Revises: ee895f48e769
Create Date: 2018-10-27 21:11:41.866926+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50de723247d1'
down_revision = 'ee895f48e769'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('contents', sa.Column('latest_comment_time', sa.String(length=255)))


def downgrade():
    op.drop_column('contents', 'latest_comment_time')
