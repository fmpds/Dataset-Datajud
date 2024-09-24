"""init db

Revision ID: bc1378e4e526
Revises: 
Create Date: 2024-09-23 17:27:09.158456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bc1378e4e526'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "processos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("numero_processo", sa.String(50), nullable=False),
        sa.Column("tribunal", sa.String(100), nullable=False),
        sa.Column("grau", sa.String(100), nullable=False),
        sa.Column("data_juizamento", sa.DateTime, nullable=False),
        sa.Column("movimentacoes", sa.String(100), nullable=False),
        sa.Column("assuntos", sa.String(100), nullable=False),
        sa.Column("codigo_da_classe", sa.String(100), nullable=False),
        sa.Column("codigo_formato", sa.String(100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("processos")
