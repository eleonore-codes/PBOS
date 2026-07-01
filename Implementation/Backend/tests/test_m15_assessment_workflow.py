import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

from pbos.domain.enums import AssessmentStatus, EvidenceSource, QuestionStatus
from pbos.infrastructure.database.base import Base
from pbos.infrastructure.database.models import Business, PBHSQuestion, User
from pbos.infrastructure.database.session import get_session
from pbos.infrastructure.repositories.sqlalchemy_repositories import SqlAlchemyEvidenceRepository
from pbos.main import create_app
from pbos.services.assessment_service import AssessmentService


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def seed_business_and_questions(session: Session) -> tuple[Business, list[PBHSQuestion]]:
    user = User(name="Customer Zero", email="customer@example.com")
    session.add(user)
    session.flush()
    business = Business(user_id=user.user_id, name="PBOS Studio", industry="Education")
    questions = [
        PBHSQuestion(
            capability="Human Signature",
            construct="Differentiation",
            question_text="My business communicates expertise competitors cannot copy.",
            response_scale="likert_1_5",
            version="0.1",
            status=QuestionStatus.ACTIVE,
        ),
        PBHSQuestion(
            capability="Knowledge Assets",
            construct="Reusable IP",
            question_text="I regularly convert expertise into reusable assets.",
            response_scale="likert_1_5",
            version="0.1",
            status=QuestionStatus.ACTIVE,
        ),
    ]
    session.add_all([business, *questions])
    session.commit()
    return business, questions


def test_start_assessment_snapshots_active_questions_and_freezes_question_text() -> None:
    session = create_session()
    business, questions = seed_business_and_questions(session)
    service = AssessmentService(session)

    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")
    questions[0].question_text = "Changed after assessment start."
    session.commit()

    snapshots = service.list_assessment_questions(assessment.assessment_id)

    assert [snapshot.question_id for snapshot in snapshots] == [
        question.question_id for question in questions
    ]
    assert (
        snapshots[0].question_text
        == "My business communicates expertise competitors cannot copy."
    )
    assert snapshots[0].question_version == "0.1"


def test_progress_submit_and_lock_preserve_self_report_evidence() -> None:
    session = create_session()
    business, questions = seed_business_and_questions(session)
    service = AssessmentService(session)
    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")

    service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=questions[0].question_id,
        response_value=4,
    )
    progress = service.get_progress(assessment.assessment_id)

    assert progress.answered_required_questions == 1
    assert progress.total_required_questions == 2
    assert progress.percent_complete == 50.0
    assert progress.missing_capabilities == ["Knowledge Assets"]

    with pytest.raises(ValueError, match="assessment_incomplete"):
        service.submit_assessment(assessment.assessment_id)

    response, evidence = service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=questions[1].question_id,
        response_value=5,
    )
    submitted = service.submit_assessment(assessment.assessment_id)

    assert submitted.status == AssessmentStatus.SUBMITTED
    assert submitted.completed_at is not None
    assert service.get_progress(assessment.assessment_id).locked is True
    assert evidence.evidence_source == EvidenceSource.SELF_REPORT
    assert evidence.response_id == response.response_id

    with pytest.raises(ValueError, match="assessment_locked"):
        service.submit_response(
            assessment_id=assessment.assessment_id,
            question_id=questions[0].question_id,
            response_value=3,
        )


def test_response_validation_uses_assessment_question_snapshot() -> None:
    session = create_session()
    business, questions = seed_business_and_questions(session)
    service = AssessmentService(session)
    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")
    questions[0].response_scale = "yes_no"
    session.commit()

    service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=questions[0].question_id,
        response_value=5,
    )

    with pytest.raises(ValueError, match="response_value_must_be_integer_1_to_5"):
        service.submit_response(
            assessment_id=assessment.assessment_id,
            question_id=questions[1].question_id,
            response_value=True,
        )


def test_draft_response_update_reuses_response_evidence_item() -> None:
    session = create_session()
    business, questions = seed_business_and_questions(session)
    service = AssessmentService(session)
    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")

    first_response, first_evidence = service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=questions[0].question_id,
        response_value=2,
    )
    second_response, second_evidence = service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=questions[0].question_id,
        response_value=4,
    )
    evidence_items = SqlAlchemyEvidenceRepository(session).list_for_assessment(
        assessment.assessment_id
    )

    assert second_response.response_id == first_response.response_id
    assert second_evidence.evidence_id == first_evidence.evidence_id
    assert second_evidence.evidence_value == 4
    assert len(evidence_items) == 1


def test_assessment_api_exposes_questions_progress_responses_and_submit() -> None:
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

    questions_response = client.get(f"/api/v1/assessments/{assessment_id}/questions")
    initial_progress = client.get(f"/api/v1/assessments/{assessment_id}/progress")
    response_submission = client.post(
        f"/api/v1/assessments/{assessment_id}/responses",
        json={"question_id": question_id, "response_value": 4},
    )
    responses_response = client.get(f"/api/v1/assessments/{assessment_id}/responses")
    submit_response = client.post(f"/api/v1/assessments/{assessment_id}/submit")
    locked_response = client.post(
        f"/api/v1/assessments/{assessment_id}/responses",
        json={"question_id": question_id, "response_value": 5},
    )

    assert questions_response.status_code == 200
    assert len(questions_response.json()) == 1
    assert initial_progress.json()["percent_complete"] == 0.0
    assert response_submission.status_code == 201
    assert responses_response.status_code == 200
    assert len(responses_response.json()) == 1
    assert submit_response.status_code == 200
    assert submit_response.json()["status"] == "submitted"
    assert locked_response.status_code == 409
    assert locked_response.json()["detail"] == "assessment_locked"
