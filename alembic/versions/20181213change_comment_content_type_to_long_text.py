"""change comment content type to long text

Revision ID: 54a4b45165b5
Revises: e8daf8c2731e
Create Date: 2018-12-13 13:02:24.986715+08:00

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.mysql as sql


# revision identifiers, used by Alembic.
revision = '54a4b45165b5'
down_revision = 'e8daf8c2731e'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("ALTER TABLE comments MODIFY content LONGTEXT")


def downgrade():
    conn = op.get_bind()
    conn.execute("ALTER TABLE comments MODIFY content TEXT")
