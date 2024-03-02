"""v1.1

Revision ID: e83f6bc0c3c7
Revises: 
Create Date: 2023-03-26 05:14:58.976623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e83f6bc0c3c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('role',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.String, nullable=False, unique=True)
                    )
    op.create_table('district',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.String, nullable=False, unique=True)
                    )
    op.create_table('upazilla',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('district', sa.String, sa.ForeignKey("district.name", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('name', sa.String, nullable=False, unique=True)
                    )
    op.create_table('mouza',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('upazilla', sa.String, sa.ForeignKey("upazilla.name", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('name', sa.String, nullable=False, unique=True)
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('username', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('role', sa.String, sa.ForeignKey("role.name", ondelete="CASCADE"),
                              nullable=False, default=None, unique=False)
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('mouza')
    op.drop_table('upazilla')
    op.drop_table('district')
    op.drop_table('role')

    pass
