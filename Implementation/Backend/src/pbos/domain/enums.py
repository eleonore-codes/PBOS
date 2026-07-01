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


class RecommendationStatus(StrEnum):
    CANDIDATE = "candidate"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    SUPERSEDED = "superseded"


class RecommendationExecutionPath(StrEnum):
    DIY = "DIY"
    DWY = "DWY"
    DFY = "DFY"


class RecommendationCategory(StrEnum):
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    ASSET = "asset"
    AI_LEVERAGE = "ai_leverage"
    COMMERCIAL = "commercial"
    LIFE_RETURN = "life_return"


class RecommendationType(StrEnum):
    SPONSOR_READINESS = "SPONSOR_READINESS"
    CONTENT_SYSTEM = "CONTENT_SYSTEM"
    EMAIL_FUNNEL = "EMAIL_FUNNEL"
    AUTOMATION = "AUTOMATION"
    KNOWLEDGE_LIBRARY = "KNOWLEDGE_LIBRARY"
