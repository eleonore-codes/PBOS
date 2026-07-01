"""add assessment question snapshots

Revision ID: 0002_add_assessment_question_snapshots
Revises: 0001_create_m2_pbhs_foundation
Create Date: 2026-07-01
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_assessment_question_snapshots"
down_revision = "0001_create_m2_pbhs_foundation"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "pbhs_assessment_questions",
        sa.Column("assessment_question_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("question_id", sa.String(length=36), nullable=False),
        sa.Column("question_version", sa.String(length=50), nullable=False),
        sa.Column("capability", sa.String(length=150), nullable=False),
        sa.Column("construct", sa.String(length=150), nullable=False),
        sa.Column("question_text", sa.String(length=1000), nullable=False),
        sa.Column("response_scale", sa.String(length=100), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("source_status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["pbhs_assessments.assessment_id"],
            name=op.f("fk_pbhs_assessment_questions_assessment_id_pbhs_assessments"),
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["pbhs_questions.question_id"],
            name=op.f("fk_pbhs_assessment_questions_question_id_pbhs_questions"),
        ),
        sa.PrimaryKeyConstraint(
            "assessment_question_id",
            name=op.f("pk_pbhs_assessment_questions"),
        ),
        sa.UniqueConstraint(
            "assessment_id",
            "question_id",
            name="uq_pbhs_assessment_questions_assessment_question",
        ),
    )
    op.create_index(
        op.f("ix_pbhs_assessment_questions_assessment_id"),
        "pbhs_assessment_questions",
        ["assessment_id"],
        unique=False,
    )
    op.create_index(
        "ix_pbhs_assessment_questions_assessment_capability",
        "pbhs_assessment_questions",
        ["assessment_id", "capability"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pbhs_assessment_questions_question_id"),
        "pbhs_assessment_questions",
        ["question_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_pbhs_assessment_questions_question_id"),
        table_name="pbhs_assessment_questions",
    )
    op.drop_index(
        "ix_pbhs_assessment_questions_assessment_capability",
        table_name="pbhs_assessment_questions",
    )
    op.drop_index(
        op.f("ix_pbhs_assessment_questions_assessment_id"),
        table_name="pbhs_assessment_questions",
    )
    op.drop_table("pbhs_assessment_questions")
