"""add article id to comments

Revision ID: 1a9b44aa8208
Revises: a7bfa0f5a3a3
Create Date: 2017-10-11 23:04:59.550210+08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a9b44aa8208'
down_revision = 'a7bfa0f5a3a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('article_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'article_id')
    # ### end Alembic commands ###
