# Database

## Purpose

The Database folder defines how the PBOS Domain Model will be persisted.

It translates Entities, Value Objects and Aggregates into implementation-ready data structures.

---

# Mission

Create a database architecture that preserves the semantic integrity of PBOS.

The database should reflect the Domain Model rather than force the Domain Model into generic tables.

---

# Source of Truth

The primary source for database design is:

```text
Architecture/Domain_Model/
```

---

# PBHS MVP Setup

M1 creates the migration location only. Tables are intentionally deferred until persistence behavior enters scope, so schema changes can follow the PBHS MVP data contract directly.

## Structure

- `migrations/` contains ordered SQL migrations.
