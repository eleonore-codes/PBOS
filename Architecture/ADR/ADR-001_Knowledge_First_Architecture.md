---
id: PBOS-ADR-001
title: Knowledge-First Architecture
version: 1.0
status: Accepted
owner: PBOS Architecture
category: Architecture Decision Record
created: 2026-06-30
updated: 2026-06-30
---

# ADR-001 – Knowledge-First Architecture

## Status

Accepted

---

## Context

PBOS is intended to become:

- a business methodology
- a software platform
- a consulting framework
- a certification program
- an AI-powered operating system

These products must evolve from a single, coherent source of truth.

---

## Decision

PBOS adopts a Knowledge-First Architecture.

The knowledge architecture is the primary product.

Software, AI Employees, workshops, documentation and commercial offerings are implementations of that knowledge.

---

## Consequences

All PBOS artifacts must exist as canonical knowledge before they are implemented.

Every concept has exactly one canonical definition.

Software never defines business concepts.

Software implements business concepts.

---

## Rationale

This approach enables:

- consistent terminology
- reusable intellectual property
- traceable architectural decisions
- AI reasoning over the complete knowledge base
- independent evolution of software implementations

---

## Related Principles

- One concept → one canonical document.
- Foundation is independent of software.
- Architecture depends on Foundation.
- Commercial offerings depend on Architecture.
- Software implements Architecture.

---

## Decision

Accepted as the first architectural decision of PBOS.
