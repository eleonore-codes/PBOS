"""add capability scores

Revision ID: 0003_add_capability_scores
Revises: 0002_add_assessment_question_snapshots
Create Date: 2026-07-01
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_add_capability_scores"
down_revision = "0002_add_assessment_question_snapshots"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("pbhs_assessments", sa.Column("overall_score", sa.Float(), nullable=True))
    op.add_column("pbhs_assessments", sa.Column("overall_confidence", sa.Float(), nullable=True))
    op.add_column(
        "pbhs_assessments",
        sa.Column("scoring_method", sa.String(length=100), nullable=True),
    )
    op.add_column("pbhs_assessments", sa.Column("scored_at", sa.DateTime(), nullable=True))

    op.create_table(
        "capability_scores",
        sa.Column("capability_score_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("capability", sa.String(length=150), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("maturity_level", sa.Integer(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("calculation_method", sa.String(length=100), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("scored_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "score >= 0.0 AND score <= 100.0",
            name=op.f("ck_capability_scores_capability_score_range"),
        ),
        sa.CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name=op.f("ck_capability_scores_capability_confidence_range"),
        ),
        sa.CheckConstraint(
            "maturity_level >= 1 AND maturity_level <= 5",
            name=op.f("ck_capability_scores_maturity_level_range"),
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["pbhs_assessments.assessment_id"],
            name=op.f("fk_capability_scores_assessment_id_pbhs_assessments"),
        ),
        sa.PrimaryKeyConstraint("capability_score_id", name=op.f("pk_capability_scores")),
        sa.UniqueConstraint(
            "assessment_id",
            "capability",
            name="uq_capability_scores_assessment_capability",
        ),
    )
    op.create_index(
        op.f("ix_capability_scores_assessment_id"),
        "capability_scores",
        ["assessment_id"],
        unique=False,
    )
    op.create_index(
        "ix_capability_scores_assessment_capability",
        "capability_scores",
        ["assessment_id", "capability"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_capability_scores_assessment_capability", table_name="capability_scores")
    op.drop_index(op.f("ix_capability_scores_assessment_id"), table_name="capability_scores")
    op.drop_table("capability_scores")
    op.drop_column("pbhs_assessments", "scored_at")
    op.drop_column("pbhs_assessments", "scoring_method")
    op.drop_column("pbhs_assessments", "overall_confidence")
    op.drop_column("pbhs_assessments", "overall_score")
