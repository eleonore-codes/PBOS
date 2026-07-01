"""add recommendations

Revision ID: 0004_add_recommendations
Revises: 0003_add_capability_scores
Create Date: 2026-07-01
"""

from alembic import op
import sqlalchemy as sa

revision = "0004_add_recommendations"
down_revision = "0003_add_capability_scores"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "recommendations",
        sa.Column("recommendation_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("rule_id", sa.String(length=100), nullable=False),
        sa.Column("rule_version", sa.String(length=50), nullable=False),
        sa.Column("template_id", sa.String(length=100), nullable=False),
        sa.Column("template_version", sa.String(length=50), nullable=False),
        sa.Column("recommendation_type", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=250), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("priority_score", sa.Float(), nullable=False),
        sa.Column("priority_rationale", sa.String(length=1000), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("confidence_label", sa.String(length=50), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("risk_label", sa.String(length=50), nullable=False),
        sa.Column("expected_business_return", sa.JSON(), nullable=False),
        sa.Column("expected_life_return", sa.JSON(), nullable=False),
        sa.Column("human_time_required", sa.JSON(), nullable=False),
        sa.Column("human_signature_impact", sa.JSON(), nullable=False),
        sa.Column("triggered_capabilities", sa.JSON(), nullable=False),
        sa.Column("capability_score_ids", sa.JSON(), nullable=False),
        sa.Column("supporting_evidence_ids", sa.JSON(), nullable=False),
        sa.Column("rationale", sa.JSON(), nullable=False),
        sa.Column("calculation_trace", sa.JSON(), nullable=False),
        sa.Column("recommended_execution_path", sa.String(length=20), nullable=False),
        sa.Column("success_criteria", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("generated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "priority_score >= 0.0 AND priority_score <= 100.0",
            name=op.f("ck_recommendations_priority_range"),
        ),
        sa.CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name=op.f("ck_recommendations_recommendation_confidence_range"),
        ),
        sa.CheckConstraint(
            "risk_score >= 0.0 AND risk_score <= 1.0",
            name=op.f("ck_recommendations_risk_range"),
        ),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["pbhs_assessments.assessment_id"],
            name=op.f("fk_recommendations_assessment_id_pbhs_assessments"),
        ),
        sa.PrimaryKeyConstraint("recommendation_id", name=op.f("pk_recommendations")),
        sa.UniqueConstraint(
            "assessment_id",
            "recommendation_type",
            name="uq_recommendations_assessment_type",
        ),
    )
    op.create_index(
        op.f("ix_recommendations_assessment_id"),
        "recommendations",
        ["assessment_id"],
        unique=False,
    )
    op.create_index(
        "ix_recommendations_assessment_priority",
        "recommendations",
        ["assessment_id", "priority_score"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_recommendations_assessment_priority", table_name="recommendations")
    op.drop_index(op.f("ix_recommendations_assessment_id"), table_name="recommendations")
    op.drop_table("recommendations")
