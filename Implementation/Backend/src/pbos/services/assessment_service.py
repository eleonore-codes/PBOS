from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from pbos.domain.enums import AssessmentStatus
from pbos.infrastructure.database.models import (
    PBHSAssessment,
    PBHSAssessmentQuestion,
    PBHSResponse,
)
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyAssessmentRepository,
    SqlAlchemyBusinessRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyQuestionRepository,
)


@dataclass(frozen=True)
class AssessmentProgress:
    assessment_id: str
    status: AssessmentStatus
    total_required_questions: int
    answered_required_questions: int
    percent_complete: float
    missing_question_ids: list[str]
    missing_capabilities: list[str]
    locked: bool


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
        for order_index, question in enumerate(self.questions.list_active(), start=1):
            self.assessments.add_assessment_question(
                PBHSAssessmentQuestion(
                    assessment_id=assessment.assessment_id,
                    question_id=question.question_id,
                    question_version=question.version,
                    capability=question.capability,
                    construct=question.construct,
                    question_text=question.question_text,
                    response_scale=question.response_scale,
                    required=True,
                    order_index=order_index,
                    source_status=question.status.value,
                )
            )
        self.session.commit()
        self.session.refresh(assessment)
        return assessment

    def get_assessment(self, assessment_id: UUID) -> PBHSAssessment:
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")
        return assessment

    def list_assessment_questions(self, assessment_id: UUID) -> list[PBHSAssessmentQuestion]:
        self.get_assessment(assessment_id)
        return self.assessments.list_assessment_questions(assessment_id)

    def list_responses(self, assessment_id: UUID) -> list[PBHSResponse]:
        self.get_assessment(assessment_id)
        return self.assessments.list_responses(assessment_id)

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
        if assessment.status != AssessmentStatus.DRAFT:
            raise ValueError("assessment_locked")

        assessment_question = self.assessments.get_assessment_question(assessment_id, question_id)
        if assessment_question is None:
            raise ValueError("question_not_in_assessment")

        self._validate_response_value(assessment_question.response_scale, response_value)

        response = self.assessments.get_response(assessment_id, question_id)
        if response is None:
            response = PBHSResponse(
                assessment_id=str(assessment_id),
                question_id=str(question_id),
                question_version=assessment_question.question_version,
                response_value=response_value,
            )
            self.assessments.add_response(response)
        else:
            response.question_version = assessment_question.question_version
            response.response_value = response_value
            response.submitted_at = datetime.now(UTC)
            self.session.flush()

        evidence = self.evidence.create_from_response(
            assessment_id=assessment_id,
            question_id=question_id,
            response_id=UUID(response.response_id),
            related_capability=assessment_question.capability,
            evidence_value=response_value,
        )
        self.session.commit()
        self.session.refresh(response)
        self.session.refresh(evidence)
        return response, evidence

    def get_progress(self, assessment_id: UUID) -> AssessmentProgress:
        assessment = self.get_assessment(assessment_id)
        required_questions = [
            question
            for question in self.assessments.list_assessment_questions(assessment_id)
            if question.required
        ]
        responses = self.assessments.list_responses(assessment_id)
        answered_question_ids = {response.question_id for response in responses}
        missing_questions = [
            question
            for question in required_questions
            if question.question_id not in answered_question_ids
        ]
        total_required = len(required_questions)
        answered_required = total_required - len(missing_questions)
        percent_complete = (
            round((answered_required / total_required) * 100, 2) if total_required else 0.0
        )

        return AssessmentProgress(
            assessment_id=assessment.assessment_id,
            status=assessment.status,
            total_required_questions=total_required,
            answered_required_questions=answered_required,
            percent_complete=percent_complete,
            missing_question_ids=[question.question_id for question in missing_questions],
            missing_capabilities=sorted({question.capability for question in missing_questions}),
            locked=assessment.status != AssessmentStatus.DRAFT,
        )

    def submit_assessment(self, assessment_id: UUID) -> PBHSAssessment:
        assessment = self.get_assessment(assessment_id)
        if assessment.status != AssessmentStatus.DRAFT:
            raise ValueError("invalid_status_transition")

        progress = self.get_progress(assessment_id)
        if progress.total_required_questions == 0:
            raise ValueError("assessment_has_no_required_questions")
        if progress.answered_required_questions != progress.total_required_questions:
            raise ValueError("assessment_incomplete")

        assessment.status = AssessmentStatus.SUBMITTED
        assessment.completed_at = datetime.now(UTC)
        self.session.commit()
        self.session.refresh(assessment)
        return assessment

    def _validate_response_value(self, response_scale: str, response_value: Any) -> None:
        if response_scale == "likert_1_5":
            if (
                not isinstance(response_value, int)
                or isinstance(response_value, bool)
                or not 1 <= response_value <= 5
            ):
                raise ValueError("response_value_must_be_integer_1_to_5")
            return

        if response_scale == "likert_1_7":
            if (
                not isinstance(response_value, int)
                or isinstance(response_value, bool)
                or not 1 <= response_value <= 7
            ):
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
