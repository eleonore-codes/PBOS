---
id: PBHS-API-v1
title: PBHS Core v1 Public REST API
version: 1.0
status: Frozen
stability: canonical
category: API
owner: PBOS Architecture
created: 2026-07-01
updated: 2026-07-01
implemented_scope: M13-M17
---

# PBHS Core v1 Public REST API

## Purpose

This document freezes the implemented public REST API for PBHS Core v1.

It describes the actual API surface implemented in the backend at the end of M17. It supersedes earlier draft API descriptions where those drafts include unimplemented endpoints or lifecycle states.

PBHS Core v1 implements a deterministic decision-support pipeline:

```text
User -> Business -> Assessment -> Responses -> Evidence -> Scores -> Recommendations
```

## Base URL

All canonical v1 domain endpoints are mounted under:

```text
/api/v1
```

The system health endpoint is mounted outside the v1 domain API:

```text
/health
```

## Versioning Policy

PBHS Core v1 uses path-based API versioning.

The canonical v1 base path is:

```text
/api/v1
```

Rules:

- Backward-compatible additions may be added under `/api/v1`.
- Breaking changes must use a new path version, for example `/api/v2`.
- Existing v1 response fields must not be renamed, removed, or changed in meaning.
- Enum values used by v1 clients must remain valid for v1.
- Historical assessments remain tied to their stored `pbhs_version`, question snapshots, rule versions, template versions, and engine versions.

## Authentication

Authentication is not implemented in PBHS Core v1.

The API accepts direct user and business identifiers. Access control, identity providers, sessions, organizations, API keys, and role-based permissions are deferred.

## Error Format

Implemented API errors use FastAPI's canonical HTTP error shape:

```json
{
  "detail": "error_code"
}
```

Validation errors produced by the framework use FastAPI/Pydantic validation error structures.

## Error Codes

Implemented domain errors use stable string codes.

| Error code | HTTP status | Meaning |
| --- | ---: | --- |
| `user_email_already_exists` | 409 | A user with the submitted email already exists. |
| `user_not_found` | 404 | The referenced user does not exist. |
| `business_not_found` | 404 | The referenced business does not exist. |
| `assessment_not_found` | 404 | The referenced assessment does not exist. |
| `recommendation_not_found` | 404 | The referenced recommendation does not exist. |
| `assessment_locked` | 409 | Responses cannot be changed because the assessment is no longer draft. |
| `invalid_status_transition` | 409 | The requested lifecycle transition is not valid from the current state. |
| `assessment_incomplete` | 409 | Required assessment questions are not all answered. |
| `assessment_has_no_required_questions` | 409 | The assessment has no required questions and cannot be submitted. |
| `assessment_not_submitted` | 409 | Scoring was requested before assessment submission. |
| `assessment_not_scored` | 409 | Scores or recommendations were requested before scoring. |
| `missing_required_evidence` | 409 | A required response lacks corresponding evidence. |
| `capability_has_no_scoreable_responses` | 409 | A capability has no scoreable response inputs. |
| `no_matching_recommendations` | 409 | No recommendation rules matched the scored assessment. |
| `question_not_in_assessment` | 422 | The submitted question is not part of the assessment snapshot. |
| `response_value_must_be_integer_1_to_5` | 422 | A `likert_1_5` response was not an integer from 1 to 5. |
| `response_value_must_be_integer_1_to_7` | 422 | A `likert_1_7` response was not an integer from 1 to 7. |
| `response_value_must_be_boolean` | 422 | A `yes_no` response was not boolean. |
| `response_value_must_be_non_empty_text` | 422 | A `text` response was empty or not a string. |
| `unsupported_response_scale` | 422 | The response scale is not supported by the relevant operation. |

## Lifecycle

Implemented assessment lifecycle:

```text
draft -> submitted -> scored -> recommendations_generated
```

Implemented recommendation lifecycle:

```text
candidate
```

Recommendation status values beyond `candidate` are reserved by the enum but are not transitioned by PBHS Core v1.

## Endpoints

### Health Check

```http
GET /health
```

Returns service health.

Response:

```json
{
  "status": "ok"
}
```

### Create User

```http
POST /api/v1/users
```

Creates a user record representing the business owner.

Request model:

```json
{
  "name": "Customer Zero",
  "email": "customer@example.com"
}
```

Response model: `UserRead`

Status: `201 Created`

Errors:

- `409 user_email_already_exists`

### Create Business

```http
POST /api/v1/businesses
```

Creates a business profile owned by a user.

Request model:

```json
{
  "user_id": "uuid",
  "name": "PBOS Studio",
  "industry": "Education",
  "business_stage": "optional string",
  "primary_business_model": "optional string",
  "vision_of_life_version": "optional string",
  "business_vision_version": "optional string"
}
```

Response model: `BusinessRead`

Status: `201 Created`

Errors:

- `404 user_not_found`

### Get Business

```http
GET /api/v1/businesses/{business_id}
```

Returns a business profile.

Response model: `BusinessRead`

Errors:

- `404 business_not_found`

### Create PBHS Question

```http
POST /api/v1/pbhs/questions
```

Creates a PBHS question definition.

This endpoint is part of the implemented v1 surface. It is used to seed the question bank from which assessment snapshots are created.

Request model:

```json
{
  "capability": "Human Signature",
  "construct": "Differentiation",
  "question_text": "My business communicates expertise competitors cannot copy.",
  "response_scale": "likert_1_5",
  "version": "0.1",
  "status": "active"
}
```

Response model: `QuestionRead`

Status: `201 Created`

### List Active PBHS Questions

```http
GET /api/v1/pbhs/questions
```

Returns active PBHS questions.

Response model:

```json
[
  {
    "question_id": "uuid",
    "capability": "Human Signature",
    "construct": "Differentiation",
    "question_text": "My business communicates expertise competitors cannot copy.",
    "response_scale": "likert_1_5",
    "version": "0.1",
    "status": "active"
  }
]
```

### Start Assessment

```http
POST /api/v1/businesses/{business_id}/assessments
```

Creates a draft assessment for a business and snapshots all active PBHS questions.

Request model:

```json
{
  "pbhs_version": "0.1"
}
```

Response model: `AssessmentRead`

Status: `201 Created`

Errors:

- `404 business_not_found`

### Get Assessment

```http
GET /api/v1/assessments/{assessment_id}
```

Returns assessment metadata and status.

Response model: `AssessmentRead`

Errors:

- `404 assessment_not_found`

### List Assessment Questions

```http
GET /api/v1/assessments/{assessment_id}/questions
```

Returns immutable question snapshots for an assessment.

Response model: list of `AssessmentQuestionRead`

Errors:

- `404 assessment_not_found`

### Get Assessment Progress

```http
GET /api/v1/assessments/{assessment_id}/progress
```

Returns completion progress for required questions.

Response model:

```json
{
  "assessment_id": "uuid",
  "status": "draft",
  "total_required_questions": 8,
  "answered_required_questions": 4,
  "percent_complete": 50.0,
  "missing_question_ids": ["uuid"],
  "missing_capabilities": ["Knowledge Assets"],
  "locked": false
}
```

Errors:

- `404 assessment_not_found`

### Submit Response

```http
POST /api/v1/assessments/{assessment_id}/responses
```

Creates or updates a response for a draft assessment. Each response creates or updates one self-report evidence item.

Request model:

```json
{
  "question_id": "uuid",
  "response_value": 4
}
```

Response model: `ResponseSubmissionRead`

Status: `201 Created`

Errors:

- `404 assessment_not_found`
- `409 assessment_locked`
- `422 question_not_in_assessment`
- `422 response_value_must_be_integer_1_to_5`
- `422 response_value_must_be_integer_1_to_7`
- `422 response_value_must_be_boolean`
- `422 response_value_must_be_non_empty_text`
- `422 unsupported_response_scale`

### List Assessment Responses

```http
GET /api/v1/assessments/{assessment_id}/responses
```

Returns responses submitted for an assessment.

Response model: list of `ResponseRead`

Errors:

- `404 assessment_not_found`

### List Assessment Evidence

```http
GET /api/v1/assessments/{assessment_id}/evidence
```

Returns evidence items for an assessment.

Response model: list of `EvidenceRead`

Note: PBHS Core v1 does not explicitly reject unknown assessment IDs for this endpoint. If no evidence exists, the endpoint returns an empty list.

### Submit Assessment

```http
POST /api/v1/assessments/{assessment_id}/submit
```

Transitions a complete draft assessment to `submitted`.

Response model: `AssessmentRead`

Errors:

- `404 assessment_not_found`
- `409 invalid_status_transition`
- `409 assessment_has_no_required_questions`
- `409 assessment_incomplete`

### Score Assessment

```http
POST /api/v1/assessments/{assessment_id}/score
```

Scores a submitted or already scored assessment.

The scoring operation is deterministic and idempotent. Existing capability score rows are updated for the same assessment and capability.

Response model: `AssessmentScoreRead`

Errors:

- `404 assessment_not_found`
- `409 assessment_not_submitted`
- `409 assessment_incomplete`
- `409 missing_required_evidence`
- `409 capability_has_no_scoreable_responses`
- `422 unsupported_response_scale`
- `422 response_value_must_be_integer_1_to_5`

### Get Assessment Scores

```http
GET /api/v1/assessments/{assessment_id}/scores
```

Returns persisted scoring results for an assessment.

Response model: `AssessmentScoreRead`

Errors:

- `404 assessment_not_found`
- `409 assessment_not_scored`

### Generate Recommendations

```http
POST /api/v1/pbhs/assessments/{assessment_id}/recommendations/generate
```

Generates deterministic recommendation candidates for a scored assessment.

The operation is idempotent by recommendation type. Existing matching recommendations are updated. Existing recommendations whose type no longer matches generated rules are marked `superseded`.

Response model: `RecommendationPortfolioRead`

Errors:

- `404 assessment_not_found`
- `409 assessment_not_scored`
- `409 no_matching_recommendations`

### List Recommendations

```http
GET /api/v1/pbhs/assessments/{assessment_id}/recommendations
```

Returns recommendations persisted for an assessment, ordered by descending priority score.

Response model: list of `RecommendationRead`

Errors:

- `404 assessment_not_found`

### Get Recommendation

```http
GET /api/v1/recommendations/{recommendation_id}
```

Returns a recommendation by ID.

Response model: `RecommendationRead`

Errors:

- `404 recommendation_not_found`

### Explain Recommendation

```http
GET /api/v1/recommendations/{recommendation_id}/explain
```

Returns the explanation subset for a recommendation.

Response model: `RecommendationExplanationRead`

Errors:

- `404 recommendation_not_found`

### Get Recommendation Evidence

```http
GET /api/v1/recommendations/{recommendation_id}/evidence
```

Returns provenance links from a recommendation to capability scores and evidence.

Response model: `RecommendationEvidenceRead`

Errors:

- `404 recommendation_not_found`

## Canonical Models

### UserCreate

```json
{
  "name": "string",
  "email": "string"
}
```

Constraints:

- `name`: length 1-200
- `email`: length 3-320

### UserRead

```json
{
  "user_id": "uuid",
  "name": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### BusinessCreate

```json
{
  "user_id": "uuid",
  "name": "string",
  "industry": "string",
  "business_stage": "string | null",
  "primary_business_model": "string | null",
  "vision_of_life_version": "string | null",
  "business_vision_version": "string | null"
}
```

### BusinessRead

```json
{
  "business_id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "industry": "string",
  "created_at": "datetime",
  "business_stage": "string | null",
  "primary_business_model": "string | null",
  "vision_of_life_version": "string | null",
  "business_vision_version": "string | null"
}
```

### AssessmentCreate

```json
{
  "pbhs_version": "string"
}
```

Constraints:

- `pbhs_version`: length 1-50

### AssessmentRead

```json
{
  "assessment_id": "uuid",
  "business_id": "uuid",
  "pbhs_version": "string",
  "status": "draft | submitted | scored | recommendations_generated",
  "created_at": "datetime",
  "completed_at": "datetime | null"
}
```

### QuestionCreate

```json
{
  "capability": "string",
  "construct": "string",
  "question_text": "string",
  "response_scale": "string",
  "version": "string",
  "status": "active | experimental | retired"
}
```

### QuestionRead

```json
{
  "question_id": "uuid",
  "capability": "string",
  "construct": "string",
  "question_text": "string",
  "response_scale": "string",
  "version": "string",
  "status": "active | experimental | retired"
}
```

### AssessmentQuestionRead

```json
{
  "assessment_question_id": "uuid",
  "assessment_id": "uuid",
  "question_id": "uuid",
  "question_version": "string",
  "capability": "string",
  "construct": "string",
  "question_text": "string",
  "response_scale": "string",
  "required": true,
  "order_index": 1,
  "source_status": "active",
  "created_at": "datetime"
}
```

### ResponseCreate

```json
{
  "question_id": "uuid",
  "response_value": "any JSON value"
}
```

### ResponseRead

```json
{
  "response_id": "uuid",
  "assessment_id": "uuid",
  "question_id": "uuid",
  "question_version": "string",
  "response_value": "any JSON value",
  "submitted_at": "datetime"
}
```

### EvidenceRead

```json
{
  "evidence_id": "uuid",
  "assessment_id": "uuid",
  "response_id": "uuid | null",
  "evidence_source": "self_report | behavioral | business | portfolio | ai_interview | longitudinal",
  "related_capability": "string",
  "source_reference": "string",
  "evidence_value": "any JSON value",
  "confidence": 1.0,
  "created_at": "datetime"
}
```

### ResponseSubmissionRead

```json
{
  "response": "ResponseRead",
  "evidence": "EvidenceRead"
}
```

### CapabilityScoreRead

```json
{
  "capability_score_id": "uuid",
  "assessment_id": "uuid",
  "capability": "string",
  "score": 75.0,
  "maturity_level": 4,
  "confidence": 0.4,
  "calculation_method": "pbhs_questionnaire_v1",
  "evidence_ids": ["uuid"],
  "scored_at": "datetime"
}
```

### AssessmentScoreRead

```json
{
  "assessment_id": "uuid",
  "status": "scored",
  "overall_score": 75.0,
  "overall_confidence": 0.4,
  "calculation_method": "pbhs_questionnaire_v1",
  "scored_at": "datetime",
  "capability_scores": ["CapabilityScoreRead"]
}
```

### RecommendationRead

```json
{
  "recommendation_id": "uuid",
  "assessment_id": "uuid",
  "rule_id": "string",
  "rule_version": "string",
  "template_id": "string",
  "template_version": "string",
  "recommendation_type": "SPONSOR_READINESS | CONTENT_SYSTEM | EMAIL_FUNNEL | AUTOMATION | KNOWLEDGE_LIBRARY",
  "category": "strategic | operational | asset | ai_leverage | commercial | life_return",
  "title": "string",
  "description": "string",
  "priority": "critical | high | medium | low | deferred",
  "priority_score": 0.0,
  "priority_rationale": "string",
  "confidence": 0.0,
  "confidence_label": "very_low | low | moderate | high | very_high",
  "risk_score": 0.0,
  "risk_label": "very_low | low | moderate | high | very_high",
  "expected_business_return": {},
  "expected_life_return": {},
  "human_time_required": {},
  "human_signature_impact": {},
  "triggered_capabilities": ["string"],
  "capability_score_ids": ["uuid"],
  "supporting_evidence_ids": ["uuid"],
  "rationale": {},
  "calculation_trace": {},
  "recommended_execution_path": "DIY | DWY | DFY",
  "success_criteria": ["string"],
  "status": "candidate | reviewed | approved | rejected | deferred | superseded",
  "created_at": "datetime",
  "generated_at": "datetime"
}
```

### RecommendationPortfolioRead

```json
{
  "assessment_id": "uuid",
  "status": "recommendations_generated",
  "engine_version": "m17_recommendation_engine_v1",
  "rule_set_version": "m17_rules_v1",
  "generated_at": "datetime",
  "recommendations": ["RecommendationRead"],
  "generation_run": {
    "run_id": "string",
    "assessment_id": "uuid",
    "engine_version": "m17_recommendation_engine_v1",
    "rule_set_version": "m17_rules_v1",
    "started_at": "datetime",
    "completed_at": "datetime | null",
    "status": "completed",
    "error_summary": "string | null"
  }
}
```

### RecommendationExplanationRead

```json
{
  "recommendation_id": "uuid",
  "recommendation_type": "SPONSOR_READINESS | CONTENT_SYSTEM | EMAIL_FUNNEL | AUTOMATION | KNOWLEDGE_LIBRARY",
  "title": "string",
  "rationale": {},
  "calculation_trace": {},
  "priority_rationale": "string"
}
```

### RecommendationEvidenceRead

```json
{
  "recommendation_id": "uuid",
  "recommendation_type": "SPONSOR_READINESS | CONTENT_SYSTEM | EMAIL_FUNNEL | AUTOMATION | KNOWLEDGE_LIBRARY",
  "capability_score_ids": ["uuid"],
  "supporting_evidence_ids": ["uuid"],
  "triggered_capabilities": ["string"]
}
```

## Deferred API Scope

The following are not implemented in PBHS Core v1 and are outside the frozen v1 contract:

- Authentication and authorization endpoints.
- Executive report generation and retrieval endpoints.
- Business Owner decision endpoints.
- Recommendation review, approval, rejection, deferment, and supersession workflows, except internal supersession during regeneration.
- Executive Board endpoints.
- Strategy, objective, project, department, and AI Employee endpoints.
- External evidence ingestion endpoints.
- Longitudinal reassessment and trend endpoints.
- Multi-user organization or workspace endpoints.

