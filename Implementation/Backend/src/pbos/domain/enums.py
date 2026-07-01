from enum import StrEnum


class AssessmentStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    SCORED = "scored"
    RECOMMENDATIONS_GENERATED = "recommendations_generated"
    REVIEWED = "reviewed"
    REPORTED = "reported"


class QuestionStatus(StrEnum):
    ACTIVE = "active"
    EXPERIMENTAL = "experimental"
    RETIRED = "retired"


class EvidenceSource(StrEnum):
    SELF_REPORT = "self_report"
    BEHAVIORAL = "behavioral"
    BUSINESS = "business"
    PORTFOLIO = "portfolio"
    AI_INTERVIEW = "ai_interview"
    LONGITUDINAL = "longitudinal"
