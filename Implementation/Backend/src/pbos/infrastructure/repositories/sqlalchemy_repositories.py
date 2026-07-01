from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from pbos.domain.enums import EvidenceSource, QuestionStatus
from pbos.domain.repositories import (
    AssessmentRepository,
    BusinessRepository,
    CapabilityScoreRepository,
    EvidenceRepository,
    QuestionRepository,
)
from pbos.infrastructure.database.models import (
    Business,
    CapabilityScore,
    EvidenceItem,
    PBHSAssessment,
    PBHSAssessmentQuestion,
    PBHSQuestion,
    PBHSResponse,
    coerce_uuid,
)


class SqlAlchemyBusinessRepository(BusinessRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, business: Business) -> Business:
        self.session.add(business)
        self.session.flush()
        return business

    def get(self, business_id: UUID) -> Business | None:
        return self.session.get(Business, coerce_uuid(business_id))


class SqlAlchemyAssessmentRepository(AssessmentRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, assessment: PBHSAssessment) -> PBHSAssessment:
        self.session.add(assessment)
        self.session.flush()
        return assessment

    def get(self, assessment_id: UUID) -> PBHSAssessment | None:
        return self.session.get(PBHSAssessment, coerce_uuid(assessment_id))

    def add_response(self, response: PBHSResponse) -> PBHSResponse:
        self.session.add(response)
        self.session.flush()
        return response

    def list_responses(self, assessment_id: UUID) -> list[PBHSResponse]:
        statement = select(PBHSResponse).where(
            PBHSResponse.assessment_id == coerce_uuid(assessment_id)
        )
        return list(self.session.scalars(statement))

    def get_response(self, assessment_id: UUID, question_id: UUID) -> PBHSResponse | None:
        statement = select(PBHSResponse).where(
            PBHSResponse.assessment_id == coerce_uuid(assessment_id),
            PBHSResponse.question_id == coerce_uuid(question_id),
        )
        return self.session.scalars(statement).first()

    def add_assessment_question(
        self, assessment_question: PBHSAssessmentQuestion
    ) -> PBHSAssessmentQuestion:
        self.session.add(assessment_question)
        self.session.flush()
        return assessment_question

    def list_assessment_questions(self, assessment_id: UUID) -> list[PBHSAssessmentQuestion]:
        statement = (
            select(PBHSAssessmentQuestion)
            .where(PBHSAssessmentQuestion.assessment_id == coerce_uuid(assessment_id))
            .order_by(PBHSAssessmentQuestion.order_index)
        )
        return list(self.session.scalars(statement))

    def get_assessment_question(
        self, assessment_id: UUID, question_id: UUID
    ) -> PBHSAssessmentQuestion | None:
        statement = select(PBHSAssessmentQuestion).where(
            PBHSAssessmentQuestion.assessment_id == coerce_uuid(assessment_id),
            PBHSAssessmentQuestion.question_id == coerce_uuid(question_id),
        )
        return self.session.scalars(statement).first()


class SqlAlchemyQuestionRepository(QuestionRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, question: PBHSQuestion) -> PBHSQuestion:
        self.session.add(question)
        self.session.flush()
        return question

    def get(self, question_id: UUID) -> PBHSQuestion | None:
        return self.session.get(PBHSQuestion, coerce_uuid(question_id))

    def list_active(self) -> list[PBHSQuestion]:
        statement = select(PBHSQuestion).where(PBHSQuestion.status == QuestionStatus.ACTIVE)
        return list(self.session.scalars(statement))


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, evidence: EvidenceItem) -> EvidenceItem:
        self.session.add(evidence)
        self.session.flush()
        return evidence

    def list_for_assessment(self, assessment_id: UUID) -> list[EvidenceItem]:
        statement = select(EvidenceItem).where(
            EvidenceItem.assessment_id == coerce_uuid(assessment_id)
        )
        return list(self.session.scalars(statement))

    def get_for_response(self, response_id: UUID) -> EvidenceItem | None:
        statement = select(EvidenceItem).where(EvidenceItem.response_id == coerce_uuid(response_id))
        return self.session.scalars(statement).first()

    def create_from_response(
        self,
        *,
        assessment_id: UUID,
        question_id: UUID,
        response_id: UUID,
        related_capability: str,
        evidence_value: Any,
    ) -> EvidenceItem:
        existing = self.get_for_response(response_id)
        if existing is not None:
            existing.related_capability = related_capability
            existing.evidence_value = evidence_value
            self.session.flush()
            return existing

        evidence = EvidenceItem(
            assessment_id=coerce_uuid(assessment_id),
            response_id=coerce_uuid(response_id),
            evidence_source=EvidenceSource.SELF_REPORT,
            related_capability=related_capability,
            source_reference=f"pbhs_response:{question_id}",
            evidence_value=evidence_value,
            confidence=1.0,
        )
        return self.add(evidence)


class SqlAlchemyCapabilityScoreRepository(CapabilityScoreRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, capability_score: CapabilityScore) -> CapabilityScore:
        self.session.add(capability_score)
        self.session.flush()
        return capability_score

    def list_for_assessment(self, assessment_id: UUID) -> list[CapabilityScore]:
        statement = (
            select(CapabilityScore)
            .where(CapabilityScore.assessment_id == coerce_uuid(assessment_id))
            .order_by(CapabilityScore.capability)
        )
        return list(self.session.scalars(statement))

    def get_for_capability(
        self,
        assessment_id: UUID,
        capability: str,
    ) -> CapabilityScore | None:
        statement = select(CapabilityScore).where(
            CapabilityScore.assessment_id == coerce_uuid(assessment_id),
            CapabilityScore.capability == capability,
        )
        return self.session.scalars(statement).first()
