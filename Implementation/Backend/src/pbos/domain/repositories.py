from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
from uuid import UUID

if TYPE_CHECKING:
    from pbos.infrastructure.database.models import (
        Business,
        CapabilityScore,
        EvidenceItem,
        PBHSAssessment,
        PBHSQuestion,
        PBHSResponse,
    )


class BusinessRepository(ABC):
    @abstractmethod
    def add(self, business: Business) -> Business:
        raise NotImplementedError

    @abstractmethod
    def get(self, business_id: UUID) -> Business | None:
        raise NotImplementedError


class AssessmentRepository(ABC):
    @abstractmethod
    def add(self, assessment: PBHSAssessment) -> PBHSAssessment:
        raise NotImplementedError

    @abstractmethod
    def get(self, assessment_id: UUID) -> PBHSAssessment | None:
        raise NotImplementedError

    @abstractmethod
    def add_response(self, response: PBHSResponse) -> PBHSResponse:
        raise NotImplementedError


class QuestionRepository(ABC):
    @abstractmethod
    def add(self, question: PBHSQuestion) -> PBHSQuestion:
        raise NotImplementedError

    @abstractmethod
    def get(self, question_id: UUID) -> PBHSQuestion | None:
        raise NotImplementedError

    @abstractmethod
    def list_active(self) -> list[PBHSQuestion]:
        raise NotImplementedError


class EvidenceRepository(ABC):
    @abstractmethod
    def add(self, evidence: EvidenceItem) -> EvidenceItem:
        raise NotImplementedError

    @abstractmethod
    def list_for_assessment(self, assessment_id: UUID) -> list[EvidenceItem]:
        raise NotImplementedError

    @abstractmethod
    def create_from_response(
        self,
        *,
        assessment_id: UUID,
        question_id: UUID,
        response_id: UUID,
        related_capability: str,
        evidence_value: Any,
    ) -> EvidenceItem:
        raise NotImplementedError


class CapabilityScoreRepository(ABC):
    @abstractmethod
    def add(self, capability_score: CapabilityScore) -> CapabilityScore:
        raise NotImplementedError

    @abstractmethod
    def list_for_assessment(self, assessment_id: UUID) -> list[CapabilityScore]:
        raise NotImplementedError

    @abstractmethod
    def get_for_capability(
        self,
        assessment_id: UUID,
        capability: str,
    ) -> CapabilityScore | None:
        raise NotImplementedError
