"""empty message

Revision ID: f6be176be455
Revises: e9bbe903f593
Create Date: 2024-09-12 18:22:05.793853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6be176be455'
down_revision: Union[str, None] = 'e9bbe903f593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_tags_user_id'), 'tags', ['user_id'], unique=False)
    op.create_foreign_key(None, 'tags', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='foreignkey')
    op.drop_index(op.f('ix_tags_user_id'), table_name='tags')
    op.drop_column('tags', 'user_id')
    # ### end Alembic commands ###
