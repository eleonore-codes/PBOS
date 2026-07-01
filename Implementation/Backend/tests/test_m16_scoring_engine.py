import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from pbos.domain.enums import AssessmentStatus, QuestionStatus
from pbos.infrastructure.database.base import Base
from pbos.infrastructure.database.models import Business, PBHSQuestion, User
from pbos.infrastructure.database.session import get_session
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyCapabilityScoreRepository,
    SqlAlchemyEvidenceRepository,
)
from pbos.main import create_app
from pbos.services.assessment_service import AssessmentService
from pbos.services.scoring_service import ScoringService, maturity_level, normalize_response


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


def seed_business_and_capability_questions(
    session: Session,
    *,
    question_count: int = 5,
) -> tuple[Business, list[PBHSQuestion]]:
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
        for question_number in range(1, question_count + 1)
    ]
    session.add_all([business, *questions])
    session.commit()
    return business, questions


def submit_complete_assessment(
    session: Session,
    *,
    values_by_capability: dict[str, list[int]],
) -> tuple[AssessmentService, object]:
    business, questions = seed_business_and_capability_questions(session)
    service = AssessmentService(session)
    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")

    for capability in CAPABILITIES:
        capability_questions = [
            question for question in questions if question.capability == capability
        ]
        for question, response_value in zip(
            capability_questions,
            values_by_capability[capability],
            strict=True,
        ):
            service.submit_response(
                assessment_id=assessment.assessment_id,
                question_id=question.question_id,
                response_value=response_value,
            )

    return service, service.submit_assessment(assessment.assessment_id)


def test_likert_1_to_5_normalization_maps_to_0_to_100() -> None:
    assert [normalize_response("likert_1_5", value) for value in range(1, 6)] == [
        0,
        25,
        50,
        75,
        100,
    ]


def test_maturity_levels_classify_boundaries() -> None:
    assert maturity_level(0) == 1
    assert maturity_level(20) == 1
    assert maturity_level(20.01) == 2
    assert maturity_level(40) == 2
    assert maturity_level(60) == 3
    assert maturity_level(80) == 4
    assert maturity_level(80.01) == 5
    assert maturity_level(100) == 5


def test_scoring_calculates_capability_overall_confidence_maturity_and_provenance() -> None:
    session = create_session()
    values_by_capability = {
        "Human Signature": [1, 2, 3, 4, 5],
        "Knowledge Assets": [5, 5, 5, 5, 5],
        "Podcast Assets": [4, 4, 4, 4, 4],
        "Trust": [3, 3, 3, 3, 3],
        "Business Systems": [2, 2, 2, 2, 2],
        "AI Leverage": [1, 1, 1, 1, 1],
        "Business Return": [5, 4, 3, 2, 1],
        "Life Return": [4, 5, 4, 5, 4],
    }
    _, assessment = submit_complete_assessment(
        session,
        values_by_capability=values_by_capability,
    )

    result = ScoringService(session).score_assessment(assessment.assessment_id)
    scores = {score.capability: score for score in result.capability_scores}
    evidence_count = len(
        SqlAlchemyEvidenceRepository(session).list_for_assessment(assessment.assessment_id)
    )

    assert scores["Human Signature"].score == 50
    assert scores["Human Signature"].maturity_level == 3
    assert scores["Human Signature"].confidence == 0.4
    assert len(scores["Human Signature"].evidence_ids) == 5
    assert scores["Knowledge Assets"].score == 100
    assert scores["AI Leverage"].score == 0
    assert result.overall_score == 54.38
    assert result.overall_confidence == 0.4
    assert result.status == AssessmentStatus.SCORED
    assert evidence_count == 40


def test_scoring_uses_assessment_question_snapshot_not_live_question_changes() -> None:
    session = create_session()
    business, questions = seed_business_and_capability_questions(session, question_count=1)
    assessment_service = AssessmentService(session)
    assessment = assessment_service.start_assessment(
        business_id=business.business_id,
        pbhs_version="0.1",
    )
    original_capability = questions[0].capability
    questions[0].capability = "Changed Capability"
    session.commit()

    for question in questions:
        assessment_service.submit_response(
            assessment_id=assessment.assessment_id,
            question_id=question.question_id,
            response_value=4,
        )
    assessment_service.submit_assessment(assessment.assessment_id)

    result = ScoringService(session).score_assessment(assessment.assessment_id)

    assert original_capability in {score.capability for score in result.capability_scores}
    assert "Changed Capability" not in {score.capability for score in result.capability_scores}


def test_scoring_persists_scores_changes_status_and_is_idempotent() -> None:
    session = create_session()
    _, assessment = submit_complete_assessment(
        session,
        values_by_capability={capability: [4, 4, 4, 4, 4] for capability in CAPABILITIES},
    )
    service = ScoringService(session)

    first_result = service.score_assessment(assessment.assessment_id)
    second_result = service.score_assessment(assessment.assessment_id)
    persisted_scores = SqlAlchemyCapabilityScoreRepository(session).list_for_assessment(
        assessment.assessment_id
    )

    assert first_result.overall_score == 75
    assert second_result.overall_score == first_result.overall_score
    assert [score.capability_score_id for score in second_result.capability_scores] == [
        score.capability_score_id for score in first_result.capability_scores
    ]
    assert len(persisted_scores) == len(CAPABILITIES)
    assert service.assessments.get(assessment.assessment_id).status == AssessmentStatus.SCORED


def test_scoring_draft_assessment_fails() -> None:
    session = create_session()
    business, _ = seed_business_and_capability_questions(session)
    assessment = AssessmentService(session).start_assessment(
        business_id=business.business_id,
        pbhs_version="0.1",
    )

    with pytest.raises(ValueError, match="assessment_not_submitted"):
        ScoringService(session).score_assessment(assessment.assessment_id)


def test_score_api_returns_summary_capability_scores_and_provenance() -> None:
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
    question_response = client.post(
        "/api/v1/pbhs/questions",
        json={
            "capability": "Human Signature",
            "construct": "Differentiation",
            "question_text": "My business communicates expertise competitors cannot copy.",
            "response_scale": "likert_1_5",
            "version": "0.1",
            "status": "active",
        },
    )
    assessment_response = client.post(
        f"/api/v1/businesses/{business_response.json()['business_id']}/assessments",
        json={"pbhs_version": "0.1"},
    )
    assessment_id = assessment_response.json()["assessment_id"]
    question_id = question_response.json()["question_id"]
    draft_score_response = client.post(f"/api/v1/assessments/{assessment_id}/score")

    client.post(
        f"/api/v1/assessments/{assessment_id}/responses",
        json={"question_id": question_id, "response_value": 5},
    )
    client.post(f"/api/v1/assessments/{assessment_id}/submit")
    score_response = client.post(f"/api/v1/assessments/{assessment_id}/score")
    get_response = client.get(f"/api/v1/assessments/{assessment_id}/scores")
    score_payload = score_response.json()

    assert draft_score_response.status_code == 409
    assert draft_score_response.json()["detail"] == "assessment_not_submitted"
    assert score_response.status_code == 200
    assert get_response.status_code == 200
    assert score_payload["overall_score"] == 100
    assert score_payload["overall_confidence"] == 0.4
    assert score_payload["status"] == "scored"
    assert score_payload["capability_scores"][0]["score"] == 100
    assert score_payload["capability_scores"][0]["maturity_level"] == 5
    assert len(score_payload["capability_scores"][0]["evidence_ids"]) == 1
