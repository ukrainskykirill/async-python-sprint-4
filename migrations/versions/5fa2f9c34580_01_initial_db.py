"""01_initial-db

Revision ID: 5fa2f9c34580
Revises: 
Create Date: 2022-11-20 14:30:55.805714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fa2f9c34580'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('short_URL',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('short_url', sa.String(length=100), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url')
    )
    op.create_index(op.f('ix_short_URL_created_at'), 'short_URL', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_short_URL_created_at'), table_name='short_URL')
    op.drop_table('short_URL')
    # ### end Alembic commands ###
