from dataclasses import dataclass
from datetime import UTC, datetime
from statistics import mean
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from pbos.domain.enums import AssessmentStatus, EvidenceSource
from pbos.infrastructure.database.models import (
    CapabilityScore,
    EvidenceItem,
    PBHSAssessment,
    PBHSAssessmentQuestion,
    PBHSResponse,
)
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyAssessmentRepository,
    SqlAlchemyCapabilityScoreRepository,
    SqlAlchemyEvidenceRepository,
)

SCORING_METHOD = "pbhs_questionnaire_v1"
QUESTIONNAIRE_ONLY_SOURCE_BREADTH_FACTOR = 0.4


@dataclass(frozen=True)
class CapabilityScoreSummary:
    capability_score_id: str
    assessment_id: str
    capability: str
    score: float
    maturity_level: int
    confidence: float
    calculation_method: str
    evidence_ids: list[str]
    scored_at: datetime


@dataclass(frozen=True)
class AssessmentScoreSummary:
    assessment_id: str
    status: AssessmentStatus
    overall_score: float
    overall_confidence: float
    calculation_method: str
    scored_at: datetime
    capability_scores: list[CapabilityScoreSummary]


@dataclass(frozen=True)
class ScoreInput:
    question: PBHSAssessmentQuestion
    response: PBHSResponse
    evidence: EvidenceItem
    normalized_score: float


class ScoringService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.assessments = SqlAlchemyAssessmentRepository(session)
        self.evidence = SqlAlchemyEvidenceRepository(session)
        self.capability_scores = SqlAlchemyCapabilityScoreRepository(session)

    def score_assessment(self, assessment_id: UUID) -> AssessmentScoreSummary:
        assessment = self._get_scoreable_assessment(assessment_id)
        score_inputs = self._collect_score_inputs(assessment_id)
        capability_names = self._capability_names(assessment_id)
        scored_at = datetime.now(UTC)
        saved_scores: list[CapabilityScore] = []

        for capability in capability_names:
            capability_inputs = [
                score_input
                for score_input in score_inputs
                if score_input.question.capability == capability
            ]
            if not capability_inputs:
                raise ValueError("capability_has_no_scoreable_responses")

            raw_score = mean(score_input.normalized_score for score_input in capability_inputs)
            evidence_ids = [score_input.evidence.evidence_id for score_input in capability_inputs]
            confidence = self._calculate_confidence(capability_inputs, assessment_id, capability)
            saved_scores.append(
                self._upsert_capability_score(
                    assessment_id=assessment_id,
                    capability=capability,
                    score=round(raw_score, 2),
                    maturity_level=maturity_level(raw_score),
                    confidence=confidence,
                    evidence_ids=evidence_ids,
                    scored_at=scored_at,
                )
            )

        assessment.overall_score = round(mean(score.score for score in saved_scores), 2)
        assessment.overall_confidence = round(mean(score.confidence for score in saved_scores), 2)
        assessment.scoring_method = SCORING_METHOD
        assessment.scored_at = scored_at
        assessment.status = AssessmentStatus.SCORED
        self.session.commit()

        return self.get_scores(assessment_id)

    def get_scores(self, assessment_id: UUID) -> AssessmentScoreSummary:
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")

        scores = self.capability_scores.list_for_assessment(assessment_id)
        if not scores or assessment.overall_score is None or assessment.overall_confidence is None:
            raise ValueError("assessment_not_scored")

        capability_order = {
            capability: order for order, capability in enumerate(self._capability_names(assessment_id))
        }
        scores.sort(key=lambda score: capability_order.get(score.capability, len(capability_order)))
        return self._to_summary(assessment, scores)

    def _get_scoreable_assessment(self, assessment_id: UUID) -> PBHSAssessment:
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")
        if assessment.status not in {AssessmentStatus.SUBMITTED, AssessmentStatus.SCORED}:
            raise ValueError("assessment_not_submitted")
        return assessment

    def _collect_score_inputs(self, assessment_id: UUID) -> list[ScoreInput]:
        questions = self.assessments.list_assessment_questions(assessment_id)
        responses = {
            response.question_id: response
            for response in self.assessments.list_responses(assessment_id)
        }
        evidence_items = self.evidence.list_for_assessment(assessment_id)
        evidence_by_response_id = {
            evidence.response_id: evidence
            for evidence in evidence_items
            if evidence.response_id is not None
        }
        score_inputs: list[ScoreInput] = []

        for question in questions:
            response = responses.get(question.question_id)
            if response is None:
                if question.required:
                    raise ValueError("assessment_incomplete")
                continue

            evidence = evidence_by_response_id.get(response.response_id)
            if evidence is None:
                raise ValueError("missing_required_evidence")

            score_inputs.append(
                ScoreInput(
                    question=question,
                    response=response,
                    evidence=evidence,
                    normalized_score=normalize_response(
                        question.response_scale,
                        response.response_value,
                    ),
                )
            )

        if not score_inputs:
            raise ValueError("assessment_incomplete")
        return score_inputs

    def _capability_names(self, assessment_id: UUID) -> list[str]:
        names: list[str] = []
        for question in self.assessments.list_assessment_questions(assessment_id):
            if question.capability not in names:
                names.append(question.capability)
        return names

    def _calculate_confidence(
        self,
        capability_inputs: list[ScoreInput],
        assessment_id: UUID,
        capability: str,
    ) -> float:
        required_questions = [
            question
            for question in self.assessments.list_assessment_questions(assessment_id)
            if question.capability == capability and question.required
        ]
        coverage_factor = (
            len(capability_inputs) / len(required_questions) if required_questions else 0.0
        )
        evidence_quality_factor = mean(
            score_input.evidence.confidence for score_input in capability_inputs
        )
        source_breadth_factor = self._source_breadth_factor(
            {score_input.evidence.evidence_source for score_input in capability_inputs}
        )
        return round(coverage_factor * evidence_quality_factor * source_breadth_factor, 2)

    def _source_breadth_factor(self, sources: set[EvidenceSource]) -> float:
        if sources == {EvidenceSource.SELF_REPORT}:
            return QUESTIONNAIRE_ONLY_SOURCE_BREADTH_FACTOR
        return min(1.0, QUESTIONNAIRE_ONLY_SOURCE_BREADTH_FACTOR + (0.2 * (len(sources) - 1)))

    def _upsert_capability_score(
        self,
        *,
        assessment_id: UUID,
        capability: str,
        score: float,
        maturity_level: int,
        confidence: float,
        evidence_ids: list[str],
        scored_at: datetime,
    ) -> CapabilityScore:
        capability_score = self.capability_scores.get_for_capability(assessment_id, capability)
        if capability_score is None:
            return self.capability_scores.add(
                CapabilityScore(
                    assessment_id=str(assessment_id),
                    capability=capability,
                    score=score,
                    maturity_level=maturity_level,
                    confidence=confidence,
                    calculation_method=SCORING_METHOD,
                    evidence_ids=evidence_ids,
                    scored_at=scored_at,
                )
            )

        capability_score.score = score
        capability_score.maturity_level = maturity_level
        capability_score.confidence = confidence
        capability_score.calculation_method = SCORING_METHOD
        capability_score.evidence_ids = evidence_ids
        capability_score.scored_at = scored_at
        self.session.flush()
        return capability_score

    def _to_summary(
        self,
        assessment: PBHSAssessment,
        scores: list[CapabilityScore],
    ) -> AssessmentScoreSummary:
        return AssessmentScoreSummary(
            assessment_id=assessment.assessment_id,
            status=assessment.status,
            overall_score=assessment.overall_score,
            overall_confidence=assessment.overall_confidence,
            calculation_method=assessment.scoring_method or SCORING_METHOD,
            scored_at=assessment.scored_at or datetime.now(UTC),
            capability_scores=[
                CapabilityScoreSummary(
                    capability_score_id=score.capability_score_id,
                    assessment_id=score.assessment_id,
                    capability=score.capability,
                    score=score.score,
                    maturity_level=score.maturity_level,
                    confidence=score.confidence,
                    calculation_method=score.calculation_method,
                    evidence_ids=list(score.evidence_ids),
                    scored_at=score.scored_at,
                )
                for score in scores
            ],
        )


def normalize_response(response_scale: str, response_value: Any) -> float:
    if response_scale != "likert_1_5":
        raise ValueError("unsupported_response_scale")
    if not isinstance(response_value, int) or isinstance(response_value, bool):
        raise ValueError("response_value_must_be_integer_1_to_5")
    if not 1 <= response_value <= 5:
        raise ValueError("response_value_must_be_integer_1_to_5")
    return ((response_value - 1) / 4) * 100


def maturity_level(score: float) -> int:
    if score <= 20:
        return 1
    if score <= 40:
        return 2
    if score <= 60:
        return 3
    if score <= 80:
        return 4
    return 5
