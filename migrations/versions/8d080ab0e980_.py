"""
Revision ID: 8d080ab0e980
Revises: 796ec72a3475
Create Date: 2026-04-26 14:43:06.725427
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '8d080ab0e980'
down_revision: Union[str, Sequence[str], None] = '796ec72a3475'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create the new table first
    op.create_table('embeddedtext',
    sa.Column('question', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('answer', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=768), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 2. DROP the old index FIRST to free up the name 'ix_item_embedding'
    # Added IF EXISTS logic just in case the index was already partially messed with
    op.execute("DROP INDEX IF EXISTS ix_item_embedding")

    # 3. NOW create the new index on the new table
    op.create_index(
        'ix_item_embedding', 
        'embeddedtext', 
        ['embedding'], 
        unique=False, 
        postgresql_using='hnsw', 
        postgresql_with={'m': 16, 'ef_construction': 64}, 
        postgresql_ops={'embedding': 'vector_cosine_ops'}
    )


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Drop the index from the new table
    op.drop_index(
        'ix_item_embedding', 
        table_name='embeddedtext', 
        postgresql_using='hnsw', 
        postgresql_with={'m': 16, 'ef_construction': 64}, 
        postgresql_ops={'embedding': 'vector_cosine_ops'}
    )

    # 2. Re-create the index on the old 'item' table
    op.create_index(
        'ix_item_embedding', 
        'item', 
        ['embedding'], 
        unique=False, 
        postgresql_ops={'embedding': 'vector_cosine_ops'}, 
        postgresql_with={'m': '16', 'ef_construction': '64'}, 
        postgresql_using='hnsw'
    )

    # 3. Drop the new table
    op.drop_table('embeddedtext')