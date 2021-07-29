"""empty message

Revision ID: 171d5eb75cab
Revises: aa3e9e6f6930
Create Date: 2021-07-18 15:14:12.851181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '171d5eb75cab'
down_revision = 'aa3e9e6f6930'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('paasword', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###