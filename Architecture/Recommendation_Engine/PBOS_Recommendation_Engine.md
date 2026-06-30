---
id: PBOS-ARCH-002
title: PBOS Recommendation Engine
version: 0.1
status: Draft
stability: experimental

category: Architecture

owner: PBOS Architecture

accountable_role: Business Owner

created: 2026-06-30
updated: 2026-06-30

related_entities:
  - Purpose
  - Vision of Life
  - Human Signature
  - Business Return
  - Life Return
  - Investment
  - Recommendation
  - Executive
  - AI Employee
  - Podcast Business Health Score (PBHS)

related_adrs:
  - ADR-001

---

# PBOS Recommendation Engine

## Purpose

The PBOS Recommendation Engine transforms business knowledge into prioritized actions.

Its purpose is not to maximize productivity.

Its purpose is to maximize **Business Return** and **Life Return** according to the owner's **Vision of Life** while protecting and amplifying the owner's **Human Signature**.

---

# Mission

At every moment PBOS should answer one question:

> What is the highest-value thing this business owner should do next?

The answer must be personalized.

It must consider the current business, available time, strategic goals, available AI Employees and the owner's Vision of Life.

---

# Architectural Principle

PBOS does not optimize for:

- activity
- output
- hours worked

PBOS optimizes for:

- Business Return
- Life Return
- Human Signature Leverage
- Knowledge Asset Growth
- Sustainable execution

---

# Inputs

The Recommendation Engine continuously receives information from multiple sources.

## Identity

- Purpose
- Vision of Life
- Human Signature

---

## Business

- Business Assets
- Knowledge Assets
- Podcast Assets
- Revenue
- Costs

---

## Operations

- Business Capability Profile
- Active Projects
- Available AI Employees
- Available Automations

---

## Measurement

- PBHS
- Business Return Score
- Alignment Score
- Business Capability Score

---

## Constraints

- Available time
- Budget
- Energy
- Cognitive capacity
- Family commitments
- Strategic priorities

---

# Decision Questions

Every recommendation should answer:

1. What is happening?
2. Why is it happening?
3. What should improve first?
4. Why this before everything else?
5. What Business Return is expected?
6. What Life Return is expected?
7. How much Human Time is required?
8. Can AI execute all or part of the work?
9. Should the owner DIY, DWY or DFY?
10. How will success be measured?

---

# Recommendation Pipeline

Business Reality

↓

PBHS observes

↓

Executive Board evaluates

↓

Recommendation Engine prioritizes

↓

AI Employees prepare execution plans

↓

Business Owner approves strategic work

↓

Execution

↓

Measurement

↓

Learning

↓

Next recommendation

---

# Recommendation Categories

Recommendations may improve:

## Business

- Revenue
- Profitability
- Marketing
- Sales
- Products
- Customer Success

---

## Knowledge

- Knowledge Assets
- Podcast Assets
- Educational Assets
- Brand Authority

---

## Operations

- Automation
- Delegation
- Process Improvement
- AI Adoption

---

## Personal

- Time
- Energy
- Focus
- Family Time
- Recovery
- Learning

---

# Recommendation Score

Each recommendation receives a PBOS Recommendation Score.

The score should consider multiple dimensions.

## Positive Factors

- Expected Business Return
- Expected Life Return
- Human Signature Leverage
- Trust Growth
- Knowledge Asset Growth
- Strategic Alignment
- Customer Value

---

## Negative Factors

- Human Time Required
- Cognitive Load
- Opportunity Cost
- Financial Cost
- Execution Risk
- Complexity

---

## Example Concept

PBOS does not calculate success using a single ROI metric.

Instead it evaluates the overall expected contribution to the business owner's long-term objectives.

Conceptually:

Business Return

+

Life Return

+

Human Signature Leverage

+

Knowledge Asset Growth

+

Trust Growth

−

Human Time

−

Opportunity Cost

−

Execution Complexity

=

PBOS Recommendation Score

The exact weighting of these dimensions is configurable and evolves as PBOS matures.

---

# Recommendation Output

Every recommendation should include:

## Executive Summary

One sentence.

---

## Why Now?

Why this action has the highest priority.

---

## Expected Business Return

Estimated impact.

---

## Expected Life Return

Estimated improvement in quality of life.

---

## Time Investment

Estimated Human Time.

---

## AI Support

Which AI Employees participate.

---

## Execution Plan

DIY

DWY

DFY

Recommended option with justification.

---

## Success Criteria

How success will be measured.

---

# Learning Loop

After execution PBOS records:

- actual Business Return
- actual Life Return
- actual Human Time
- actual AI contribution
- lessons learned

The Recommendation Engine continuously improves through this feedback.

---

# Core Principle

PBOS exists to protect the owner's Human Signature while maximizing Business Return and Life Return.

Recommendations that increase short-term revenue but erode Human Signature or violate the owner's Vision of Life should receive a lower priority.

Recommendations that compound knowledge, trust, and long-term capability should generally receive higher priority.

---

# Design Notes

The Recommendation Engine is the decision-making core of PBOS.

PBHS measures reality.

The Executive Board interprets reality.

The Recommendation Engine determines priorities.

AI Employees execute.

The Business Owner retains accountability.

---

# Future Evolution

Future versions may incorporate:

- predictive forecasting
- scenario simulation
- reinforcement learning from historical recommendations
- portfolio optimization across multiple business initiatives
- adaptive weighting based on changing Vision of Life
- collaborative recommendations across multiple AI Employees

---

# Changelog

## Version 0.1

Initial architecture of the PBOS Recommendation Engine.