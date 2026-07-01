from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from pbos.domain.enums import AssessmentStatus, QuestionStatus
from pbos.infrastructure.database.models import PBHSAssessment, PBHSResponse
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyAssessmentRepository,
    SqlAlchemyBusinessRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyQuestionRepository,
)


class AssessmentService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.assessments = SqlAlchemyAssessmentRepository(session)
        self.businesses = SqlAlchemyBusinessRepository(session)
        self.questions = SqlAlchemyQuestionRepository(session)
        self.evidence = SqlAlchemyEvidenceRepository(session)

    def start_assessment(self, *, business_id: UUID, pbhs_version: str) -> PBHSAssessment:
        business = self.businesses.get(business_id)
        if business is None:
            raise ValueError("business_not_found")

        assessment = PBHSAssessment(
            business_id=str(business_id),
            pbhs_version=pbhs_version,
            status=AssessmentStatus.DRAFT,
        )
        self.assessments.add(assessment)
        self.session.commit()
        self.session.refresh(assessment)
        return assessment

    def submit_response(
        self,
        *,
        assessment_id: UUID,
        question_id: UUID,
        response_value: Any,
    ) -> tuple[PBHSResponse, Any]:
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")

        question = self.questions.get(question_id)
        if question is None:
            raise ValueError("question_not_found")
        if question.status == QuestionStatus.RETIRED:
            raise ValueError("question_retired")

        self._validate_response_value(question.response_scale, response_value)

        response = PBHSResponse(
            assessment_id=str(assessment_id),
            question_id=str(question_id),
            question_version=question.version,
            response_value=response_value,
        )
        self.assessments.add_response(response)
        evidence = self.evidence.create_from_response(
            assessment_id=assessment_id,
            question_id=question_id,
            response_id=UUID(response.response_id),
            related_capability=question.capability,
            evidence_value=response_value,
        )
        self.session.commit()
        self.session.refresh(response)
        self.session.refresh(evidence)
        return response, evidence

    def _validate_response_value(self, response_scale: str, response_value: Any) -> None:
        if response_scale == "likert_1_5":
            if not isinstance(response_value, int) or not 1 <= response_value <= 5:
                raise ValueError("response_value_must_be_integer_1_to_5")
            return

        if response_scale == "likert_1_7":
            if not isinstance(response_value, int) or not 1 <= response_value <= 7:
                raise ValueError("response_value_must_be_integer_1_to_7")
            return

        if response_scale == "yes_no":
            if not isinstance(response_value, bool):
                raise ValueError("response_value_must_be_boolean")
            return

        if response_scale == "text":
            if not isinstance(response_value, str) or not response_value.strip():
                raise ValueError("response_value_must_be_non_empty_text")
            return

        raise ValueError("unsupported_response_scale")
