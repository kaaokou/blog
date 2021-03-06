"""添加审核reason

Revision ID: ef9bbfa68a0e
Revises: 48b13229c4d2
Create Date: 2018-06-19 12:35:28.402099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9bbfa68a0e'
down_revision = '48b13229c4d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs_comment', sa.Column('reason', sa.String(length=100), nullable=True))
    op.add_column('blogs_message', sa.Column('reason', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs_message', 'reason')
    op.drop_column('blogs_comment', 'reason')
    # ### end Alembic commands ###
