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
        "processo",
        #sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("numero_processo", sa.String(100), nullable=False, primary_key=True),
        sa.Column("tribunal", sa.String(100), nullable=False),
        sa.Column("grau", sa.String(100), nullable=False),
        sa.Column("orgao_codigo", sa.Float, nullable=False),
        sa.Column("orgao_nome", sa.String(100), nullable=False),

        sa.Column("data_ajuizamento", sa.DateTime, nullable=False),
        sa.Column("data_julgamento", sa.DateTime, nullable=False),
        sa.Column("tempo_julgamento", sa.Float, nullable=False),

        sa.Column("codigo_classe", sa.Float, nullable=False),
        sa.Column("classe_nivel1", sa.Float, nullable=False),
        sa.Column("classe_nivel2", sa.Float, nullable=True),
        sa.Column("classe_nivel3", sa.Float, nullable=True),
        sa.Column("classe_nivel4", sa.Float, nullable=True),
        sa.Column("classe_nivel5", sa.Float, nullable=True),

        sa.Column("codigo_assunto", sa.Float, nullable=False),
        sa.Column("assunto_nivel1", sa.Float, nullable=False),
        sa.Column("assunto_nivel2", sa.Float, nullable=True),
        sa.Column("assunto_nivel3", sa.Float, nullable=True),
        sa.Column("assunto_nivel4", sa.Float, nullable=True),
        sa.Column("assunto_nivel5", sa.Float, nullable=True),

        sa.Column("codigo_formato", sa.Float, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("processo")
