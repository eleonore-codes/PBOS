---
id: PBOS-000
title: PBOS Repository Map
version: 0.1
status: Active
stability: evolving

category: Repository

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01
---

# PBOS Repository Map

## Purpose

This document serves as the master navigation guide for the PBOS repository.

It provides an architectural overview of every major subsystem, their responsibilities, maturity, relationships and intended evolution.

All contributors—human and AI—should use this document as the primary entry point into the repository.

---

# PBOS Architectural Vision

PBOS (Personal Business Operating System) is an AI-native executive operating system.

Its purpose is to help business owners make better strategic decisions, organize execution and continuously improve Business Return and Life Return according to their Vision of Life.

---

# Repository Architecture

```text
PBOS
│
├── Foundation
├── Architecture
├── Business
├── Product
├── Customer_Zero          (planned)
├── Data                   (planned)
├── Interfaces             (planned)
├── Implementation         (planned)
├── Tests                  (planned)
└── Docs                   (planned)
```

---

# Foundation

Purpose

Defines the philosophy and fundamental principles of PBOS.

Typical contents

- Vision
- Principles
- Human Signature
- ADRs
- Core Concepts

Status

✅ Stable

---

# Architecture

Purpose

Defines how PBOS thinks, reasons and operates.

Subsystems

```text
Architecture

├── Domain_Model
├── Recommendation_Engine
├── Executive_Board
├── Decision_Framework
├── Strategy
└── Departments
```

Status

🚧 Growing

---

## Domain Model

Purpose

Defines the core business entities used throughout PBOS.

Status

✅ Stable

---

## Recommendation Engine

Purpose

Transforms PBHS findings into candidate recommendations.

Status

🚧 Growing

---

## Executive Board

Purpose

Provides multidisciplinary strategic reasoning through Executive Agents.

Status

🚧 Growing

---

## Decision Framework

Purpose

Defines the canonical reasoning model used by every Executive Agent.

Status

🚧 Growing

---

## Strategy

Purpose

Transforms executive decisions into strategic objectives, initiatives, roadmaps and portfolios.

Status

🚧 Growing

---

## Departments

Purpose

Defines operational departments responsible for execution.

Current Reference Department

```text
Marketing Department
```

Future Departments

- Sales
- Content
- Operations
- Finance
- Knowledge
- AI
- Customer Success

Status

🚧 Reference Implementation

---

# Business

Purpose

Defines the business concepts represented inside PBOS.

Examples

- Company
- Business Model
- Human Signature
- Value Engine
- Recommendation Engine

Status

✅ Stable

---

# Product

Purpose

Defines user-facing PBOS products.

Current Product

```text
PBHS
```

Future Products

- Executive Dashboard
- Recommendation Workspace
- Strategy Workspace
- Portfolio Dashboard

Status

🚧 Growing

---

# Planned Repository Areas

## Customer_Zero

Purpose

Reference implementation using CreatingReorganized.

Examples

- real business data
- workflows
- KPIs
- recommendations

---

## Data

Purpose

Domain objects and persistence model.

Future

- entities
- schemas
- relationships
- migrations

---

## Interfaces

Purpose

External interfaces.

Examples

- REST API
- MCP
- Integrations
- Events

---

## Implementation

Purpose

Executable PBOS platform.

Future

- Backend
- Frontend
- AI Services
- Infrastructure

---

## Tests

Purpose

Architecture validation.

Examples

- Unit Tests
- Integration Tests
- Decision Tests
- Recommendation Tests

---

## Docs

Purpose

Developer documentation.

Examples

- tutorials
- examples
- coding standards
- onboarding

---

# PBOS Intelligence Stack

```text
Vision Layer
────────────────────────
Vision of Life
Business Vision

↓

Assessment Layer
────────────────────────
PBHS

↓

Recommendation Layer
────────────────────────
Recommendation Engine

↓

Decision Layer
────────────────────────
Decision Framework
Executive Board

↓

Strategy Layer
────────────────────────
Objectives
Initiatives
Roadmaps
Portfolio

↓

Execution Layer
────────────────────────
Departments
Operational AI Employees

↓

Learning Layer
────────────────────────
Measurement
Continuous Improvement
```

---

# Repository Maturity

| Area | Status |
|-------|--------|
| Foundation | ✅ Stable |
| Architecture | 🚧 Growing |
| Business | ✅ Stable |
| Product | 🚧 Growing |
| PBHS | ✅ Stable |
| Recommendation Engine | 🚧 Growing |
| Executive Board | 🚧 Growing |
| Decision Framework | 🚧 Growing |
| Strategy | 🚧 Growing |
| Departments | 🚧 Reference Implementation |
| Operational AI Employees | ⏳ Planned |
| Data Model | ⏳ Planned |
| APIs | ⏳ Planned |
| UI | ⏳ Planned |
| Customer Zero | ⏳ Planned |

---

# Architectural Principles

PBOS follows these principles:

- Vision before Strategy
- Strategy before Execution
- Evidence before Opinion
- Human Signature before Automation
- Business Return and Life Return together
- Explainability over opacity
- Reusable assets over one-time outputs
- Continuous learning through feedback

---

# Recommended Reading Order

For new contributors:

1. README.md
2. REPOSITORY_MAP.md
3. Foundation
4. Business
5. Architecture
6. Product
7. Customer Zero (when available)
8. Implementation (when available)

---

# Long-Term Vision

PBOS will evolve from a structured architecture repository into an executable AI-native business operating system.

Every subsystem should remain:

- modular
- explainable
- testable
- reusable
- scalable

---

# Changelog

## Version 0.1

Initial repository architecture map.