from __future__ import annotations

import logging
from pathlib import Path

from markdown import markdown

from app.utils.openai_client import REPORT_MODEL, openai_client

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_report_as_markdown(job_title: str, report_markdown: str) -> str:
    """
    Persist report content as Markdown.
    """
    safe_filename = job_title.lower().replace(" ", "_").replace("/", "_")
    markdown_path = OUTPUT_DIR / f"{safe_filename}_interview_report.md"
    markdown_path.write_text(report_markdown, encoding="utf-8")
    return str(markdown_path)


def generate_final_report(
    job_title: str,
    requirements_text: str,
    questions_text: str,
    tips_text: str,
) -> str:
    """
    Agent type: Writer.
    Combine analysis outputs into a final Markdown report.
    """
    logger.info("Generating final report for: %s", job_title)

    response = openai_client.chat.completions.create(
        model=REPORT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Write a complete interview preparation report in Markdown format. "
                    "Use clear headings, bullet points, and a short conclusion."
                ),
            },
            {
                "role": "user",
                "content": f"""
Create an interview preparation report.

Job Title:
{job_title}

Job Requirements:
{requirements_text}

Interview Questions:
{questions_text}

Preparation Tips:
{tips_text}
""",
            },
        ],
    )

    report = response.choices[0].message.content
    if not report:
        raise ValueError("Failed to generate final report.")

    return report


def save_report_as_pdf(job_title: str, report_markdown: str) -> str:
    """
    Agent type: Publisher.
    Convert Markdown report into PDF.
    Falls back to Markdown if PDF export is unavailable.
    """
    logger.info("Saving PDF report for: %s", job_title)

    try:
        # Lazy import to avoid import-time crashes on machines lacking system
        # dependencies when PDF generation is not used.
        from weasyprint import HTML

        safe_filename = job_title.lower().replace(" ", "_").replace("/", "_")
        pdf_path = OUTPUT_DIR / f"{safe_filename}_interview_report.pdf"

        html_content = markdown(report_markdown)
        HTML(string=html_content).write_pdf(str(pdf_path))
        return str(pdf_path)

    except Exception as error:
        logger.exception(
            "PDF export failed for '%s'. Falling back to Markdown. Error: %s",
            job_title,
            error,
        )
        return save_report_as_markdown(job_title, report_markdown)
