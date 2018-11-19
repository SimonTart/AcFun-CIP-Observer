"""make contents type nullable

Revision ID: 4ca1430878ec
Revises: e358c147cd3c
Create Date: 2018-11-17 13:42:27.340106+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ca1430878ec'
down_revision = 'e358c147cd3c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('contents', 'type', type=sa.String(length=255), existing_type=sa.String(length=255), nullable=True)


def downgrade():
    op.alter_column('contents', 'type', type=sa.String(length=255), existing_type=sa.String(length=255), nullable=False)
