---
id: PBOS-IMPL-002
title: PBHS MVP Data Contract
version: 0.1
status: Draft
stability: foundational

category: Implementation

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01
---

# PBHS MVP Data Contract

## Purpose

This document defines the minimum data contract required to implement the PBHS MVP without inventing new business concepts in software.

The contract preserves explainability, evidence provenance, versioning and the canonical PBOS pipeline.

---

# Scope

The MVP data contract supports:

- one Business Owner
- one Business profile
- PBHS questionnaire evidence
- capability scoring
- prioritized recommendations
- Executive Board review summaries
- Business Owner decision state
- Executive Report generation

---

# Non-Goals

The MVP does not implement:

- full Executive Board simulation
- Strategy workspace
- Departments workspace
- Operational AI Employees
- external integrations
- payments
- multi-user teams

---

# Canonical Pipeline

```text
PBHS
    ->
Recommendation Engine
    ->
Executive Board
    ->
Business Owner
    ->
Strategy
    ->
Departments
```

For the MVP, Strategy and Departments may be represented only as deferred downstream stages.

---

# MVP Domain Objects

The MVP must preserve these domain objects:

- User
- Business
- PBHS Assessment
- PBHS Question
- PBHS Response
- Evidence Item
- Capability Score
- Recommendation
- Executive Review
- Business Owner Decision
- Executive Report

---

# User Contract

Required fields:

- user_id
- name
- email
- created_at

---

# Business Contract

Required fields:

- business_id
- user_id
- name
- industry
- created_at

Optional MVP fields:

- business_stage
- primary_business_model
- vision_of_life_version
- business_vision_version

---

# Assessment Contract

Required fields:

- assessment_id
- business_id
- pbhs_version
- status
- created_at
- completed_at

Allowed status values:

- draft
- submitted
- scored
- recommendations_generated
- reviewed
- reported

---

# Question Contract

Required fields:

- question_id
- capability
- construct
- question_text
- response_scale
- version
- status

Allowed status values:

- active
- experimental
- retired

---

# Response Contract

Required fields:

- response_id
- assessment_id
- question_id
- response_value
- submitted_at

Rules:

- response_value must follow the question response scale
- every response must remain traceable to the question version used

---

# Evidence Contract

Required fields:

- evidence_id
- assessment_id
- evidence_source
- related_capability
- source_reference
- evidence_value
- confidence
- created_at

Allowed evidence_source values:

- self_report
- behavioral
- business
- portfolio
- ai_interview
- longitudinal

MVP rule:

Questionnaire responses are stored as self_report evidence.

Future evidence sources may be empty in the MVP but must not require schema redesign.

---

# Capability Score Contract

Required fields:

- capability_score_id
- assessment_id
- capability
- score
- maturity_level
- confidence
- calculation_method
- evidence_ids

Rules:

- score uses a 0-100 scale
- confidence uses a 0.00-1.00 scale
- every score must be explainable from evidence

---

# Recommendation Contract

Required fields:

- recommendation_id
- assessment_id
- title
- description
- priority
- confidence
- expected_business_return
- expected_life_return
- human_time_required
- supporting_evidence_ids
- rationale
- recommended_execution_path
- status

Allowed recommended_execution_path values:

- DIY
- DWY
- DFY

Allowed status values:

- candidate
- reviewed
- approved
- rejected
- deferred
- superseded

---

# Executive Review Contract

Required fields:

- executive_review_id
- recommendation_id
- executive_role
- opinion
- rationale
- confidence
- risks
- opportunities
- suggested_modifications

MVP rule:

Executive Review may be generated as a lightweight structured summary. Full Executive Board simulation is deferred.

---

# Business Owner Decision Contract

Required fields:

- decision_id
- recommendation_id
- decision
- decision_date
- decision_rationale

Allowed decision values:

- approve
- reject
- defer
- request_more_evidence

---

# Executive Report Contract

Required fields:

- report_id
- assessment_id
- report_version
- generated_at
- executive_summary
- capability_profile
- bottleneck_analysis
- recommendation_portfolio
- confidence_summary
- action_plan_90_days

Rules:

- report content must trace back to assessment, evidence, scores and recommendations
- report generation must not overwrite source assessment data

---

# Versioning Rules

The MVP must preserve:

- PBHS version
- question version
- scoring method
- report version

Historical assessments must remain understandable after future PBHS changes.

---

# Explainability Requirements

Every capability score must answer:

- which responses contributed
- which evidence source was used
- how the score was calculated
- how confident PBOS is

Every recommendation must answer:

- why it was generated
- which capability or bottleneck it addresses
- which evidence supports it
- what Business Return is expected
- what Life Return is expected
- what Human Time is required

---

# Deferred Fields

The MVP may defer full support for:

- strategy_objective_id
- initiative_id
- project_id
- deliverable_id
- department_id
- ai_employee_id
- external_integration_id

These fields should be introduced when Strategy, Departments and Operational AI Employees enter scope.

---

# Acceptance Criteria

The data contract is sufficient when the MVP can:

1. Create a Business profile.
2. Start a PBHS Assessment.
3. Store versioned PBHS Questions.
4. Store PBHS Responses as self-report Evidence Items.
5. Calculate explainable Capability Scores.
6. Generate prioritized Recommendations.
7. Store lightweight Executive Reviews.
8. Store Business Owner decisions.
9. Generate an Executive Report traceable to source data.

---

# Status

Version: 0.1

Status: Active
