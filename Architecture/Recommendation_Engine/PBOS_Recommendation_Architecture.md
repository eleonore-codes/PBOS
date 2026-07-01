---
id: PBOS-REC-001
title: PBOS Recommendation Architecture
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
  - Recommendation
  - PBHS
  - Business Return
  - Life Return
  - Human Signature
  - Vision of Life
  - AI Employee
  - Executive Board

related_adrs:
  - ADR-001
---

# PBOS Recommendation Architecture

## Purpose

The PBOS Recommendation Architecture defines how PBOS transforms assessment results into prioritized executive recommendations.

Recommendations are the bridge between business diagnosis and action.

PBHS identifies what is true.

The Recommendation Engine determines what should happen next.

---

# Core Definition

A PBOS recommendation is an evidence-based investment proposal.

It tells the business owner:

- what to do
- why now
- what evidence supports it
- what Business Return is expected
- what Life Return is expected
- what Human Time is required
- which AI Employees can support execution
- whether the recommended path is DIY, DWY or DFY
- how success will be measured

---

# Architectural Role

The Recommendation Engine sits between:

```text
PBHS
    ↓
Recommendation Engine
    ↓
Executive Board
    ↓
Business Owner
    ↓
Strategy
    ↓
Departments
```

It converts interpretation into actionable priorities.

---

# Recommendation Inputs

The Recommendation Engine receives inputs from multiple PBOS subsystems.

## PBHS Inputs

- capability scores
- confidence scores
- capability maturity
- primary bottleneck
- secondary bottlenecks
- opportunity analysis
- longitudinal trends

---

## Business Inputs

- business model
- revenue streams
- cost structure
- offers
- customer segments
- current business assets

---

## Owner Inputs

- Vision of Life
- available Human Time
- financial constraints
- energy constraints
- strategic preferences
- non-negotiables

---

## AI Inputs

- available AI Employees
- available automations
- integration readiness
- execution capacity

---

# Recommendation Outputs

Every recommendation should produce:

- title
- executive summary
- business rationale
- supporting evidence
- expected Business Return
- expected Life Return
- estimated Human Time
- estimated cost
- confidence level
- urgency
- complexity
- recommended execution path
- assigned AI Employees
- success criteria
- review date

---

# Recommendation Types

PBOS supports multiple recommendation types.

## Strategic Recommendation

Changes direction or positioning.

Example:

Pause content creation and build a sponsorship system.

---

## Operational Recommendation

Improves processes or systems.

Example:

Document the podcast publishing workflow.

---

## Asset Recommendation

Creates or improves reusable business assets.

Example:

Build a Sponsor Media Kit.

---

## AI Leverage Recommendation

Uses AI to reduce work or increase capability.

Example:

Create an AI Publishing Manager.

---

## Commercial Recommendation

Improves revenue generation.

Example:

Create a workshop offer based on existing podcast episodes.

---

## Life Return Recommendation

Improves alignment with the owner's Vision of Life.

Example:

Move recording sessions to protected creative mornings.

---

# Recommendation Lifecycle

```text
Candidate Recommendation
        ↓
Evidence Check
        ↓
Business Return Estimate
        ↓
Life Return Estimate
        ↓
Constraint Check
        ↓
Prioritization
        ↓
Executive Board Review
        ↓
Owner Decision
        ↓
Execution
        ↓
Measurement
        ↓
Learning
```

---

# Decision Rules

## Rule 1 — No recommendation without evidence

Every recommendation must be supported by evidence or explicitly marked as low-confidence.

---

## Rule 2 — No recommendation may violate Vision of Life

If a recommendation conflicts with a declared non-negotiable, it must be rejected or redesigned.

---

## Rule 3 — Human Signature must be protected

Recommendations should increase the leverage of Human Signature rather than replace it.

---

## Rule 4 — Business Return and Life Return are evaluated together

Revenue-only recommendations are insufficient.

---

## Rule 5 — Prefer compounding assets

When two recommendations have similar expected return, PBOS should prioritize the one that creates reusable assets.

---

## Rule 6 — Prefer bottleneck relief

Recommendations that address the primary bottleneck should generally rank above recommendations addressing secondary issues.

---

# Prioritization Logic

Recommendations are ranked using multiple factors.

Positive factors:

- expected Business Return
- expected Life Return
- Human Signature leverage
- asset creation
- confidence
- strategic alignment
- bottleneck relevance

Negative factors:

- Human Time required
- financial cost
- cognitive load
- complexity
- execution risk
- conflict with Vision of Life

---

# Execution Path

Every recommendation should include one recommended execution path.

## DIY

The owner can execute independently.

Best when:

- complexity is low
- confidence is high
- required skills are available
- Human Time cost is acceptable

---

## DWY

The owner executes with guidance.

Best when:

- strategic judgment is required
- capability building matters
- learning is valuable
- implementation risk is moderate

---

## DFY

PBOS team or partners execute.

Best when:

- operational work is time-consuming
- founder involvement should be minimized
- execution quality must be high
- Human Signature is not required

---

# Relationship to Executive Board

The Recommendation Engine generates candidate recommendations.

The Executive Board reviews them through multiple perspectives.

Example:

- CFO evaluates financial return.
- CMO evaluates trust and marketing impact.
- COO evaluates operational feasibility.
- Chief AI Officer evaluates automation potential.
- Chief Wellbeing Officer evaluates Life Return.
- CEO evaluates strategic coherence.

---

# Relationship to AI Employees

AI Employees do not decide strategy independently.

They execute, prepare, analyze or support recommendations after approval.

Each recommendation may assign:

- primary AI Employee
- supporting AI Employees
- required human approval points

---

# Relationship to PBHS Report

The PBHS Executive Report presents the highest-priority recommendations in a form the business owner can understand and act upon.

The report should not expose every internal calculation.

It should present:

- the recommendation
- the reason
- the expected impact
- the execution path
- the confidence level

---

# Future Evolution

Future versions may include:

- recommendation templates
- portfolio optimization
- scenario simulation
- adaptive weighting
- recommendation history
- recommendation outcome tracking
- industry-specific recommendation libraries
- AI-assisted implementation planning

---

# Architectural Principle

PBOS recommendations are not tasks.

They are investment decisions.

A recommendation should only be generated when PBOS believes the proposed action is likely to improve Business Return, Life Return, Human Signature leverage or system capability.

---

# Changelog

## Version 0.1

Initial architecture for the PBOS Recommendation Engine.
