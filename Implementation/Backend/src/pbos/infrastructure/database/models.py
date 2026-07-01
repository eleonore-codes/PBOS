from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pbos.domain.enums import (
    AssessmentStatus,
    EvidenceSource,
    QuestionStatus,
    RecommendationCategory,
    RecommendationExecutionPath,
    RecommendationStatus,
    RecommendationType,
)
from pbos.infrastructure.database.base import Base


def enum_values(enum_cls) -> list[str]:
    return [item.value for item in enum_cls]


def new_uuid() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    businesses: Mapped[list["Business"]] = relationship(back_populates="user")


class Business(Base):
    __tablename__ = "businesses"

    business_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    industry: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    business_stage: Mapped[str | None] = mapped_column(String(100))
    primary_business_model: Mapped[str | None] = mapped_column(String(100))
    vision_of_life_version: Mapped[str | None] = mapped_column(String(50))
    business_vision_version: Mapped[str | None] = mapped_column(String(50))

    user: Mapped[User] = relationship(back_populates="businesses")
    assessments: Mapped[list["PBHSAssessment"]] = relationship(back_populates="business")


class PBHSAssessment(Base):
    __tablename__ = "pbhs_assessments"

    assessment_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    business_id: Mapped[str] = mapped_column(
        ForeignKey("businesses.business_id"), nullable=False, index=True
    )
    pbhs_version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(AssessmentStatus, native_enum=False, values_callable=enum_values),
        nullable=False,
        default=AssessmentStatus.DRAFT,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    overall_score: Mapped[float | None] = mapped_column()
    overall_confidence: Mapped[float | None] = mapped_column()
    scoring_method: Mapped[str | None] = mapped_column(String(100))
    scored_at: Mapped[datetime | None] = mapped_column(DateTime)

    business: Mapped[Business] = relationship(back_populates="assessments")
    assessment_questions: Mapped[list["PBHSAssessmentQuestion"]] = relationship(
        back_populates="assessment",
        order_by="PBHSAssessmentQuestion.order_index",
    )
    responses: Mapped[list["PBHSResponse"]] = relationship(back_populates="assessment")
    evidence_items: Mapped[list["EvidenceItem"]] = relationship(back_populates="assessment")
    capability_scores: Mapped[list["CapabilityScore"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
    )
    recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
    )


class PBHSQuestion(Base):
    __tablename__ = "pbhs_questions"
    __table_args__ = (
        UniqueConstraint("question_id", "version", name="uq_pbhs_questions_question_version"),
        Index("ix_pbhs_questions_capability_construct", "capability", "construct"),
    )

    question_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    capability: Mapped[str] = mapped_column(String(150), nullable=False)
    construct: Mapped[str] = mapped_column(String(150), nullable=False)
    question_text: Mapped[str] = mapped_column(String(1000), nullable=False)
    response_scale: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[QuestionStatus] = mapped_column(
        Enum(QuestionStatus, native_enum=False, values_callable=enum_values),
        nullable=False,
        default=QuestionStatus.ACTIVE,
    )

    responses: Mapped[list["PBHSResponse"]] = relationship(back_populates="question")
    assessment_questions: Mapped[list["PBHSAssessmentQuestion"]] = relationship(
        back_populates="question"
    )


class PBHSAssessmentQuestion(Base):
    __tablename__ = "pbhs_assessment_questions"
    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "question_id",
            name="uq_pbhs_assessment_questions_assessment_question",
        ),
        Index(
            "ix_pbhs_assessment_questions_assessment_capability",
            "assessment_id",
            "capability",
        ),
    )

    assessment_question_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=new_uuid
    )
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_assessments.assessment_id"), nullable=False, index=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_questions.question_id"), nullable=False, index=True
    )
    question_version: Mapped[str] = mapped_column(String(50), nullable=False)
    capability: Mapped[str] = mapped_column(String(150), nullable=False)
    construct: Mapped[str] = mapped_column(String(150), nullable=False)
    question_text: Mapped[str] = mapped_column(String(1000), nullable=False)
    response_scale: Mapped[str] = mapped_column(String(100), nullable=False)
    required: Mapped[bool] = mapped_column(nullable=False, default=True)
    order_index: Mapped[int] = mapped_column(nullable=False)
    source_status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    assessment: Mapped[PBHSAssessment] = relationship(back_populates="assessment_questions")
    question: Mapped[PBHSQuestion] = relationship(back_populates="assessment_questions")


class PBHSResponse(Base):
    __tablename__ = "pbhs_responses"
    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "question_id",
            name="uq_pbhs_responses_assessment_question",
        ),
    )

    response_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_assessments.assessment_id"), nullable=False, index=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_questions.question_id"), nullable=False, index=True
    )
    question_version: Mapped[str] = mapped_column(String(50), nullable=False)
    response_value: Mapped[Any] = mapped_column(JSON, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    assessment: Mapped[PBHSAssessment] = relationship(back_populates="responses")
    question: Mapped[PBHSQuestion] = relationship(back_populates="responses")
    evidence_items: Mapped[list["EvidenceItem"]] = relationship(back_populates="response")


class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    __table_args__ = (
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="confidence_range"),
        Index("ix_evidence_items_assessment_capability", "assessment_id", "related_capability"),
    )

    evidence_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_assessments.assessment_id"), nullable=False, index=True
    )
    response_id: Mapped[str | None] = mapped_column(ForeignKey("pbhs_responses.response_id"))
    evidence_source: Mapped[EvidenceSource] = mapped_column(
        Enum(EvidenceSource, native_enum=False, values_callable=enum_values),
        nullable=False,
    )
    related_capability: Mapped[str] = mapped_column(String(150), nullable=False)
    source_reference: Mapped[str] = mapped_column(String(500), nullable=False)
    evidence_value: Mapped[Any] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    assessment: Mapped[PBHSAssessment] = relationship(back_populates="evidence_items")
    response: Mapped[PBHSResponse | None] = relationship(back_populates="evidence_items")


class CapabilityScore(Base):
    __tablename__ = "capability_scores"
    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 100.0", name="capability_score_range"),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="capability_confidence_range",
        ),
        CheckConstraint("maturity_level >= 1 AND maturity_level <= 5", name="maturity_level_range"),
        UniqueConstraint(
            "assessment_id",
            "capability",
            name="uq_capability_scores_assessment_capability",
        ),
        Index("ix_capability_scores_assessment_capability", "assessment_id", "capability"),
    )

    capability_score_id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=new_uuid
    )
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_assessments.assessment_id"), nullable=False, index=True
    )
    capability: Mapped[str] = mapped_column(String(150), nullable=False)
    score: Mapped[float] = mapped_column(nullable=False)
    maturity_level: Mapped[int] = mapped_column(nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    calculation_method: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    scored_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    assessment: Mapped[PBHSAssessment] = relationship(back_populates="capability_scores")


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        CheckConstraint("priority_score >= 0.0 AND priority_score <= 100.0", name="priority_range"),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="recommendation_confidence_range",
        ),
        CheckConstraint("risk_score >= 0.0 AND risk_score <= 1.0", name="risk_range"),
        UniqueConstraint(
            "assessment_id",
            "recommendation_type",
            name="uq_recommendations_assessment_type",
        ),
        Index("ix_recommendations_assessment_priority", "assessment_id", "priority_score"),
    )

    recommendation_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_uuid)
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("pbhs_assessments.assessment_id"), nullable=False, index=True
    )
    rule_id: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(50), nullable=False)
    template_id: Mapped[str] = mapped_column(String(100), nullable=False)
    template_version: Mapped[str] = mapped_column(String(50), nullable=False)
    recommendation_type: Mapped[RecommendationType] = mapped_column(
        Enum(RecommendationType, native_enum=False, values_callable=enum_values),
        nullable=False,
    )
    category: Mapped[RecommendationCategory] = mapped_column(
        Enum(RecommendationCategory, native_enum=False, values_callable=enum_values),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    priority_score: Mapped[float] = mapped_column(nullable=False)
    priority_rationale: Mapped[str] = mapped_column(String(1000), nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_score: Mapped[float] = mapped_column(nullable=False)
    risk_label: Mapped[str] = mapped_column(String(50), nullable=False)
    expected_business_return: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    expected_life_return: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    human_time_required: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    human_signature_impact: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    triggered_capabilities: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    capability_score_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    supporting_evidence_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    rationale: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    calculation_trace: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    recommended_execution_path: Mapped[RecommendationExecutionPath] = mapped_column(
        Enum(RecommendationExecutionPath, native_enum=False, values_callable=enum_values),
        nullable=False,
    )
    success_criteria: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, native_enum=False, values_callable=enum_values),
        nullable=False,
        default=RecommendationStatus.CANDIDATE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utc_now)

    assessment: Mapped[PBHSAssessment] = relationship(back_populates="recommendations")


def coerce_uuid(value: UUID | str) -> str:
    return str(value)
