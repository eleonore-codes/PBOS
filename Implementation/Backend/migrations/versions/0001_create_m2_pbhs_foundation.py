"""create m2 pbhs foundation

Revision ID: 0001_create_m2_pbhs_foundation
Revises:
Create Date: 2026-07-01
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_m2_pbhs_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "pbhs_questions",
        sa.Column("question_id", sa.String(length=36), nullable=False),
        sa.Column("capability", sa.String(length=150), nullable=False),
        sa.Column("construct", sa.String(length=150), nullable=False),
        sa.Column("question_text", sa.String(length=1000), nullable=False),
        sa.Column("response_scale", sa.String(length=100), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.Enum("active", "experimental", "retired", name="questionstatus", native_enum=False),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("question_id", name=op.f("pk_pbhs_questions")),
        sa.UniqueConstraint(
            "question_id",
            "version",
            name="uq_pbhs_questions_question_version",
        ),
    )
    op.create_index(
        "ix_pbhs_questions_capability_construct",
        "pbhs_questions",
        ["capability", "construct"],
        unique=False,
    )

    op.create_table(
        "businesses",
        sa.Column("business_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("industry", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("business_stage", sa.String(length=100), nullable=True),
        sa.Column("primary_business_model", sa.String(length=100), nullable=True),
        sa.Column("vision_of_life_version", sa.String(length=50), nullable=True),
        sa.Column("business_vision_version", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], name=op.f("fk_businesses_user_id_users")),
        sa.PrimaryKeyConstraint("business_id", name=op.f("pk_businesses")),
    )
    op.create_index(op.f("ix_businesses_user_id"), "businesses", ["user_id"], unique=False)

    op.create_table(
        "pbhs_assessments",
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("business_id", sa.String(length=36), nullable=False),
        sa.Column("pbhs_version", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "draft",
                "submitted",
                "scored",
                "recommendations_generated",
                "reviewed",
                "reported",
                name="assessmentstatus",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.business_id"],
            name=op.f("fk_pbhs_assessments_business_id_businesses"),
        ),
        sa.PrimaryKeyConstraint("assessment_id", name=op.f("pk_pbhs_assessments")),
    )
    op.create_index(
        op.f("ix_pbhs_assessments_business_id"),
        "pbhs_assessments",
        ["business_id"],
        unique=False,
    )

    op.create_table(
        "pbhs_responses",
        sa.Column("response_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("question_id", sa.String(length=36), nullable=False),
        sa.Column("question_version", sa.String(length=50), nullable=False),
        sa.Column("response_value", sa.JSON(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["pbhs_assessments.assessment_id"],
            name=op.f("fk_pbhs_responses_assessment_id_pbhs_assessments"),
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["pbhs_questions.question_id"],
            name=op.f("fk_pbhs_responses_question_id_pbhs_questions"),
        ),
        sa.PrimaryKeyConstraint("response_id", name=op.f("pk_pbhs_responses")),
        sa.UniqueConstraint(
            "assessment_id",
            "question_id",
            name="uq_pbhs_responses_assessment_question",
        ),
    )
    op.create_index(
        op.f("ix_pbhs_responses_assessment_id"),
        "pbhs_responses",
        ["assessment_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pbhs_responses_question_id"),
        "pbhs_responses",
        ["question_id"],
        unique=False,
    )

    op.create_table(
        "evidence_items",
        sa.Column("evidence_id", sa.String(length=36), nullable=False),
        sa.Column("assessment_id", sa.String(length=36), nullable=False),
        sa.Column("response_id", sa.String(length=36), nullable=True),
        sa.Column(
            "evidence_source",
            sa.Enum(
                "self_report",
                "behavioral",
                "business",
                "portfolio",
                "ai_interview",
                "longitudinal",
                name="evidencesource",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("related_capability", sa.String(length=150), nullable=False),
        sa.Column("source_reference", sa.String(length=500), nullable=False),
        sa.Column("evidence_value", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name=op.f("ck_evidence_items_confidence_range")),
        sa.ForeignKeyConstraint(
            ["assessment_id"],
            ["pbhs_assessments.assessment_id"],
            name=op.f("fk_evidence_items_assessment_id_pbhs_assessments"),
        ),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["pbhs_responses.response_id"],
            name=op.f("fk_evidence_items_response_id_pbhs_responses"),
        ),
        sa.PrimaryKeyConstraint("evidence_id", name=op.f("pk_evidence_items")),
    )
    op.create_index(
        "ix_evidence_items_assessment_capability",
        "evidence_items",
        ["assessment_id", "related_capability"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evidence_items_assessment_id"),
        "evidence_items",
        ["assessment_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_evidence_items_assessment_id"), table_name="evidence_items")
    op.drop_index("ix_evidence_items_assessment_capability", table_name="evidence_items")
    op.drop_table("evidence_items")
    op.drop_index(op.f("ix_pbhs_responses_question_id"), table_name="pbhs_responses")
    op.drop_index(op.f("ix_pbhs_responses_assessment_id"), table_name="pbhs_responses")
    op.drop_table("pbhs_responses")
    op.drop_index(op.f("ix_pbhs_assessments_business_id"), table_name="pbhs_assessments")
    op.drop_table("pbhs_assessments")
    op.drop_index(op.f("ix_businesses_user_id"), table_name="businesses")
    op.drop_table("businesses")
    op.drop_index("ix_pbhs_questions_capability_construct", table_name="pbhs_questions")
    op.drop_table("pbhs_questions")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
