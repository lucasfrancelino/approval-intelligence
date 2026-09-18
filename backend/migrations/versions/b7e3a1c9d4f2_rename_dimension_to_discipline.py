"""rename dimension to discipline

Revision ID: b7e3a1c9d4f2
Revises: 9efec0a5fff8
Create Date: 2026-09-18 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b7e3a1c9d4f2'
down_revision: Union[str, Sequence[str], None] = '9efec0a5fff8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index('ix_evidences_dimension', table_name='evidences')

    op.alter_column(
        'evidences',
        'dimension',
        new_column_name='discipline',
    )

    op.create_index(
        op.f('ix_evidences_discipline'),
        'evidences',
        ['discipline'],
        unique=False,
    )

    op.alter_column(
        'decisions',
        'target_dimension',
        new_column_name='target_discipline',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'decisions',
        'target_discipline',
        new_column_name='target_dimension',
    )

    op.drop_index(
        op.f('ix_evidences_discipline'),
        table_name='evidences',
    )

    op.alter_column(
        'evidences',
        'discipline',
        new_column_name='dimension',
    )

    op.create_index(
        'ix_evidences_dimension',
        'evidences',
        ['dimension'],
        unique=False,
    )