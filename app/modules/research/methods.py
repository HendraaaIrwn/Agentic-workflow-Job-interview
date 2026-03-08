from __future__ import annotations

"""
Compatibility facade for research workflow methods.

The implementation is split by agent type under `app.modules.research.agents`.
This module re-exports the previous API to avoid breaking existing imports.
"""

from app.modules.research.agents.analysis_agent import (
    extract_job_requirements,
    generate_interview_questions,
    generate_preparation_tips,
)
from app.modules.research.agents.query_agent import generate_queries
from app.modules.research.agents.report_agent import (
    generate_final_report,
    save_report_as_pdf,
)
from app.modules.research.agents.research_agent import (
    build_research_context,
    search_web,
)
from app.modules.research.workflow import run_interview_prep_workflow

__all__ = [
    "generate_queries",
    "search_web",
    "build_research_context",
    "extract_job_requirements",
    "generate_interview_questions",
    "generate_preparation_tips",
    "generate_final_report",
    "save_report_as_pdf",
    "run_interview_prep_workflow",
]

