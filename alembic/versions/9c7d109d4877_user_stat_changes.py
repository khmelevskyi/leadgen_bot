"""user stat changes

Revision ID: 9c7d109d4877
Revises: ea1b65b7a808
Create Date: 2021-09-02 15:21:39.861701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c7d109d4877'
down_revision = 'ea1b65b7a808'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'deals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('linkedin', sa.String),
        sa.Column('leadgen_id', sa.Integer, sa.ForeignKey("user.chat_id")),
    )
    op.create_foreign_key(
            "leadgen", "deals",
            "user", ["leadgen_id"], ["chat_id"])
    op.add_column('admin', sa.Column('role', sa.String))
    op.add_column('user_stat', sa.Column('deals', sa.Integer))
    op.add_column('user_stat', sa.Column('earned', sa.Integer))


def downgrade():
    pass
