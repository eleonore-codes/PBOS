---
id: PBOS-PBHS-006
title: PBHS Scoring Model
version: 0.1
status: Draft
stability: evolving

category: Product

owner: PBOS Product Management

accountable_role: Business Owner
primary_ai_employee: Chief Strategy Officer

created: 2026-07-01
updated: 2026-07-01

related_entities:
  - PBHS
  - PBHS Capability Model
  - PBHS Evidence Model
  - PBHS Interpretation Model
  - Recommendation Engine
  - Executive Board

related_adrs:
  - ADR-001
---

# PBHS Scoring Model

## Purpose

The PBHS Scoring Model defines how PBOS transforms evidence into capability scores, confidence estimates, business interpretations and executive recommendations.

PBHS does not calculate a single business score.

PBHS evaluates business capabilities, their relationships and the confidence of the available evidence before generating recommendations.

The overall PBHS score is a summary of the complete assessment rather than its primary objective.

---

# Design Principles

The scoring model follows five principles.

## Capability First

Capabilities are scored individually before any overall score is calculated.

---

## Evidence First

Scores are derived from evidence rather than assumptions.

---

## Confidence Aware

Every capability score includes an explicit confidence level.

---

## Explainable

Every score can be traced back to supporting evidence.

---

## Actionable

Every score must support a business decision.

---

# Scoring Pipeline

```text
Evidence

↓

Indicators

↓

Capability Scores

↓

Confidence Scores

↓

Capability Relationships

↓

Pattern Recognition

↓

Executive Interpretation

↓

Recommendation Priority

↓

PBHS Summary
```

---

# Capability Scores

Each capability receives an independent score.

Initial range:

0–100

Example

Human Signature

92

Knowledge Assets

76

Podcast Assets

81

Trust

58

Business Systems

44

AI Leverage

29

Business Return

47

Life Return

69

---

# Confidence Scores

Every capability also receives a confidence estimate.

Confidence reflects evidence quality rather than business performance.

Scale

0–100

Example

Trust

Capability Score

58

Confidence

91

Interpretation

PBOS has strong evidence that Trust is currently moderate.

---

Example

AI Leverage

Capability Score

62

Confidence

28

Interpretation

PBOS currently has insufficient evidence.

Additional assessment is recommended.

---

# Evidence Weighting

Evidence sources contribute differently.

Initial weighting:

| Evidence Source | Initial Weight |
|-----------------|---------------:|
| Objective Business Evidence | 30% |
| Behavioral Evidence | 25% |
| Portfolio Evidence | 20% |
| Self-Report | 15% |
| AI Interview | 10% |

These weights are configurable and may evolve as PBOS gains additional validation data.

---

# Capability Maturity

Each capability receives both a score and a maturity level.

| Level | Range | Description |
|-------|-------|-------------|
| 1 | 0–20 | Initial |
| 2 | 21–40 | Developing |
| 3 | 41–60 | Managed |
| 4 | 61–80 | Optimized |
| 5 | 81–100 | Transformational |

The maturity level communicates capability development more effectively than the raw score alone.

---

# Dependency Analysis

Capabilities influence one another.

PBOS models these relationships explicitly.

Example

```text
Human Signature
        │
        ▼
Knowledge Assets
        │
        ▼
Podcast Assets
        │
        ▼
Trust
        │
        ▼
Business Return
        │
        ▼
Life Return
```

Recommendations should address upstream capabilities before downstream outcomes whenever appropriate.

---

# Bottleneck Detection

PBOS identifies the capability that most constrains Business Return and Life Return.

Selection criteria include:

- capability score
- confidence
- dependency relationships
- expected leverage
- implementation effort
- alignment with Vision of Life

The primary bottleneck is not necessarily the lowest-scoring capability.

---

# Opportunity Score

Each improvement opportunity receives an Opportunity Score.

The Opportunity Score estimates expected value by considering:

- expected Business Return
- expected Life Return
- Human Time required
- AI support available
- implementation complexity
- confidence

Higher Opportunity Scores receive higher recommendation priority.

---

# Recommendation Priority

Recommendations are ranked according to:

1. Opportunity Score
2. Confidence
3. Strategic alignment
4. Capability dependencies
5. Human Time efficiency

PBOS prioritizes recommendations with the highest expected long-term impact.

---

# Overall PBHS Score

The PBHS score is calculated only after all capabilities have been evaluated.

The overall score summarizes the current health of the business.

It should never replace capability-level analysis.

The overall score is intended for:

- trend analysis
- longitudinal tracking
- benchmarking
- executive summaries

Business decisions should always be based primarily on capability profiles.

---

# Trend Analysis

PBOS compares every assessment with previous assessments.

For each capability PBOS records:

- current score
- previous score
- direction of change
- rate of improvement
- confidence trend

Progress over time is more important than isolated assessments.

---

# Explainability

Every reported score must answer:

- Which evidence contributed?
- Which evidence was unavailable?
- Which capabilities influenced this result?
- How confident is PBOS?
- Which intervention is expected to improve the score?

---

# Future Evolution

Future versions may include:

- Bayesian updating
- probabilistic confidence models
- machine learning calibration
- industry-specific weighting
- benchmarking
- predictive simulations
- causal inference
- organizational scoring

---

# Architectural Principle

PBHS does not optimize numerical scores.

PBHS optimizes business capabilities that sustainably increase Business Return and Life Return while protecting Human Signature according to the owner's Vision of Life.

Scores support decisions.

They never replace judgment.

---

# Changelog

## Version 0.1

Initial capability-based scoring model with confidence estimates, dependency analysis and opportunity prioritization.