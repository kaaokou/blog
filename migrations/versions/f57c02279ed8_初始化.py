"""初始化

Revision ID: f57c02279ed8
Revises: 
Create Date: 2018-06-17 15:55:13.789877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57c02279ed8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogs_category',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('isDelete', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs_message',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('isDelete', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('blog_address', sa.String(length=40), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.Column('msg', sa.String(length=200), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('isDelete', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.Column('nick_name', sa.String(length=20), nullable=True),
    sa.Column('mobile', sa.String(length=11), nullable=True),
    sa.Column('password_hash', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs_info',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('isDelete', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('pic', sa.String(length=50), nullable=True),
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('summary', sa.String(length=200), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=20), nullable=True),
    sa.Column('click_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['blogs_category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogs_comment',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('isDelete', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick_name', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('blog_address', sa.String(length=40), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.Column('blogs_id', sa.Integer(), nullable=True),
    sa.Column('msg', sa.String(length=200), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blogs_id'], ['blogs_info.id'], ),
    sa.ForeignKeyConstraint(['comment_id'], ['blogs_comment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs_comment')
    op.drop_table('blogs_info')
    op.drop_table('user_info')
    op.drop_table('blogs_message')
    op.drop_table('blogs_category')
    # ### end Alembic commands ###
