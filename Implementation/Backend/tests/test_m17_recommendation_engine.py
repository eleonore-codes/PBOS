import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from pbos.domain.enums import AssessmentStatus, QuestionStatus, RecommendationType
from pbos.infrastructure.database.base import Base
from pbos.infrastructure.database.models import Business, PBHSQuestion, User
from pbos.infrastructure.database.session import get_session
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyRecommendationRepository,
)
from pbos.main import create_app
from pbos.services.assessment_service import AssessmentService
from pbos.services.recommendation_service import RecommendationService
from pbos.services.scoring_service import ScoringService


CAPABILITIES = [
    "Human Signature",
    "Knowledge Assets",
    "Podcast Assets",
    "Trust",
    "Business Systems",
    "AI Leverage",
    "Business Return",
    "Life Return",
]


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def seed_business_and_capability_questions(session: Session) -> tuple[Business, list[PBHSQuestion]]:
    user = User(name="Customer Zero", email="customer@example.com")
    session.add(user)
    session.flush()
    business = Business(user_id=user.user_id, name="PBOS Studio", industry="Education")
    questions = [
        PBHSQuestion(
            capability=capability,
            construct=f"{capability} Construct",
            question_text=f"{capability} question {question_number}",
            response_scale="likert_1_5",
            version="0.1",
            status=QuestionStatus.ACTIVE,
        )
        for capability in CAPABILITIES
        for question_number in range(1, 4)
    ]
    session.add_all([business, *questions])
    session.commit()
    return business, questions


def score_assessment(
    session: Session,
    *,
    values_by_capability: dict[str, list[int]],
):
    business, questions = seed_business_and_capability_questions(session)
    assessment_service = AssessmentService(session)
    assessment = assessment_service.start_assessment(
        business_id=business.business_id,
        pbhs_version="0.1",
    )

    for capability in CAPABILITIES:
        capability_questions = [
            question for question in questions if question.capability == capability
        ]
        for question, response_value in zip(
            capability_questions,
            values_by_capability[capability],
            strict=True,
        ):
            assessment_service.submit_response(
                assessment_id=assessment.assessment_id,
                question_id=question.question_id,
                response_value=response_value,
            )

    assessment_service.submit_assessment(assessment.assessment_id)
    ScoringService(session).score_assessment(assessment.assessment_id)
    return assessment


def trigger_all_template_rules() -> dict[str, list[int]]:
    return {
        "Human Signature": [5, 5, 5],
        "Knowledge Assets": [3, 3, 3],
        "Podcast Assets": [4, 4, 4],
        "Trust": [4, 4, 4],
        "Business Systems": [2, 2, 2],
        "AI Leverage": [2, 2, 2],
        "Business Return": [2, 2, 2],
        "Life Return": [3, 3, 3],
    }


def test_recommendation_generation_uses_templates_and_stable_types() -> None:
    session = create_session()
    assessment = score_assessment(session, values_by_capability=trigger_all_template_rules())

    result = RecommendationService(session).generate_recommendations(assessment.assessment_id)
    recommendation_types = {
        recommendation.recommendation_type for recommendation in result.recommendations
    }

    assert result.status == AssessmentStatus.RECOMMENDATIONS_GENERATED
    assert result.generation_run.status == "completed"
    assert result.generation_run.engine_version == "m17_recommendation_engine_v1"
    assert recommendation_types == {
        RecommendationType.SPONSOR_READINESS,
        RecommendationType.CONTENT_SYSTEM,
        RecommendationType.EMAIL_FUNNEL,
        RecommendationType.AUTOMATION,
        RecommendationType.KNOWLEDGE_LIBRARY,
    }
    assert all(recommendation.template_id for recommendation in result.recommendations)
    assert all(recommendation.rule_id for recommendation in result.recommendations)


def test_recommendations_are_explainable_and_trace_evidence() -> None:
    session = create_session()
    assessment = score_assessment(session, values_by_capability=trigger_all_template_rules())

    recommendation = RecommendationService(session).generate_recommendations(
        assessment.assessment_id
    ).recommendations[0]

    assert recommendation.rationale["why_generated"]
    assert recommendation.triggered_capabilities
    assert recommendation.capability_score_ids
    assert recommendation.supporting_evidence_ids
    assert recommendation.expected_business_return["score"] > 0
    assert recommendation.expected_life_return["score"] > 0
    assert recommendation.human_time_required["estimated_hours_required"]["max"] > 0
    assert 0 <= recommendation.confidence <= 1
    assert 0 <= recommendation.risk_score <= 1
    assert recommendation.priority_rationale
    assert recommendation.calculation_trace["template"]["recommendation_type"] == (
        recommendation.recommendation_type.value
    )


def test_recommendation_generation_is_idempotent_and_deterministic() -> None:
    session = create_session()
    assessment = score_assessment(session, values_by_capability=trigger_all_template_rules())
    service = RecommendationService(session)

    first = service.generate_recommendations(assessment.assessment_id)
    first_ids = [recommendation.recommendation_id for recommendation in first.recommendations]
    first_order = [recommendation.recommendation_type for recommendation in first.recommendations]
    second = service.generate_recommendations(assessment.assessment_id)
    second_ids = [recommendation.recommendation_id for recommendation in second.recommendations]
    second_order = [recommendation.recommendation_type for recommendation in second.recommendations]
    persisted = SqlAlchemyRecommendationRepository(session).list_for_assessment(
        assessment.assessment_id
    )

    assert second_ids == first_ids
    assert second_order == first_order
    assert len(persisted) == 5


def test_generation_requires_scored_assessment() -> None:
    session = create_session()
    business, _ = seed_business_and_capability_questions(session)
    assessment = AssessmentService(session).start_assessment(
        business_id=business.business_id,
        pbhs_version="0.1",
    )

    with pytest.raises(ValueError, match="assessment_not_scored"):
        RecommendationService(session).generate_recommendations(assessment.assessment_id)


def test_recommendation_api_generates_lists_explains_and_returns_evidence() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    def override_get_session():
        with testing_session() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)

    user_response = client.post(
        "/api/v1/users",
        json={"name": "Customer Zero", "email": "customer-zero@example.com"},
    )
    business_response = client.post(
        "/api/v1/businesses",
        json={
            "user_id": user_response.json()["user_id"],
            "name": "PBOS Studio",
            "industry": "Education",
        },
    )
    question_ids_by_capability: dict[str, list[str]] = {}
    for capability in CAPABILITIES:
        question_ids_by_capability[capability] = []
        for question_number in range(1, 4):
            response = client.post(
                "/api/v1/pbhs/questions",
                json={
                    "capability": capability,
                    "construct": f"{capability} Construct",
                    "question_text": f"{capability} question {question_number}",
                    "response_scale": "likert_1_5",
                    "version": "0.1",
                    "status": "active",
                },
            )
            question_ids_by_capability[capability].append(response.json()["question_id"])

    assessment_response = client.post(
        f"/api/v1/businesses/{business_response.json()['business_id']}/assessments",
        json={"pbhs_version": "0.1"},
    )
    assessment_id = assessment_response.json()["assessment_id"]
    for capability, values in trigger_all_template_rules().items():
        for question_id, response_value in zip(
            question_ids_by_capability[capability],
            values,
            strict=True,
        ):
            client.post(
                f"/api/v1/assessments/{assessment_id}/responses",
                json={"question_id": question_id, "response_value": response_value},
            )
    client.post(f"/api/v1/assessments/{assessment_id}/submit")
    client.post(f"/api/v1/assessments/{assessment_id}/score")

    generate_response = client.post(
        f"/api/v1/pbhs/assessments/{assessment_id}/recommendations/generate"
    )
    list_response = client.get(f"/api/v1/pbhs/assessments/{assessment_id}/recommendations")
    recommendation_id = generate_response.json()["recommendations"][0]["recommendation_id"]
    explain_response = client.get(f"/api/v1/recommendations/{recommendation_id}/explain")
    evidence_response = client.get(f"/api/v1/recommendations/{recommendation_id}/evidence")

    assert generate_response.status_code == 200
    assert list_response.status_code == 200
    assert len(generate_response.json()["recommendations"]) == 5
    assert list_response.json()[0]["recommendation_id"] == recommendation_id
    assert generate_response.json()["recommendations"][0]["recommendation_type"]
    assert explain_response.status_code == 200
    assert explain_response.json()["rationale"]["why_generated"]
    assert evidence_response.status_code == 200
    assert evidence_response.json()["supporting_evidence_ids"]
