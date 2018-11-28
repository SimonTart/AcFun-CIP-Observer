"""add count ref count to comment

Revision ID: e8daf8c2731e
Revises: a51f03e22f7a
Create Date: 2018-11-28 21:41:49.796101+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8daf8c2731e'
down_revision = 'a51f03e22f7a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('comments', sa.Column('count', sa.Integer))
    op.add_column('comments', sa.Column('ref_count', sa.Integer))


def downgrade():
    op.drop_column('comments', 'count')
    op.drop_column('comments', 'ref_count')
