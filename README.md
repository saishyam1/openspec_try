# Reports API — Vibe Coded 🚀

A FastAPI service exposing a paginated `/reports` endpoint with filtering, sorting, and pagination — built vibe-coding style.

## Layout

```
app/
├── __init__.py
├── data.py        # Seed dataset (120 rows, deterministic)
├── models.py      # Pydantic models — internal vs public
├── reports.py     # Filter / sort / pagination query layer
└── main.py        # FastAPI HTTP layer + landing page
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

| Method | Path       | Description                            |
| ------ | ---------- | -------------------------------------- |
| GET    | `/`        | Landing page                           |
| GET    | `/health`  | `{"status": "ok"}`                     |
| GET    | `/reports` | Paginated reports with filter + sort   |
| GET    | `/docs`    | Swagger UI                             |

## `/reports` query params

| Param        | Type           | Default      | Notes                                                              |
| ------------ | -------------- | ------------ | ------------------------------------------------------------------ |
| `status`     | enum           | —            | `pending`, `approved`, `rejected`, `archived`                      |
| `date_from`  | datetime (ISO) | —            | Lower bound on `created_at` (inclusive)                            |
| `date_to`    | datetime (ISO) | —            | Upper bound on `created_at` (inclusive)                            |
| `sort`       | string         | `created_at` | `id`, `title`, `status`, `owner`, `amount`, `rating_for_vibecoding`, `created_at` |
| `descending` | bool           | `true`       | Sort direction                                                     |
| `offset`     | int (>=0)      | `0`          | Pagination offset                                                  |
| `limit`      | int (1..200)   | `20`         | Page size                                                          |
