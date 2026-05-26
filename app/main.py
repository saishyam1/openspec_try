"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query

app = FastAPI(title="SDD Workshop — Reports API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def landing_page() -> HTMLResponse:
    return HTMLResponse(
        """
        <!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8' />
            <meta name='viewport' content='width=device-width, initial-scale=1.0' />
            <title>Sai Shyam — Vibe Coding</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 2rem; background: #f4f7fb; color: #1f2937; }
                .page { max-width: 860px; margin: 0 auto; background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08); }
                h1 { margin-top: 0; color: #0f172a; }
                h2 { color: #1e3a8a; }
                .badge { display: inline-block; margin-top: 0.75rem; padding: 0.35rem 0.75rem; background: #e0f2fe; color: #0369a1; border-radius: 999px; font-size: 0.95rem; font-weight: 600; }
                section { margin-top: 1.5rem; }
                ul { margin: 0.75rem 0 0 1.5rem; line-height: 1.8; }
                a { color: #0369a1; text-decoration: none; }
                a:hover { text-decoration: underline; }
                code { background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.9rem; }
            </style>
        </head>
        <body>
            <div class='page'>
                <h1>Sai Shyam — Vibe Coding 🚀</h1>
                <div class='badge'>Reports API · FastAPI · Python-first</div>
                <p>Built fast. No overthinking. Just clean, working code powered by FastAPI and Pydantic.</p>

                <section>
                    <h2>What's this?</h2>
                    <p>A paginated <strong>Reports API</strong> with filtering, sorting, and a <code>rating_for_vibecoding</code> field — because why not rate how vibe-coded each report is.</p>
                </section>

                <section>
                    <h2>Endpoints</h2>
                    <ul>
                        <li><a href='/health'><code>GET /health</code></a> — liveness probe</li>
                        <li><a href='/reports'><code>GET /reports</code></a> — paginated reports list</li>
                        <li><a href='/docs'><code>GET /docs</code></a> — auto-generated Swagger UI</li>
                    </ul>
                </section>

                <section>
                    <h2>Try it</h2>
                    <ul>
                        <li><code>GET /reports?limit=5</code></li>
                        <li><code>GET /reports?status=approved&amp;sort=amount&amp;descending=true</code></li>
                        <li><code>GET /reports?sort=rating_for_vibecoding&amp;descending=false&amp;limit=10</code></li>
                    </ul>
                </section>

                <section>
                    <h2>Run locally</h2>
                    <p><code>pip install -e . &amp;&amp; uvicorn app.main:app --reload --port 8000</code></p>
                </section>
            </div>
        </body>
        </html>
        """
    )


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> ReportListResponse:
    """Return a paginated list of reports.

    Public fields only — `internal_id` and `owner_email` are stripped via
    `ReportPublic.from_internal`.
    """
    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    page = rows[offset : offset + limit]
    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )
