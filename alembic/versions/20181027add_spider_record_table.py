"""add spider record table

Revision ID: e358c147cd3c
Revises: 50de723247d1
Create Date: 2018-10-27 21:12:13.875685+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e358c147cd3c'
down_revision = '50de723247d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('spider_record',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('channel_id', sa.Integer()),
        sa.Column('type', sa.String(length=255), nullable=False),
        sa.Column('success_date', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(),
                  server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('spider_record')
