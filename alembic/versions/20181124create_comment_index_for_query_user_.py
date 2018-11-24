"""create comment index for query user comment

Revision ID: a51f03e22f7a
Revises: 3c43e4060439
Create Date: 2018-11-24 12:32:22.116095+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a51f03e22f7a'
down_revision = '3c43e4060439'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index('user_id_index', 'comments')
    op.create_index('content_id_index', 'comments', ['content_id'])
    op.create_index('user_content_id_index', 'comments', ['user_id', 'content_id'])


def downgrade():
    op.drop_index('content_id_index', 'comments')
    op.drop_index('user_content_id_index', 'comments')
    op.create_index('user_id_index', 'comments', ['user_id'])
