# Changelog

# PBHS Core v1 Complete

PBHS Core v1 was completed with milestones M13–M17.

The system now provides a complete deterministic decision-support pipeline:

Assessment → Evidence → Capability Scores → Recommendation Engine

Subsequent milestones build governance, strategic execution, AI Employees, and organizational orchestration on top of this analytical core.



## M13 – PBHS MVP Project Setup

### Added

- FastAPI backend scaffold
- React/Vite frontend scaffold
- SQLite migration scaffold
- Shared TypeScript package scaffold
- Health endpoint
- OpenAPI documentation
- Initial pytest setup

### Verified

- Backend starts successfully
- `/health` returns HTTP 200
- OpenAPI documentation works
- pytest passes

### Deferred

- Domain persistence
- Assessment workflow
- Scoring
- Recommendations
- Executive reports

## M14 – PBHS MVP Domain Model and Persistence

### Added

- User domain model
- Business domain model
- Assessment domain model
- Question domain model
- Response domain model
- Evidence domain model
- Initial persistence layer
- Initial migrations
- Repository interfaces

### Deferred

- Scoring
- Recommendations
- Executive Board
- Reports

## M15 – PBHS MVP Assessment Engine

### Added

- Assessment question snapshots
- Draft-only response submission
- Response validation against snapshot
- Assessment progress tracking
- Submit and lock lifecycle
- Evidence provenance for self-report responses
- Assessment workflow API endpoints
- Assessment workflow tests

### Deferred

- Capability scoring
- Recommendations
- Executive Board
- Executive reports

## M16 – PBHS MVP Scoring Engine

**Version:** v0.4.0-m16

### Added

- Deterministic PBHS Scoring Engine
- Capability Score persistence
- Capability Score repository
- Likert (1–5) response normalization to a 0–100 scale
- Capability Score calculation for all eight PBHS capabilities
- Overall PBHS Summary Score calculation
- Questionnaire-only confidence calculation
- Capability maturity level classification (Levels 1–5)
- Evidence provenance for every Capability Score
- Assessment status transition from **Submitted** to **Scored**
- Idempotent scoring workflow
- Scoring API endpoints:
  - `POST /api/v1/assessments/{assessment_id}/score`
  - `GET /api/v1/assessments/{assessment_id}/scores`
- Database migration for Capability Scores and Assessment Summary fields

### Tests

- Likert normalization
- Capability Score calculation
- Overall PBHS Summary Score calculation
- Confidence calculation
- Maturity level classification
- Evidence provenance
- Snapshot-based scoring
- Assessment status transition
- Idempotent rescoring
- Draft assessment scoring rejection
- Scoring API endpoints

### Verification

- ✅ 14 automated backend tests passed
- ✅ Backend verification successful
- ✅ Evidence provenance preserved
- ⚠️ One upstream FastAPI/Starlette `httpx` deprecation warning remains (non-blocking)

### Deferred

- Recommendation Engine
- Executive Board
- Business Owner Decisions
- Executive Reports
- Strategy generation

### Project Status

Completed

- ✅ Backend foundation
- ✅ Domain model
- ✅ Persistence layer
- ✅ Assessment Engine
- ✅ Scoring Engine

Next milestone

- ▶️ M17 – Recommendation Engine

### Notes

M16 completes the deterministic PBHS Scoring Layer. PBOS can now transform questionnaire evidence into explainable Capability Scores, calculate an overall PBHS Summary Score, assign maturity levels, and preserve full evidence provenance for downstream decision making.

## M17 – PBHS MVP Recommendation Engine

**Version:** v0.5.0-m17

### Added

- Deterministic Recommendation Engine
- Rule → Recommendation Template → Recommendation Instance architecture
- Stable recommendation types:
  - `SPONSOR_READINESS`
  - `CONTENT_SYSTEM`
  - `EMAIL_FUNNEL`
  - `AUTOMATION`
  - `KNOWLEDGE_LIBRARY`
- Recommendation persistence
- Recommendation rule matching
- Recommendation templates
- Recommendation instances including:
  - Business Return estimation
  - Life Return estimation
  - Human Time estimation
  - Human Signature impact
  - Confidence calculation
  - Risk assessment
  - Priority calculation
  - Structured rationale
  - Calculation trace
  - Evidence provenance
- Recommendation API endpoints:
  - `POST /api/v1/assessments/{assessment_id}/recommendations`
  - Recommendation list
  - Recommendation detail
  - Recommendation explanation
  - Recommendation evidence
- Database migration for Recommendation persistence

### Changed

- Recommendation generation endpoint aligned with the canonical API specification.
- PBHS MVP Scoring now explicitly supports **Likert 1–5** response scales only.
- Added deterministic domain error:

  `pbhs_scoring_requires_likert_1_5_response_scale`

- Added regression tests ensuring unsupported response scales are rejected during scoring while remaining forward-compatible within the Assessment Engine.

### Tests

- Deterministic recommendation generation
- Rule matching
- Recommendation template instantiation
- Recommendation persistence
- Business Return estimation
- Life Return estimation
- Human Time estimation
- Human Signature impact
- Confidence calculation
- Risk calculation
- Priority calculation
- Evidence provenance
- Recommendation API endpoints
- Deterministic recommendation ordering
- Regression test for unsupported response scales

### Verification

- ✅ 20 automated backend tests passed
- ✅ Recommendation generation is deterministic
- ✅ Evidence provenance preserved end-to-end
- ✅ Recommendation rationale fully explainable
- ✅ API endpoints aligned with the PBHS API specification
- ⚠️ One upstream FastAPI/Starlette `httpx` deprecation warning remains (non-blocking)

### Deferred

- Executive Board
- Business Owner Decisions
- Executive Reports
- Strategy generation
- Recommendation Generation Run persistence
- Vision of Life–aware recommendation personalization
- Multi-source evidence weighting

### Project Status

Completed

- ✅ Backend foundation
- ✅ Domain model
- ✅ Persistence layer
- ✅ Assessment Engine
- ✅ Scoring Engine
- ✅ Recommendation Engine

Next milestone

- ▶️ M18 – Executive Board

### Notes

M17 completes the first fully deterministic PBHS decision-support pipeline:

**Assessment → Evidence → Capability Scores → Recommendation Engine**

PBOS can now generate reproducible, evidence-based recommendation candidates with complete provenance, structured rationale, expected Business Return, expected Life Return, Human Time estimates, Confidence, Risk, and Priority. Executive governance, Business Owner decisions, and strategic execution remain intentionally outside the scope of this milestone.

## M17.5 – PBHS Core v1 Contract Freeze

**Version:** v0.5.1-m17.5

### Added

- `Implementation/API/PBHS_API_v1.md`
- `Implementation/PBHS_Domain_Model_v1.md`
- `Implementation/PBHS_State_Machine_v1.md`
- `Implementation/PBHS_Core_v1_Architecture_Summary.md`

### Purpose

Established the canonical PBHS Core v1 implementation contract after completion of M13–M17.

The documentation freezes the implemented API, domain model, lifecycle, and architectural boundaries before beginning governance features.

### Scope

Documented:

- Public REST API
- Implemented domain model
- Assessment and recommendation lifecycle
- Implemented pipeline
- Deferred scope
- Known technical debt
- Extension points for M18+

### Verification

Documentation only.

No implementation code changed.

### Next milestone

▶️ M18 – Executive Board

## M17.6 – Founder Dashboard (Frontend MVP)

### Added
- First Founder Dashboard implemented using React/Vite/TypeScript.
- Executive dashboard layout with left navigation.
- CreatingReorganized branding applied using:
  - Blue `#335f9f`
  - Gold `#e9b25d`
- Logo integrated using repository-local SVG fallback.
- Dashboard includes:
  - PBHS Score hero card
  - Business Return
  - Life Return
  - Confidence
  - Assessment Status
  - Eight capability overview cards
  - Radar visualization
  - Weakest/Strongest capability
  - Top 3 recommendations
  - Human Time
  - Recent Activity
  - Recommendation detail panel

### API
- Consumes PBHS Core v1 endpoints.
- Recommendation endpoint aligned with canonical API:
  - `POST /api/v1/assessments/{assessment_id}/recommendations`

### Notes
- Uses labelled demo data when no assessment is supplied.
- Supports loading live PBHS Core v1 data through the implemented REST API.
- No backend changes introduced.

### Deferred
- Production logo asset.
- Historical trends.
- Executive Board.
- Strategy.
- Departments.
- AI Employees.

## M17.7 – Founder Dashboard UX Polish

### Improved
- Enlarged CreatingReorganized logo and added product subtitle.
- Increased prominence of the Overall PBHS Score.
- Enlarged radar chart for improved readability.
- Added professional SVG icons to sidebar navigation.
- Added SVG icons to KPI cards.
- Added Human Time KPI derived from recommendation data.
- Added subtle capability color coding based on operating health.

### Notes
- Frontend-only UX improvements.
- No backend changes.
- No API changes.
- No PBHS data model changes.
