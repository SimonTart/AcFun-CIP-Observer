"""change article tables name

Revision ID: 32ce7a82e57e
Revises: 9e328ab68d0f
Create Date: 2018-03-11 17:44:49.064694+08:00

"""
from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32ce7a82e57e'
down_revision = '9e328ab68d0f'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('articles', 'contents')


def downgrade():
    op.RenameTableOp('contents', 'articles')
