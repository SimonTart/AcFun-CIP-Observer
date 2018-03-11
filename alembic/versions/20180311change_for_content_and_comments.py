"""change for content and comments

Revision ID: 5ee6d18e50ed
Revises: 32ce7a82e57e
Create Date: 2018-03-11 17:54:17.931374+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ee6d18e50ed'
down_revision = '32ce7a82e57e'
branch_labels = None
depends_on = None


def upgrade():
   op.alter_column(table_name='comments', column_name='article_id', new_column_name='content_id', existing_type=sa.Integer())


def downgrade():
   op.alter_column(table_name='comments', column_name='content_id', new_column_name='article_id', existing_type=sa.Integer())
