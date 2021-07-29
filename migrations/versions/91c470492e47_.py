"""empty message

Revision ID: 91c470492e47
Revises: 171d5eb75cab
Create Date: 2021-07-20 10:44:23.241537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c470492e47'
down_revision = '171d5eb75cab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.String(length=200), nullable=False))
    op.drop_column('user', 'paasword')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('paasword', sa.VARCHAR(length=200), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###