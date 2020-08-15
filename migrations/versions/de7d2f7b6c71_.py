"""empty message

Revision ID: de7d2f7b6c71
Revises: 
Create Date: 2020-08-12 07:20:06.957898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'de7d2f7b6c71'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('picture', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('order_sum', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=1000), nullable=False),
    sa.Column('address', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders_meals',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['meals.id'], ),
    sa.PrimaryKeyConstraint('order_id', 'meal_id')
    )

    op.drop_table('teachers_goals')
    op.drop_table('bookings')
    op.drop_table('teachers')
    op.drop_table('requests')
    op.drop_table('goals')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('goal', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('availability', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('clientName', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('clientPhone', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='requests_pkey')
    )
    op.create_table('teachers_goals',
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('goal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], name='teachers_goals_goal_id_fkey'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='teachers_goals_teacher_id_fkey'),
    sa.PrimaryKeyConstraint('teacher_id', 'goal_id', name='teachers_goals_pkey')
    )
    op.create_table('bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('weekday', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='bookings_teacher_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='bookings_pkey')
    )
    op.create_table('teachers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('about', sa.VARCHAR(length=4000), autoincrement=False, nullable=True),
    sa.Column('rating', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('picture', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('free', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='teachers_pkey')
    )
    op.create_table('goals',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('goal', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('goal_ru', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='goals_pkey')
    )
    op.drop_table('orders_meals')
    op.drop_table('users')
    op.drop_table('orders')
    op.drop_table('meals')
    op.drop_table('categories')
    # ### end Alembic commands ###