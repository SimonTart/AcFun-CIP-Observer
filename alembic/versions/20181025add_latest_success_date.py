"""add latest success date

Revision ID: c4162b413189
Revises: a9f8794980b7
Create Date: 2018-10-25 21:05:20.831869+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4162b413189'
down_revision = 'a9f8794980b7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('spider_record',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.String(length=255), nullable=False),
                    sa.Column('success_date', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('spider_record')
