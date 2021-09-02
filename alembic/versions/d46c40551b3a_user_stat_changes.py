"""user stat changes

Revision ID: d46c40551b3a
Revises: 
Create Date: 2021-09-02 13:02:19.515630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd46c40551b3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('admin', sa.Column('role', sa.String))
    op.add_column('user_stat', sa.Column('deals', sa.Integer))
    op.add_column('user_stat', sa.Column('earned', sa.Integer))


def downgrade():
    pass
