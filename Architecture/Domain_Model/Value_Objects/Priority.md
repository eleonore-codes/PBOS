---
id: PBOS-VO-007
title: Priority
version: 0.1
status: Draft
stability: foundational

category: Domain Model

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01

related_entities:
  - Recommendation
  - Objective
  - Initiative
  - Project
  - Executive Agent
---

# Priority (Value Object)

## Purpose

Priority represents the relative importance of a recommendation, objective, initiative or project within PBOS.

It helps the Executive Board decide what should be addressed first when resources are limited.

Priority is determined through evidence rather than intuition alone.

---

# Definition

Priority is a Value Object.

It has no independent identity.

Its value is derived from strategic importance, expected impact, urgency, confidence, risk and alignment with the Vision of Life.

---

# Mission

Ensure that PBOS consistently focuses resources on the work that creates the greatest overall value.

---

# Characteristics

Priority is:

- evidence-based
- explainable
- dynamic
- comparable
- transparent
- continuously reviewed

---

# Priority Factors

Priority may be influenced by:

- Vision of Life Alignment
- Business Vision Alignment
- Strategic Importance
- Business Return
- Life Return
- Human Signature
- Human Time
- Confidence
- Risk
- Urgency
- Dependencies
- Available Capacity

---

# Attributes

Priority may contain:

- Priority Score
- Priority Level
- Calculation Method
- Supporting Evidence
- Last Evaluation Date
- Reviewer

---

# Priority Levels

PBOS recommends five levels:

| Level | Meaning |
|--------|---------|
| Critical | Immediate strategic attention required |
| High | Execute as soon as practical |
| Medium | Important but not urgent |
| Low | Valuable when capacity permits |
| Deferred | Reconsider during a future planning cycle |

---

# Relationships

Priority may be associated with:

- Recommendations
- Objectives
- Initiatives
- Projects
- Deliverables
- Departments
- Executive Decisions

---

# Design Principles

Priority should:

- align with the Vision of Life
- maximize long-term value
- balance Business Return and Life Return
- remain explainable
- be recalculated as evidence changes

---

# Example

Recommendation

Launch Executive Dashboard MVP.

Business Return

High

Life Return

High

Human Signature

Strengthened

Confidence

0.84

Risk

Moderate

Priority

High

Reason

The recommendation creates reusable infrastructure supporting multiple future initiatives while reducing long-term operational effort.

---

# Relationship to Confidence

Confidence measures how certain PBOS is.

Priority measures how important the recommendation is.

The two should not be confused.

---

# Relationship to Risk

Risk influences Priority but does not determine it.

Some high-risk recommendations remain high priority because of their strategic importance.

---

# Relationship to Executive Board

Executive Agents propose Priority.

The Executive Board discusses and refines it.

The Business Owner approves the final Priority.

---

# Architectural Principle

Priority is the mechanism by which PBOS allocates scarce resources.

Every significant recommendation should have an explicit, explainable Priority.

---

# Future Evolution

Future versions may support:

- weighted prioritization models
- AI-assisted priority optimization
- portfolio balancing
- scenario-dependent priorities
- adaptive reprioritization
- capacity-aware scheduling

---

# Status

Version: 0.1

Status: Foundational