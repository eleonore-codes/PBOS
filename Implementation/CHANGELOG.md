# Changelog

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