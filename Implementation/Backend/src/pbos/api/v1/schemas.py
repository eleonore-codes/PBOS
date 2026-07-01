from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from pbos.domain.enums import (
    AssessmentStatus,
    EvidenceSource,
    QuestionStatus,
    RecommendationCategory,
    RecommendationExecutionPath,
    RecommendationStatus,
    RecommendationType,
)


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    name: str
    email: str
    created_at: datetime


class BusinessCreate(BaseModel):
    user_id: str
    name: str = Field(min_length=1, max_length=200)
    industry: str = Field(min_length=1, max_length=200)
    business_stage: str | None = None
    primary_business_model: str | None = None
    vision_of_life_version: str | None = None
    business_vision_version: str | None = None


class BusinessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    business_id: str
    user_id: str
    name: str
    industry: str
    created_at: datetime
    business_stage: str | None
    primary_business_model: str | None
    vision_of_life_version: str | None
    business_vision_version: str | None


class AssessmentCreate(BaseModel):
    pbhs_version: str = Field(min_length=1, max_length=50)


class AssessmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    assessment_id: str
    business_id: str
    pbhs_version: str
    status: AssessmentStatus
    created_at: datetime
    completed_at: datetime | None


class AssessmentQuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    assessment_question_id: str
    assessment_id: str
    question_id: str
    question_version: str
    capability: str
    construct_: str = Field(alias="construct", serialization_alias="construct")
    question_text: str
    response_scale: str
    required: bool
    order_index: int
    source_status: str
    created_at: datetime


class AssessmentProgressRead(BaseModel):
    assessment_id: str
    status: AssessmentStatus
    total_required_questions: int
    answered_required_questions: int
    percent_complete: float
    missing_question_ids: list[str]
    missing_capabilities: list[str]
    locked: bool


class QuestionCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    capability: str = Field(min_length=1, max_length=150)
    construct_: str = Field(
        alias="construct",
        serialization_alias="construct",
        min_length=1,
        max_length=150,
    )
    question_text: str = Field(min_length=1, max_length=1000)
    response_scale: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=50)
    status: QuestionStatus = QuestionStatus.ACTIVE


class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    question_id: str
    capability: str
    construct_: str = Field(alias="construct", serialization_alias="construct")
    question_text: str
    response_scale: str
    version: str
    status: QuestionStatus


class ResponseCreate(BaseModel):
    question_id: str
    response_value: Any


class ResponseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    response_id: str
    assessment_id: str
    question_id: str
    question_version: str
    response_value: Any
    submitted_at: datetime


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evidence_id: str
    assessment_id: str
    response_id: str | None
    evidence_source: EvidenceSource
    related_capability: str
    source_reference: str
    evidence_value: Any
    confidence: float
    created_at: datetime


class ResponseSubmissionRead(BaseModel):
    response: ResponseRead
    evidence: EvidenceRead


class CapabilityScoreRead(BaseModel):
    capability_score_id: str
    assessment_id: str
    capability: str
    score: float
    maturity_level: int
    confidence: float
    calculation_method: str
    evidence_ids: list[str]
    scored_at: datetime


class AssessmentScoreRead(BaseModel):
    assessment_id: str
    status: AssessmentStatus
    overall_score: float
    overall_confidence: float
    calculation_method: str
    scored_at: datetime
    capability_scores: list[CapabilityScoreRead]


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recommendation_id: str
    assessment_id: str
    rule_id: str
    rule_version: str
    template_id: str
    template_version: str
    recommendation_type: RecommendationType
    category: RecommendationCategory
    title: str
    description: str
    priority: str
    priority_score: float
    priority_rationale: str
    confidence: float
    confidence_label: str
    risk_score: float
    risk_label: str
    expected_business_return: dict[str, Any]
    expected_life_return: dict[str, Any]
    human_time_required: dict[str, Any]
    human_signature_impact: dict[str, Any]
    triggered_capabilities: list[str]
    capability_score_ids: list[str]
    supporting_evidence_ids: list[str]
    rationale: dict[str, Any]
    calculation_trace: dict[str, Any]
    recommended_execution_path: RecommendationExecutionPath
    success_criteria: list[str]
    status: RecommendationStatus
    created_at: datetime
    generated_at: datetime


class RecommendationGenerationRunRead(BaseModel):
    run_id: str
    assessment_id: str
    engine_version: str
    rule_set_version: str
    started_at: datetime
    completed_at: datetime | None
    status: str
    error_summary: str | None


class RecommendationPortfolioRead(BaseModel):
    assessment_id: str
    status: AssessmentStatus
    engine_version: str
    rule_set_version: str
    generated_at: datetime
    recommendations: list[RecommendationRead]
    generation_run: RecommendationGenerationRunRead


class RecommendationExplanationRead(BaseModel):
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    rationale: dict[str, Any]
    calculation_trace: dict[str, Any]
    priority_rationale: str


class RecommendationEvidenceRead(BaseModel):
    recommendation_id: str
    recommendation_type: RecommendationType
    capability_score_ids: list[str]
    supporting_evidence_ids: list[str]
    triggered_capabilities: list[str]
