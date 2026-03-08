from __future__ import annotations

import logging
from pathlib import Path

from app.modules.research.agents.analysis_agent import (
    extract_job_requirements,
    generate_interview_questions,
    generate_preparation_tips,
)
from app.modules.research.agents.report_agent import (
    generate_final_report,
    save_report_as_pdf,
)
from app.modules.research.agents.research_agent import build_research_context

logger = logging.getLogger(__name__)


def run_interview_prep_workflow(job_title: str) -> dict:
    """
    Full workflow:
    job title -> queries -> web search -> research context
    -> requirements -> interview questions -> preparation tips
    -> final report -> pdf (fallback to markdown)
    """
    logger.info("Starting interview preparation workflow")

    research_context = build_research_context(job_title)
    requirements_text = extract_job_requirements(job_title, research_context)
    questions_text = generate_interview_questions(job_title, research_context)
    tips_text = generate_preparation_tips(job_title, research_context)
    final_report = generate_final_report(
        job_title=job_title,
        requirements_text=requirements_text,
        questions_text=questions_text,
        tips_text=tips_text,
    )
    report_path = save_report_as_pdf(job_title, final_report)
    report_format = Path(report_path).suffix.lstrip(".").lower()

    logger.info("Interview preparation workflow finished successfully")

    return {
        "job_title": job_title,
        "research_context": research_context,
        "requirements": requirements_text,
        "questions": questions_text,
        "tips": tips_text,
        "report": final_report,
        # Backward-compatible key. May hold a .md path when PDF export fails.
        "pdf_path": report_path,
        "report_path": report_path,
        "report_format": report_format,
    }
