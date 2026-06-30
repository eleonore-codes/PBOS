---
id: PBOS-PBHS-002
title: PBHS Evidence Model
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
  - Recommendation Engine
  - Executive Board
  - Human Signature
  - Business Return
  - Life Return

related_adrs:
  - ADR-001
---

# PBHS Evidence Model

## Purpose

The PBHS Evidence Model defines how PBOS gathers, evaluates, combines and interprets evidence before generating recommendations.

PBOS does not rely on a single questionnaire or isolated metric.

Instead, PBOS integrates multiple independent evidence sources to build a comprehensive understanding of the business.

The objective is to produce recommendations that are explainable, trustworthy and actionable.

---

# Core Principle

PBOS should never generate an important recommendation from a single source of evidence when multiple independent sources are available.

Recommendations become more trustworthy as evidence converges from different methods.

---

# Evidence Pipeline

Evidence

↓

Interpretation

↓

Capability Assessment

↓

Recommendation

↓

Execution

↓

Measurement

↓

Learning

↓

Evidence

PBOS is a continuous learning system.

---

# Evidence Categories

PBHS organizes evidence into six categories.

## 1. Self-Report

### Purpose

Capture the business owner's perceptions, intentions and goals.

### Typical Sources

- PBHS Questionnaire
- Vision of Life Assessment
- Strategic planning sessions
- AI coaching conversations

### Strengths

- captures intentions
- captures motivation
- captures perceived constraints

### Limitations

- subject to bias
- optimism
- memory errors
- social desirability

---

## 2. Behavioral Evidence

### Purpose

Observe what actually happens.

### Typical Sources

- publishing frequency
- task completion
- AI usage
- automation usage
- workflow execution
- meeting patterns
- calendar data

### Strengths

- objective
- continuous
- difficult to manipulate

### Limitations

- requires integrations
- behavior may not reveal intent

---

## 3. Business Evidence

### Purpose

Measure business performance.

### Typical Sources

- revenue
- recurring revenue
- products
- customers
- leads
- sponsorships
- affiliate income
- conversion rates
- email subscribers

### Strengths

- objective
- measurable
- comparable

### Limitations

- mostly lagging indicators
- influenced by external factors

---

## 4. Portfolio Evidence

### Purpose

Evaluate the quality and maturity of business assets.

### Typical Sources

- website
- podcast
- YouTube
- LinkedIn
- newsletter
- courses
- templates
- media kit
- lead magnets

### Strengths

- reflects accumulated capability
- reveals strategic gaps
- directly actionable

### Limitations

- requires AI interpretation
- may need manual review

---

## 5. AI Interview

### Purpose

Understand context through adaptive conversation.

### Typical Sources

- strategic interviews
- coaching sessions
- planning conversations
- reflection exercises

The interview is dynamic.

Future questions depend on previous answers.

### Strengths

- captures nuance
- identifies hidden assumptions
- supports executive coaching

### Limitations

- depends on conversation quality
- requires interpretation

---

## 6. Longitudinal Evidence

### Purpose

Measure progress over time.

### Typical Sources

- previous PBHS assessments
- historical recommendations
- business trends
- capability development
- recurring patterns

### Strengths

- measures improvement
- identifies sustainable change
- supports forecasting

### Limitations

- unavailable for new users

---

# Evidence Quality

Not all evidence is equally reliable.

PBOS evaluates evidence using multiple quality dimensions.

## Reliability

Is the evidence consistent?

---

## Validity

Does the evidence actually measure the intended construct?

---

## Freshness

How recent is the evidence?

---

## Completeness

How much relevant information is available?

---

## Confidence

How confident is PBOS in its interpretation?

---

# Evidence Triangulation

Important business capabilities should ideally be supported by multiple evidence sources.

Example:

## Capability

Trust

### Self-Report

"I believe my audience trusts me."

### Behavioral

Repeat listeners.

### Business

Referral customers.

### Portfolio

Testimonials and case studies.

### AI Interview

Founder describes long-term client relationships.

### Longitudinal

Trust indicators improving over multiple assessments.

The stronger the agreement between evidence sources, the higher the confidence in the assessment.

---

# Capability Mapping

Every PBHS capability should specify its evidence sources.

| Capability | Self | Behavior | Business | Portfolio | AI Interview | Longitudinal |
|------------|:----:|:--------:|:--------:|:----------:|:------------:|:------------:|
| Human Signature | ✓ | ✓ | | ✓ | ✓ | ✓ |
| Knowledge Assets | ✓ | ✓ | | ✓ | | ✓ |
| Podcast Assets | ✓ | ✓ | | ✓ | | ✓ |
| Trust | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Business Systems | ✓ | ✓ | ✓ | | | ✓ |
| AI Leverage | ✓ | ✓ | | | ✓ | ✓ |
| Business Return | ✓ | | ✓ | | | ✓ |
| Life Return | ✓ | ✓ | | | ✓ | ✓ |

This matrix will evolve as PBOS gains access to additional integrations and data sources.

---

# Confidence Levels

PBOS should communicate confidence transparently.

## High Confidence

Three or more independent evidence sources support the same conclusion.

---

## Medium Confidence

Two independent evidence sources support the same conclusion.

---

## Low Confidence

Recommendation based primarily on one evidence source.

PBOS should explicitly encourage additional evidence collection before major strategic decisions.

---

# Explainability

Every recommendation should explain:

- which evidence was used
- why the recommendation was generated
- how confident PBOS is
- which additional evidence could improve future recommendations

Users should always understand the reasoning behind PBOS recommendations.

---

# Privacy and User Control

Business owners retain control over which evidence sources PBOS may access.

Users should be able to:

- enable or disable evidence sources
- review imported data
- delete imported data
- control AI access permissions

Recommendations should adapt to the available evidence.

---

# Future Evolution

Future versions may include:

- benchmarking against peer groups
- industry-specific evidence models
- external market indicators
- financial forecasting
- sentiment analysis
- sponsor readiness analysis
- executive team assessments
- multi-user collaboration
- predictive capability modelling

---

# Architectural Principle

PBOS does not seek perfect information.

PBOS seeks sufficient trustworthy evidence to recommend the next best action with appropriate confidence.

Continuous learning is preferred over waiting for complete certainty.

---

# Changelog

## Version 0.1

Initial definition of the PBHS multi-method evidence model.