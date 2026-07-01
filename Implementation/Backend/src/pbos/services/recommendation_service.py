from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from pbos.domain.enums import (
    AssessmentStatus,
    RecommendationCategory,
    RecommendationExecutionPath,
    RecommendationStatus,
    RecommendationType,
)
from pbos.infrastructure.database.models import CapabilityScore, Recommendation
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyAssessmentRepository,
    SqlAlchemyCapabilityScoreRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyRecommendationRepository,
)

RECOMMENDATION_ENGINE_VERSION = "m17_recommendation_engine_v1"
RECOMMENDATION_RULE_SET_VERSION = "m17_rules_v1"


@dataclass(frozen=True)
class RecommendationTemplate:
    template_id: str
    version: str
    recommendation_type: RecommendationType
    category: RecommendationCategory
    title: str
    description: str
    business_return_dimensions: list[str]
    life_return_dimensions: list[str]
    human_signature_effect: str
    default_execution_path: RecommendationExecutionPath
    success_criteria: list[str]


@dataclass(frozen=True)
class RecommendationRule:
    rule_id: str
    version: str
    template_id: str
    triggered_capabilities: list[str]
    trigger_description: str
    min_scores: dict[str, float]
    max_scores: dict[str, float]
    bottleneck_capabilities: list[str]
    business_return_base: float
    life_return_base: float
    human_time_hours: tuple[float, float]
    human_time_saved_hours: tuple[float, float]
    complexity: float
    financial_cost: float
    strategic_uncertainty: float
    human_signature_risk: float
    asset_creation_value: float
    human_signature_leverage: float


@dataclass(frozen=True)
class RecommendationGenerationRun:
    run_id: str
    assessment_id: str
    engine_version: str
    rule_set_version: str
    started_at: datetime
    completed_at: datetime | None
    status: str
    error_summary: str | None


@dataclass(frozen=True)
class RecommendationPortfolioSummary:
    assessment_id: str
    status: AssessmentStatus
    engine_version: str
    rule_set_version: str
    generated_at: datetime
    recommendations: list[Recommendation]
    generation_run: RecommendationGenerationRun


TEMPLATES: dict[str, RecommendationTemplate] = {
    "sponsor_readiness_v1": RecommendationTemplate(
        template_id="sponsor_readiness_v1",
        version="1.0",
        recommendation_type=RecommendationType.SPONSOR_READINESS,
        category=RecommendationCategory.COMMERCIAL,
        title="Build sponsor readiness assets",
        description=(
            "Package the existing podcast authority into sponsor-facing assets so sponsor "
            "interest can convert into qualified commercial conversations."
        ),
        business_return_dimensions=["financial", "market", "asset", "strategic"],
        life_return_dimensions=["security", "autonomy"],
        human_signature_effect="strengthens",
        default_execution_path=RecommendationExecutionPath.DWY,
        success_criteria=[
            "Sponsor media kit created",
            "Sponsor outreach criteria documented",
            "Qualified sponsor conversation tracked",
        ],
    ),
    "content_system_v1": RecommendationTemplate(
        template_id="content_system_v1",
        version="1.0",
        recommendation_type=RecommendationType.CONTENT_SYSTEM,
        category=RecommendationCategory.OPERATIONAL,
        title="Create a repeatable content operating system",
        description=(
            "Turn podcast production and publishing into a documented system that reduces "
            "founder dependency and protects creative time."
        ),
        business_return_dimensions=["operational", "asset", "strategic"],
        life_return_dimensions=["time", "wellbeing", "autonomy"],
        human_signature_effect="protects",
        default_execution_path=RecommendationExecutionPath.DFY,
        success_criteria=[
            "Publishing workflow documented",
            "Reusable checklist created",
            "Owner operational hours reduced",
        ],
    ),
    "email_funnel_v1": RecommendationTemplate(
        template_id="email_funnel_v1",
        version="1.0",
        recommendation_type=RecommendationType.EMAIL_FUNNEL,
        category=RecommendationCategory.COMMERCIAL,
        title="Build an email conversion funnel",
        description=(
            "Create a simple email path that converts audience trust and content attention "
            "into qualified business opportunities."
        ),
        business_return_dimensions=["financial", "market", "strategic"],
        life_return_dimensions=["security", "autonomy"],
        human_signature_effect="strengthens",
        default_execution_path=RecommendationExecutionPath.DWY,
        success_criteria=[
            "Lead capture point published",
            "Email sequence drafted",
            "Conversion metric defined",
        ],
    ),
    "automation_v1": RecommendationTemplate(
        template_id="automation_v1",
        version="1.0",
        recommendation_type=RecommendationType.AUTOMATION,
        category=RecommendationCategory.AI_LEVERAGE,
        title="Automate repetitive operating work",
        description=(
            "Use AI and automation to remove repeatable administrative work while preserving "
            "the owner's judgment and authentic voice."
        ),
        business_return_dimensions=["operational", "strategic"],
        life_return_dimensions=["time", "wellbeing", "recovery"],
        human_signature_effect="protects",
        default_execution_path=RecommendationExecutionPath.DFY,
        success_criteria=[
            "Automation candidate selected",
            "Quality-control checkpoint defined",
            "Recurring owner hours saved",
        ],
    ),
    "knowledge_library_v1": RecommendationTemplate(
        template_id="knowledge_library_v1",
        version="1.0",
        recommendation_type=RecommendationType.KNOWLEDGE_LIBRARY,
        category=RecommendationCategory.ASSET,
        title="Build a reusable knowledge library",
        description=(
            "Transform the owner's expertise and podcast material into reusable knowledge "
            "assets that compound authority and reduce repeated explanation work."
        ),
        business_return_dimensions=["asset", "market", "strategic"],
        life_return_dimensions=["time", "growth"],
        human_signature_effect="strengthens",
        default_execution_path=RecommendationExecutionPath.DWY,
        success_criteria=[
            "Core expertise themes catalogued",
            "Reusable knowledge asset structure created",
            "At least one asset reused in sales or delivery",
        ],
    ),
}


RULES: tuple[RecommendationRule, ...] = (
    RecommendationRule(
        rule_id="rule_sponsor_readiness_v1",
        version="1.0",
        template_id="sponsor_readiness_v1",
        triggered_capabilities=["Podcast Assets", "Trust", "Business Return"],
        trigger_description=(
            "Podcast assets or trust are available, but Business Return is constrained."
        ),
        min_scores={"Podcast Assets": 60},
        max_scores={"Business Return": 60},
        bottleneck_capabilities=["Business Return", "Trust"],
        business_return_base=82,
        life_return_base=48,
        human_time_hours=(4, 8),
        human_time_saved_hours=(0, 2),
        complexity=0.45,
        financial_cost=0.25,
        strategic_uncertainty=0.35,
        human_signature_risk=0.2,
        asset_creation_value=82,
        human_signature_leverage=70,
    ),
    RecommendationRule(
        rule_id="rule_content_system_v1",
        version="1.0",
        template_id="content_system_v1",
        triggered_capabilities=["Podcast Assets", "Business Systems", "Life Return"],
        trigger_description=(
            "Podcast activity exists, but weak systems or Life Return indicate founder drag."
        ),
        min_scores={"Podcast Assets": 50},
        max_scores={"Business Systems": 55, "Life Return": 65},
        bottleneck_capabilities=["Business Systems", "Life Return"],
        business_return_base=68,
        life_return_base=78,
        human_time_hours=(5, 10),
        human_time_saved_hours=(3, 6),
        complexity=0.4,
        financial_cost=0.15,
        strategic_uncertainty=0.2,
        human_signature_risk=0.15,
        asset_creation_value=72,
        human_signature_leverage=64,
    ),
    RecommendationRule(
        rule_id="rule_email_funnel_v1",
        version="1.0",
        template_id="email_funnel_v1",
        triggered_capabilities=["Trust", "Knowledge Assets", "Business Return"],
        trigger_description=(
            "Trust or knowledge value exists, but revenue capability is not converting fully."
        ),
        min_scores={"Trust": 50, "Knowledge Assets": 50},
        max_scores={"Business Return": 65},
        bottleneck_capabilities=["Business Return"],
        business_return_base=76,
        life_return_base=52,
        human_time_hours=(6, 12),
        human_time_saved_hours=(1, 3),
        complexity=0.5,
        financial_cost=0.2,
        strategic_uncertainty=0.35,
        human_signature_risk=0.25,
        asset_creation_value=66,
        human_signature_leverage=68,
    ),
    RecommendationRule(
        rule_id="rule_automation_v1",
        version="1.0",
        template_id="automation_v1",
        triggered_capabilities=["AI Leverage", "Business Systems", "Life Return"],
        trigger_description=(
            "AI Leverage is low while systems or Life Return indicate repetitive work."
        ),
        min_scores={},
        max_scores={"AI Leverage": 55, "Business Systems": 65, "Life Return": 70},
        bottleneck_capabilities=["AI Leverage", "Business Systems", "Life Return"],
        business_return_base=62,
        life_return_base=82,
        human_time_hours=(3, 8),
        human_time_saved_hours=(4, 8),
        complexity=0.42,
        financial_cost=0.2,
        strategic_uncertainty=0.25,
        human_signature_risk=0.3,
        asset_creation_value=58,
        human_signature_leverage=74,
    ),
    RecommendationRule(
        rule_id="rule_knowledge_library_v1",
        version="1.0",
        template_id="knowledge_library_v1",
        triggered_capabilities=["Human Signature", "Knowledge Assets", "Podcast Assets"],
        trigger_description=(
            "Human Signature or podcast material is present, but reusable Knowledge Assets lag."
        ),
        min_scores={"Human Signature": 60},
        max_scores={"Knowledge Assets": 60},
        bottleneck_capabilities=["Knowledge Assets"],
        business_return_base=72,
        life_return_base=58,
        human_time_hours=(6, 12),
        human_time_saved_hours=(2, 5),
        complexity=0.38,
        financial_cost=0.1,
        strategic_uncertainty=0.2,
        human_signature_risk=0.1,
        asset_creation_value=88,
        human_signature_leverage=86,
    ),
)


class RecommendationService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.assessments = SqlAlchemyAssessmentRepository(session)
        self.capability_scores = SqlAlchemyCapabilityScoreRepository(session)
        self.evidence = SqlAlchemyEvidenceRepository(session)
        self.recommendations = SqlAlchemyRecommendationRepository(session)

    def generate_recommendations(self, assessment_id: UUID) -> RecommendationPortfolioSummary:
        run = RecommendationGenerationRun(
            run_id=f"run:{assessment_id}:{RECOMMENDATION_ENGINE_VERSION}",
            assessment_id=str(assessment_id),
            engine_version=RECOMMENDATION_ENGINE_VERSION,
            rule_set_version=RECOMMENDATION_RULE_SET_VERSION,
            started_at=datetime.now(UTC),
            completed_at=None,
            status="running",
            error_summary=None,
        )
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")
        if assessment.status not in {
            AssessmentStatus.SCORED,
            AssessmentStatus.RECOMMENDATIONS_GENERATED,
        }:
            raise ValueError("assessment_not_scored")

        scores = self.capability_scores.list_for_assessment(assessment_id)
        if not scores:
            raise ValueError("assessment_not_scored")

        generated_at = datetime.now(UTC)
        score_by_capability = {score.capability: score for score in scores}
        generated: list[Recommendation] = []

        for rule in RULES:
            if not self._rule_matches(rule, score_by_capability):
                continue
            template = TEMPLATES[rule.template_id]
            generated.append(
                self._upsert_recommendation(
                    assessment_id=assessment_id,
                    rule=rule,
                    template=template,
                    score_by_capability=score_by_capability,
                    generated_at=generated_at,
                )
            )

        if not generated:
            raise ValueError("no_matching_recommendations")

        generated_types = {recommendation.recommendation_type for recommendation in generated}
        for existing in self.recommendations.list_for_assessment(assessment_id):
            if existing.recommendation_type not in generated_types:
                existing.status = RecommendationStatus.SUPERSEDED

        assessment.status = AssessmentStatus.RECOMMENDATIONS_GENERATED
        self.session.commit()
        persisted = self.list_recommendations(assessment_id)
        completed_run = RecommendationGenerationRun(
            run_id=run.run_id,
            assessment_id=run.assessment_id,
            engine_version=run.engine_version,
            rule_set_version=run.rule_set_version,
            started_at=run.started_at,
            completed_at=datetime.now(UTC),
            status="completed",
            error_summary=None,
        )
        return RecommendationPortfolioSummary(
            assessment_id=str(assessment_id),
            status=AssessmentStatus.RECOMMENDATIONS_GENERATED,
            engine_version=RECOMMENDATION_ENGINE_VERSION,
            rule_set_version=RECOMMENDATION_RULE_SET_VERSION,
            generated_at=generated_at,
            recommendations=persisted,
            generation_run=completed_run,
        )

    def list_recommendations(self, assessment_id: UUID) -> list[Recommendation]:
        assessment = self.assessments.get(assessment_id)
        if assessment is None:
            raise ValueError("assessment_not_found")
        return self.recommendations.list_for_assessment(assessment_id)

    def get_recommendation(self, recommendation_id: UUID) -> Recommendation:
        recommendation = self.recommendations.get(recommendation_id)
        if recommendation is None:
            raise ValueError("recommendation_not_found")
        return recommendation

    def _rule_matches(
        self,
        rule: RecommendationRule,
        score_by_capability: dict[str, CapabilityScore],
    ) -> bool:
        required_capabilities = set(rule.triggered_capabilities)
        if not required_capabilities.issubset(score_by_capability):
            return False
        for capability, minimum in rule.min_scores.items():
            if score_by_capability[capability].score < minimum:
                return False
        return any(
            score_by_capability[capability].score <= maximum
            for capability, maximum in rule.max_scores.items()
            if capability in score_by_capability
        )

    def _upsert_recommendation(
        self,
        *,
        assessment_id: UUID,
        rule: RecommendationRule,
        template: RecommendationTemplate,
        score_by_capability: dict[str, CapabilityScore],
        generated_at: datetime,
    ) -> Recommendation:
        triggered_scores = [score_by_capability[name] for name in rule.triggered_capabilities]
        capability_score_ids = [score.capability_score_id for score in triggered_scores]
        supporting_evidence_ids = sorted(
            {
                evidence_id
                for score in triggered_scores
                for evidence_id in score.evidence_ids
            }
        )
        weakest_score = min(triggered_scores, key=lambda score: score.score)
        average_confidence = sum(score.confidence for score in triggered_scores) / len(
            triggered_scores
        )
        bottleneck_relevance = self._bottleneck_relevance(rule, score_by_capability)
        business_return = self._business_return(rule, template, bottleneck_relevance)
        life_return = self._life_return(rule, template)
        human_time = self._human_time(rule)
        confidence = self._confidence(rule, average_confidence, supporting_evidence_ids)
        risk = self._risk(rule, confidence)
        priority_score = self._priority_score(
            business_return["score"],
            life_return["score"],
            bottleneck_relevance,
            rule.human_signature_leverage,
            rule.asset_creation_value,
            confidence,
            risk["score"],
            human_time["estimated_hours_required"]["max"],
        )
        priority = priority_level(priority_score)
        priority_rationale = (
            f"Priority is {priority} because {template.recommendation_type.value} addresses "
            f"{weakest_score.capability}, the weakest triggered capability, with expected "
            f"Business Return {business_return['score']} and Life Return {life_return['score']}."
        )
        rationale = {
            "why_generated": rule.trigger_description,
            "weakest_triggered_capability": weakest_score.capability,
            "triggered_capability_scores": [
                {"capability": score.capability, "score": score.score}
                for score in triggered_scores
            ],
            "evidence_summary": (
                f"{len(supporting_evidence_ids)} evidence items support the triggered "
                "capability scores."
            ),
            "priority_reason": priority_rationale,
        }
        calculation_trace = {
            "engine_version": RECOMMENDATION_ENGINE_VERSION,
            "rule_set_version": RECOMMENDATION_RULE_SET_VERSION,
            "rule": {
                "rule_id": rule.rule_id,
                "version": rule.version,
                "min_scores": rule.min_scores,
                "max_scores": rule.max_scores,
            },
            "template": {
                "template_id": template.template_id,
                "version": template.version,
                "recommendation_type": template.recommendation_type.value,
            },
            "inputs": {
                "triggered_capabilities": rule.triggered_capabilities,
                "capability_score_ids": capability_score_ids,
                "supporting_evidence_ids": supporting_evidence_ids,
            },
            "scores": {
                "business_return": business_return["score"],
                "life_return": life_return["score"],
                "confidence": confidence,
                "risk": risk["score"],
                "priority": priority_score,
            },
        }
        values = {
            "rule_id": rule.rule_id,
            "rule_version": rule.version,
            "template_id": template.template_id,
            "template_version": template.version,
            "recommendation_type": template.recommendation_type,
            "category": template.category,
            "title": template.title,
            "description": template.description,
            "priority": priority,
            "priority_score": priority_score,
            "priority_rationale": priority_rationale,
            "confidence": confidence,
            "confidence_label": confidence_label(confidence),
            "risk_score": risk["score"],
            "risk_label": risk["level"],
            "expected_business_return": business_return,
            "expected_life_return": life_return,
            "human_time_required": human_time,
            "human_signature_impact": {
                "effect": template.human_signature_effect,
                "score": rule.human_signature_leverage,
                "rationale": (
                    "The recommendation uses AI, assets, or systems to amplify the owner's "
                    "distinct expertise instead of replacing it."
                ),
            },
            "triggered_capabilities": list(rule.triggered_capabilities),
            "capability_score_ids": capability_score_ids,
            "supporting_evidence_ids": supporting_evidence_ids,
            "rationale": rationale,
            "calculation_trace": calculation_trace,
            "recommended_execution_path": template.default_execution_path,
            "success_criteria": list(template.success_criteria),
            "status": RecommendationStatus.CANDIDATE,
            "generated_at": generated_at,
        }

        existing = self.recommendations.get_for_type(assessment_id, template.recommendation_type)
        if existing is None:
            return self.recommendations.add(
                Recommendation(assessment_id=str(assessment_id), **values)
            )

        for key, value in values.items():
            setattr(existing, key, value)
        self.session.flush()
        return existing

    def _business_return(
        self,
        rule: RecommendationRule,
        template: RecommendationTemplate,
        bottleneck_relevance: float,
    ) -> dict[str, Any]:
        score = clamp_score(
            rule.business_return_base
            + ((bottleneck_relevance - 50) * 0.2)
            + ((rule.asset_creation_value - 50) * 0.1)
        )
        return {
            "score": score,
            "level": score_level(score),
            "time_horizon": "quarterly",
            "dimensions": template.business_return_dimensions,
            "expected_outcomes": [
                "Improve the constraining business capability",
                "Create reusable business value",
                "Increase decision quality through clearer evidence",
            ],
            "assumptions": [
                "Capability scores reflect the current PBHS assessment",
                "The owner or delegated support can execute the recommendation",
            ],
        }

    def _life_return(
        self,
        rule: RecommendationRule,
        template: RecommendationTemplate,
    ) -> dict[str, Any]:
        saved_hours_midpoint = sum(rule.human_time_saved_hours) / 2
        score = clamp_score(rule.life_return_base + (saved_hours_midpoint * 2))
        return {
            "score": score,
            "level": score_level(score),
            "time_horizon": "quarterly",
            "dimensions": template.life_return_dimensions,
            "expected_outcomes": [
                "Reduce unnecessary owner load",
                "Improve alignment between business activity and sustainable work",
            ],
            "assumptions": [
                "Time savings are reinvested into strategic, creative, or recovery time"
            ],
        }

    def _human_time(self, rule: RecommendationRule) -> dict[str, Any]:
        return {
            "estimated_hours_required": {
                "min": rule.human_time_hours[0],
                "max": rule.human_time_hours[1],
            },
            "estimated_hours_saved_per_week": {
                "min": rule.human_time_saved_hours[0],
                "max": rule.human_time_saved_hours[1],
            },
            "time_quality": ["strategic", "creative", "operational"],
            "time_horizon": "quarterly",
        }

    def _confidence(
        self,
        rule: RecommendationRule,
        average_capability_confidence: float,
        supporting_evidence_ids: list[str],
    ) -> float:
        evidence_completeness = min(1.0, len(supporting_evidence_ids) / 6)
        evidence_quality = average_capability_confidence
        evidence_consistency = 0.8
        rule_specificity = min(1.0, (len(rule.min_scores) + len(rule.max_scores)) / 4)
        return round(
            (evidence_completeness * 0.25)
            + (evidence_quality * 0.25)
            + (evidence_consistency * 0.20)
            + (average_capability_confidence * 0.20)
            + (rule_specificity * 0.10),
            2,
        )

    def _risk(self, rule: RecommendationRule, confidence: float) -> dict[str, Any]:
        evidence_uncertainty = 1 - confidence
        score = round(
            (rule.complexity * 0.25)
            + (self._human_time_burden(rule.human_time_hours[1]) * 0.20)
            + (rule.financial_cost * 0.15)
            + (rule.strategic_uncertainty * 0.15)
            + (rule.human_signature_risk * 0.15)
            + (evidence_uncertainty * 0.10),
            2,
        )
        return {
            "score": score,
            "level": risk_label(score),
            "dimensions": ["operational", "strategic", "human", "ai"],
            "mitigation": "Start with a bounded MVP and preserve human approval points.",
        }

    def _priority_score(
        self,
        business_return: float,
        life_return: float,
        bottleneck_relevance: float,
        human_signature_leverage: float,
        asset_creation_value: float,
        confidence: float,
        risk: float,
        max_hours_required: float,
    ) -> float:
        human_time_penalty = min(100, max_hours_required * 5)
        score = (
            (business_return * 0.25)
            + (life_return * 0.20)
            + (bottleneck_relevance * 0.20)
            + (human_signature_leverage * 0.10)
            + (asset_creation_value * 0.10)
            + ((confidence * 100) * 0.10)
            - ((risk * 100) * 0.10)
            - (human_time_penalty * 0.05)
        )
        return clamp_score(score)

    def _bottleneck_relevance(
        self,
        rule: RecommendationRule,
        score_by_capability: dict[str, CapabilityScore],
    ) -> float:
        bottleneck_scores = [
            score_by_capability[capability].score
            for capability in rule.bottleneck_capabilities
            if capability in score_by_capability
        ]
        if not bottleneck_scores:
            return 50
        return clamp_score(100 - min(bottleneck_scores))

    def _human_time_burden(self, max_hours_required: float) -> float:
        return min(1.0, max_hours_required / 20)


def clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def score_level(score: float) -> str:
    if score >= 80:
        return "very_high"
    if score >= 65:
        return "high"
    if score >= 45:
        return "medium"
    return "low"


def priority_level(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 50:
        return "medium"
    if score >= 30:
        return "low"
    return "deferred"


def confidence_label(score: float) -> str:
    if score <= 0.20:
        return "very_low"
    if score <= 0.40:
        return "low"
    if score <= 0.60:
        return "moderate"
    if score <= 0.80:
        return "high"
    return "very_high"


def risk_label(score: float) -> str:
    if score <= 0.20:
        return "very_low"
    if score <= 0.40:
        return "low"
    if score <= 0.60:
        return "moderate"
    if score <= 0.80:
        return "high"
    return "very_high"
