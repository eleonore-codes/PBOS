---
id: PBOS-DM-100
title: PBOS Semantic Model
version: 1.0
status: Draft
stability: foundational

category: Domain Model

owner: PBOS Architecture

created: 2026-07-01
updated: 2026-07-01
---

# PBOS Semantic Model

## Purpose

The PBOS Semantic Model defines the canonical business vocabulary of the Personal Business Operating System (PBOS).

It serves as the authoritative reference for all business concepts used throughout the architecture.

Every subsystem, API, database model, AI Employee, dashboard and workflow should reference this model rather than redefining concepts independently.

---

# Mission

Provide a shared language for humans and AI.

The Semantic Model ensures that PBOS remains:

- consistent
- explainable
- modular
- implementable
- scalable

---

# Domain Architecture

```text
Vision of Life
        │
        ▼
Business Vision
        │
        ▼
Business
        │
        ▼
Recommendations
        │
        ▼
Objectives
        │
        ▼
Initiatives
        │
        ▼
Projects
        │
        ▼
Deliverables
```

Execution occurs through:

```text
Executive Board
        │
        ▼
Departments
        │
        ▼
Operational AI Employees
        │
        ▼
Business Assets
```

---

# Domain Layers

## Foundational Entities

- Vision of Life
- Business Vision

Purpose

Define why the business exists.

---

## Core Business Entity

- Business

Purpose

Represents the complete PBOS instance.

---

## Strategic Entities

- Recommendation
- Objective
- Initiative

Purpose

Transform evidence into strategic direction.

---

## Execution Entities

- Project
- Deliverable

Purpose

Transform strategy into reusable business assets.

---

## Organizational Entities

- Department
- Executive Agent
- Operational AI Employee

Purpose

Provide governance and execution capability.

---

# Value Objects

PBOS evaluates decisions using the following Value Objects.

## Optimization Values

- Business Return
- Life Return
- Human Signature
- Human Time

---

## Decision Values

- Confidence
- Risk
- Priority

---

# Aggregates

PBOS currently defines three Aggregates.

## Executive Board Aggregate

Responsible for strategic reasoning.

Aggregate Root

Executive Board

---

## Strategy Aggregate

Responsible for strategic planning.

Aggregate Root

Objective

---

## Department Aggregate

Responsible for operational execution.

Aggregate Root

Department

---

# Semantic Relationships

```text
Vision of Life
        │
        ▼
Business Vision
        │
        ▼
Business
        │
        ▼
Executive Board
        │
        ▼
Recommendation
        │
        ▼
Objective
        │
        ▼
Initiative
        │
        ▼
Project
        │
        ▼
Deliverable
```

Operational execution:

```text
Department
        │
        ▼
Operational AI Employee
        │
        ▼
Deliverable
```

---

# PBOS Optimization Model

Every Recommendation should improve one or more of:

- Business Return
- Life Return
- Human Signature

while reducing unnecessary Human Time.

These Value Objects form the optimization model of PBOS.

---

# Semantic Rules

The Semantic Model follows these principles:

- Every Entity has identity.
- Every Value Object is defined by its value.
- Every Aggregate has one Aggregate Root.
- Every Recommendation originates from evidence.
- Every Deliverable supports a Strategic Objective.
- Every Strategic Objective aligns with the Business Vision.
- Every Business Vision aligns with the Vision of Life.

---

# Intended Consumers

This document is intended for:

- Business Owner
- Executive Board
- Software Engineers
- AI Coding Agents
- API Designers
- Database Designers
- UI/UX Designers
- Contributors

---

# Architectural Principle

The Semantic Model is the single source of truth for PBOS terminology.

No subsystem should redefine concepts already specified in the Semantic Model.

---

# Future Evolution

Future versions may include:

- Domain Services
- Domain Events
- Bounded Contexts
- Context Maps
- Event Storming artifacts
- Ontology diagrams
- UML representations

---

# Status

Version: 1.0

Status: Foundational