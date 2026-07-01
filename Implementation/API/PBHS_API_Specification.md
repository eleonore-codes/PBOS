---
id: PBOS-API-001
title: PBHS API Specification
version: 0.1
status: Draft
stability: foundational

category: API

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01
---

# PBHS API Specification

## Purpose

This document defines the initial API surface required for the PBHS MVP.

The API enables a Business Owner to create a business, complete an assessment, receive capability scores, receive recommendations and view an executive report.

---

# API Design Principles

The PBHS API should be:

- simple
- RESTful
- domain-driven
- explainable
- versioned
- testable

---

# Base Path

```text
/api/v1
```

---

# Core Resources

## Users

Represents the Business Owner.

---

## Businesses

Represents the PBOS business instance.

---

## Assessments

Represents a PBHS assessment session.

---

## Responses

Represents answers to PBHS questions.

---

## Capability Scores

Represents calculated PBHS capability scores.

---

## Recommendations

Represents generated recommendations.

---

## Executive Reports

Represents the final PBHS report.

---

# MVP Endpoints

## Create Business

```http
POST /api/v1/businesses
```

Creates a new business profile.

---

## Get Business

```http
GET /api/v1/businesses/{business_id}
```

Returns business profile data.

---

## Start Assessment

```http
POST /api/v1/businesses/{business_id}/assessments
```

Creates a new PBHS assessment.

---

## Submit Assessment Responses

```http
POST /api/v1/assessments/{assessment_id}/responses
```

Stores questionnaire responses.

---

## Calculate Scores

```http
POST /api/v1/assessments/{assessment_id}/score
```

Calculates capability scores and overall PBHS summary.

---

## Generate Recommendations

```http
POST /api/v1/assessments/{assessment_id}/recommendations
```

Generates prioritized recommendations.

---

## Generate Executive Report

```http
POST /api/v1/assessments/{assessment_id}/report
```

Generates the PBHS Executive Report.

---

## Get Executive Report

```http
GET /api/v1/reports/{report_id}
```

Returns the generated report.

---

# Assessment Flow

```text
Create Business
        ↓
Start Assessment
        ↓
Submit Responses
        ↓
Calculate Scores
        ↓
Generate Recommendations
        ↓
Generate Executive Report
        ↓
Display Dashboard
```

---

# Initial Data Objects

## Business

```json
{
  "business_id": "string",
  "name": "string",
  "industry": "string",
  "created_at": "datetime"
}
```

---

## Assessment

```json
{
  "assessment_id": "string",
  "business_id": "string",
  "version": "0.1",
  "status": "draft | completed | scored | reported",
  "created_at": "datetime"
}
```

---

## Response

```json
{
  "question_id": "string",
  "value": 1
}
```

---

## Capability Score

```json
{
  "capability": "Human Signature",
  "score": 82,
  "confidence": 0.74
}
```

---

## Recommendation

```json
{
  "recommendation_id": "string",
  "title": "string",
  "priority": "High",
  "confidence": 0.82,
  "expected_business_return": "High",
  "expected_life_return": "Medium"
}
```

---

# Error Handling

Errors should return:

```json
{
  "error": "string",
  "message": "string",
  "details": {}
}
```

---

# Authentication

Authentication is required for all endpoints.

MVP authentication may be simple user authentication.

Future versions may support:

- OAuth
- organization accounts
- role-based permissions
- API keys

---

# Future API Areas

Future versions may include:

- Executive Board API
- Strategy API
- Department API
- AI Employee API
- Portfolio API
- Workflow API

---

# Architectural Principle

The API should expose PBOS domain concepts directly.

API design should follow the Domain Model rather than generic application structures.

---

# Status

Version: 0.1

Status: Active