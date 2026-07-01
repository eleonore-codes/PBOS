# PBOS Backend

## Purpose

FastAPI backend for the PBOS/PBHS MVP.

This M2 setup implements the persistence foundation for:

- User
- Business
- PBHS Assessment
- PBHS Question
- PBHS Response
- Evidence Item

Scoring, recommendations, executive reviews, owner decisions and executive reports are intentionally deferred.

## Run

```powershell
cd Implementation/Backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn pbos.main:app --reload
```

## Test

```powershell
cd Implementation/Backend
pytest
```
