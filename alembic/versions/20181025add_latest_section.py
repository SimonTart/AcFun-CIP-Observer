"""add latest section

Revision ID: a9f8794980b7
Revises: ee895f48e769
Create Date: 2018-10-25 19:35:09.836469+08:00

"""
from alembic import op
import sqlalchemy as sa
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db import connection
from config import VIDEO_SECTIONS, ARTICLE_SECTIONS

# revision identifiers, used by Alembic.
revision = 'a9f8794980b7'
down_revision = 'ee895f48e769'
branch_labels = None
depends_on = None


def insert_sentions(sections):
    for section in sections:
        connection.execute(
            'INSERT INTO section_latest_content(section_id, latest_content_date) VALUES({sectionId}, "{date}")'.format(
                sectionId=section['channelId'],
                date="2018-10-25 00:00:00"
            )
        )
        if 'subSections' in section and section['subSections'] is not None:
            insert_sentions(section['subSections'])


def upgrade():
    pass
    # op.create_table('section_latest_content',
    #                 sa.Column('id', sa.Integer(), nullable=False),
    #                 sa.Column('section_id', sa.Integer(), nullable=False),
    #                 sa.Column('latest_content_date', sa.DateTime(), nullable=False),
    #                 sa.Column('updated_at', sa.DateTime(),
    #                           server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    #                 sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    #                 sa.PrimaryKeyConstraint('id')
    #                 )
    # insert_sentions(ARTICLE_SECTIONS)
    # insert_sentions(VIDEO_SECTIONS)



def downgrade():
    pass
    # op.drop_table('section_latest_content')
