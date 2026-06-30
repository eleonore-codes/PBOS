---
id: PBOS-REC-002
title: PBOS Recommendation Pipeline
version: 0.1
status: Draft
stability: evolving

category: Architecture

owner: PBOS Architecture

accountable_role: Business Owner
primary_ai_employee: Chief Strategy Officer

created: 2026-07-01
updated: 2026-07-01

related_entities:
  - Recommendation Engine
  - PBHS
  - Executive Board
  - AI Employee

related_adrs:
  - ADR-001
---

# PBOS Recommendation Pipeline

## Purpose

The Recommendation Pipeline defines the sequential decision-making process used by PBOS to transform business evidence into prioritized executive recommendations.

Every recommendation follows the same pipeline.

This ensures consistency, explainability and continuous learning.

---

# Pipeline Overview

```text
Evidence Collection
        ↓
Capability Assessment
        ↓
Interpretation
        ↓
Constraint Analysis
        ↓
Opportunity Discovery
        ↓
Recommendation Generation
        ↓
Recommendation Prioritization
        ↓
Executive Board Review
        ↓
Business Owner Decision
        ↓
Execution
        ↓
Outcome Measurement
        ↓
Continuous Learning
```

---

# Stage 1 — Evidence Collection

Objective:

Collect all available evidence.

Examples:

- PBHS Questionnaire
- Business Metrics
- Portfolio Analysis
- AI Interview
- Historical Assessments
- External Integrations

Output:

Evidence Package

---

# Stage 2 — Capability Assessment

Objective:

Calculate capability scores and confidence levels.

Output:

Capability Profile

---

# Stage 3 — Interpretation

Objective:

Identify strengths, weaknesses, dependencies and bottlenecks.

Output:

Business Interpretation

---

# Stage 4 — Constraint Analysis

Objective:

Identify constraints that limit recommendation options.

Examples:

- Human Time
- Budget
- Vision of Life
- Available Skills
- Existing Commitments
- Technical Limitations

Output:

Constraint Profile

---

# Stage 5 — Opportunity Discovery

Objective:

Generate possible interventions.

Examples:

- create a lead magnet
- improve onboarding
- automate publishing
- redesign pricing
- launch sponsorship package

Output:

Opportunity Portfolio

---

# Stage 6 — Recommendation Generation

Objective:

Transform opportunities into executable recommendations.

Each recommendation includes:

- rationale
- expected outcomes
- required resources
- AI Employees
- execution path

Output:

Candidate Recommendations

---

# Stage 7 — Recommendation Prioritization

Objective:

Rank recommendations.

Evaluation criteria include:

- Business Return
- Life Return
- Human Time
- Strategic Alignment
- Confidence
- Complexity
- Risk
- Asset Creation

Output:

Prioritized Recommendation Portfolio

---

# Stage 8 — Executive Board Review

Objective:

Review recommendations from multiple executive perspectives.

Participants include:

- CEO
- Chief Strategy Officer
- Chief Financial Officer
- Chief Marketing Officer
- Chief Operations Officer
- Chief AI Officer
- Chief Wellbeing Officer

Output:

Executive Recommendation Package

---

# Stage 9 — Business Owner Decision

Objective:

Approve, postpone, reject or modify recommendations.

Possible outcomes:

- Approve
- Reject
- Delegate
- Schedule
- Request Additional Evidence

Output:

Approved Action Plan

---

# Stage 10 — Execution

Objective:

Execute approved recommendations.

Execution may involve:

- Business Owner
- AI Employees
- External Partners
- Contractors

Output:

Completed Work

---

# Stage 11 — Outcome Measurement

Objective:

Measure actual results.

Metrics include:

- Business Return
- Life Return
- Capability Improvement
- Time Saved
- Revenue Impact
- Asset Growth

Output:

Outcome Report

---

# Stage 12 — Continuous Learning

Objective:

Improve future recommendations.

PBOS updates:

- confidence estimates
- recommendation effectiveness
- capability history
- business knowledge
- execution preferences

Output:

Improved Recommendation Engine

---

# Pipeline Principles

Every stage should be:

- explainable
- modular
- repeatable
- measurable
- auditable

Each stage should produce explicit outputs that become inputs for the next stage.

---

# Failure Handling

If evidence is insufficient:

- lower confidence
- request additional information
- avoid high-impact recommendations

PBOS should prefer uncertainty over false certainty.

---

# Architectural Principle

Recommendations are generated through a transparent pipeline rather than opaque AI reasoning.

Every recommendation should be reproducible from its evidence and processing history.

---

# Changelog

## Version 0.1

Initial definition of the PBOS Recommendation Pipeline.