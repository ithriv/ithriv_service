"""empty message

Revision ID: dd3fca520474
Revises: 8f722fee6c67
Create Date: 2019-10-03 14:47:45.210757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd3fca520474'
down_revision = '8f722fee6c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resource', 'segment_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('resource', 'segment_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
