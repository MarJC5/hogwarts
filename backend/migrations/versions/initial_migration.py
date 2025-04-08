"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2025-04-08

"""
from alembic import op
import sqlalchemy as sa
from app.models.models import House

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create wizards table
    op.create_table(
        'wizards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('house', sa.Enum('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin', name='house'), nullable=False),
        sa.Column('wand', sa.String(), nullable=False),
        sa.Column('patronus', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wizards_id'), 'wizards', ['id'], unique=False)
    op.create_index(op.f('ix_wizards_name'), 'wizards', ['name'], unique=False)
    
    # Create teachers table
    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('subject', sa.String(), nullable=False),
        sa.Column('house', sa.Enum('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin', name='house'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers_id'), 'teachers', ['id'], unique=False)
    op.create_index(op.f('ix_teachers_name'), 'teachers', ['name'], unique=False)
    
    # Create house_points table
    op.create_table(
        'house_points',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('house', sa.Enum('Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin', name='house'), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('teacher_id', sa.Integer(), nullable=False),
        sa.Column('wizard_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
        sa.ForeignKeyConstraint(['wizard_id'], ['wizards.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_house_points_id'), 'house_points', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_house_points_id'), table_name='house_points')
    op.drop_table('house_points')
    
    op.drop_index(op.f('ix_teachers_name'), table_name='teachers')
    op.drop_index(op.f('ix_teachers_id'), table_name='teachers')
    op.drop_table('teachers')
    
    op.drop_index(op.f('ix_wizards_name'), table_name='wizards')
    op.drop_index(op.f('ix_wizards_id'), table_name='wizards')
    op.drop_table('wizards') 