"""seeds data

Revision ID: 9efa7b5eb6af
Revises: d4c2b5dd703b
Create Date: 2025-11-05 05:31:56.686435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9efa7b5eb6af'
down_revision: Union[str, Sequence[str], None] = 'd4c2b5dd703b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


import uuid
from faker import Faker
import sqlalchemy as sa

Faker.seed(0)
fake = Faker()

def upgrade() -> None:
    """Upgrade schema."""
    users = []
    for i in range(5):
        users.append(
            {
                "id": uuid.uuid4(),
                "email": fake.email(),
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
            }
        )

    op.bulk_insert(
        sa.table(
            "users",
            sa.column("id", sa.UUID),
            sa.column("email", sa.String),
            sa.column("firstname", sa.String),
            sa.column("lastname", sa.String),
        ),
        users,
    )

    notes = []
    for i in range(10):
        notes.append(
            {
                "id": uuid.uuid4(),
                "content": fake.text(),
                "user_id": users[i % 5]["id"],
            }
        )

    op.bulk_insert(
        sa.table(
            "notes",
            sa.column("id", sa.UUID),
            sa.column("content", sa.String),
            sa.column("user_id", sa.UUID),
        ),
        notes,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM notes;")
    op.execute("DELETE FROM users;")
