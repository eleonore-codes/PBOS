---
id: PBOS-DB-001
title: PBOS MVP Database Schema
version: 0.1
status: Draft
stability: foundational

category: Database

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01
---

# PBOS MVP Database Schema

## Purpose

This document defines the minimum database schema required to implement the first functional version of PBOS.

The MVP focuses on validating the PBHS workflow rather than implementing the complete PBOS platform.

---

# MVP Scope

The MVP should support:

- User
- Business
- PBHS Assessment
- Capability Scores
- Recommendations
- Executive Report

Everything else can be added iteratively.

---

# Design Philosophy

The MVP database should be:

- simple
- normalized
- extensible
- migration-friendly
- domain-driven

Avoid premature optimization.

---

# Initial Tables

## Users

Purpose

Business Owners.

Primary fields

- UserID
- Name
- Email
- CreatedAt

---

## Businesses

Purpose

One PBOS instance.

Primary fields

- BusinessID
- UserID
- Name
- Industry
- VisionOfLifeVersion
- BusinessVisionVersion

---

## PBHS Assessments

Purpose

Store completed assessments.

Primary fields

- AssessmentID
- BusinessID
- AssessmentDate
- PBHSVersion
- OverallScore

---

## PBHS Responses

Purpose

Store answers to every PBHS question.

Primary fields

- ResponseID
- AssessmentID
- QuestionID
- ResponseValue

---

## Capability Scores

Purpose

Store calculated capability scores.

Primary fields

- CapabilityScoreID
- AssessmentID
- Capability
- Score

---

## Recommendations

Purpose

Store generated recommendations.

Primary fields

- RecommendationID
- AssessmentID
- Title
- Priority
- Confidence
- Risk

---

## Executive Reports

Purpose

Store executive summaries.

Primary fields

- ReportID
- AssessmentID
- GeneratedDate
- ReportVersion

---

# Relationships

```text
User
    │
    ▼
Business
    │
    ▼
Assessment
    ├── Responses
    ├── Capability Scores
    ├── Recommendations
    └── Executive Report
```

---

# Deferred Entities

The MVP intentionally excludes:

- Departments
- Operational AI Employees
- Projects
- Deliverables
- Objectives
- Initiatives

These will be introduced in later iterations.

---

# Guiding Principle

The MVP should answer one question exceptionally well:

> "What should this business improve next?"

Everything beyond that belongs to future releases.

---

# Success Criteria

The MVP is successful if a Business Owner can:

1. Complete a PBHS assessment.
2. Receive capability scores.
3. Receive prioritized recommendations.
4. Receive an Executive Report.
5. Decide on the next business improvement.

---

# Future Evolution

Future schema versions will introduce:

- Strategic Planning
- Executive Board
- Departments
- AI Employees
- Workflow Engine
- Knowledge Graph

---

# Status

Version: 0.1

Status: Active