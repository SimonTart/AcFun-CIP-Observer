"""add content type to contents

Revision ID: ee895f48e769
Revises: c0d512bb9fa1
Create Date: 2018-03-11 18:42:52.121366+08:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import String
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'ee895f48e769'
down_revision = 'c0d512bb9fa1'
branch_labels = None
depends_on = None

Content = table( 'contents',
    column('content_type', String)
)


def upgrade():
    op.add_column('contents', sa.Column('content_type', sa.String(length=255), nullable=False))
    op.execute(
        Content.update().values({'content_type': 'article'})
        )


def downgrade():
    op.drop_column('contents', 'content_type')
