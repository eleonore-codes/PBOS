from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pbos.domain.enums import EvidenceSource, QuestionStatus
from pbos.infrastructure.database.base import Base
from pbos.infrastructure.database.models import Business, PBHSQuestion, User
from pbos.infrastructure.repositories.sqlalchemy_repositories import SqlAlchemyEvidenceRepository
from pbos.services.assessment_service import AssessmentService


def create_session() -> Session:
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_response_submission_creates_versioned_self_report_evidence() -> None:
    session = create_session()
    user = User(name="Customer Zero", email="customer@example.com")
    session.add(user)
    session.flush()
    business = Business(user_id=user.user_id, name="PBOS Studio", industry="Education")
    question = PBHSQuestion(
        capability="Human Signature",
        construct="Knowledge Capture",
        question_text="How consistently do you capture reusable knowledge?",
        response_scale="likert_1_5",
        version="0.1",
        status=QuestionStatus.ACTIVE,
    )
    session.add_all([business, question])
    session.commit()

    service = AssessmentService(session)
    assessment = service.start_assessment(business_id=business.business_id, pbhs_version="0.1")

    response, evidence = service.submit_response(
        assessment_id=assessment.assessment_id,
        question_id=question.question_id,
        response_value=4,
    )

    assert response.question_version == "0.1"
    assert evidence.evidence_source == EvidenceSource.SELF_REPORT
    assert evidence.response_id == response.response_id
    assert evidence.related_capability == "Human Signature"
    assert evidence.source_reference == f"pbhs_response:{question.question_id}"

    evidence_items = SqlAlchemyEvidenceRepository(session).list_for_assessment(
        assessment.assessment_id
    )
    assert [item.evidence_id for item in evidence_items] == [evidence.evidence_id]
