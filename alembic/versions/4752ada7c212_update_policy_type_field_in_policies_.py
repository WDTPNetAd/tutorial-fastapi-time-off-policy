"""Update policy_type field in policies and policy_histories

Revision ID: 4752ada7c212
Revises: 11566f9ef232
Create Date: 2025-08-07 06:35:28.129785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4752ada7c212'
down_revision: Union[str, Sequence[str], None] = '11566f9ef232'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ Update policy_type from Default to Annual and others to Monthly """
    op.execute("""
        UPDATE policies
        SET policy_type = CASE
            WHEN policy_type = 'Default' THEN 'Annual'
            ELSE 'Monthly'
        END
    """)

    op.execute("""
        UPDATE policy_histories
        SET policy_type = CASE
            WHEN policy_type = 'Default' THEN 'Annual'
            ELSE 'Monthly'
        END
    """)


def downgrade() -> None:
    """ Reverts Annual to Default and others to Custom """
    op.execute("""
        UPDATE policies
        SET policy_type = CASE
            WHEN policy_type = 'Annual' THEN 'Default'
            ELSE 'Custom'
        END
    """)

    op.execute("""
        UPDATE policy_histories
        SET policy_type = CASE
            WHEN policy_type = 'Annual' THEN 'Default'
            ELSE 'Custom'
        END
    """)
