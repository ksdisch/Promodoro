"""Add planned and actual times to ScheduledSession

Revision ID: 99276a3fd664
Revises: 
Create Date: 2024-10-28 06:59:46.023693

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '99276a3fd664'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scheduled_sessions', sa.Column('planned_start_time', sa.DateTime(), nullable=True))
    op.add_column('scheduled_sessions', sa.Column('planned_end_time', sa.DateTime(), nullable=True))
    op.add_column('scheduled_sessions', sa.Column('actual_start_time', sa.DateTime(), nullable=True))
    op.add_column('scheduled_sessions', sa.Column('actual_end_time', sa.DateTime(), nullable=True))
    op.add_column('scheduled_sessions', sa.Column('status', sa.String(length=20), nullable=False))
    op.drop_column('scheduled_sessions', 'start_time')
    op.drop_column('scheduled_sessions', 'end_time')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scheduled_sessions', sa.Column('end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('scheduled_sessions', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('scheduled_sessions', 'status')
    op.drop_column('scheduled_sessions', 'actual_end_time')
    op.drop_column('scheduled_sessions', 'actual_start_time')
    op.drop_column('scheduled_sessions', 'planned_end_time')
    op.drop_column('scheduled_sessions', 'planned_start_time')
    # ### end Alembic commands ###
