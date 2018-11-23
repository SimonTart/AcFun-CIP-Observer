"""create comment user_id index

Revision ID: 3c43e4060439
Revises: 4ca1430878ec
Create Date: 2018-11-23 21:42:22.316211+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c43e4060439'
down_revision = '4ca1430878ec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('user_id_index', 'comments', ['user_id'])


def downgrade():
    op.drop_index('user_id_index', 'comments')
