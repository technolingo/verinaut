"""007 change Prediction.status approved to reviewed

Revision ID: ff392cecadb3
Revises: 989393577605
Create Date: 2025-12-23 18:52:49.243459

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ff392cecadb3"
down_revision: Union[str, Sequence[str], None] = "989393577605"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite stores enum values as strings
    op.execute("UPDATE prediction SET status = 'reviewed' WHERE status = 'approved'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE prediction SET status = 'approved' WHERE status = 'reviewed'")
