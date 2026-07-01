# PBHS Backend

## Purpose

FastAPI backend skeleton for the PBHS MVP.

This M1 setup creates the application boundaries only:

- REST API layer
- application/domain service layer
- persistence layer
- configuration layer
- tests

Business logic, scoring, recommendations and report generation start in later milestones.

## Run

```powershell
cd Implementation/Backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn pbhs_backend.main:app --reload
```

## Test

```powershell
cd Implementation/Backend
pytest
```
