from __future__ import annotations

import logging

from app.utils.openai_client import DEFAULT_MODEL, openai_client

logger = logging.getLogger(__name__)


def _generate_from_context(system_prompt: str, job_title: str, research_context: str) -> str:
    response = openai_client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"""
Job Title:
{job_title}

Research Context:
{research_context}
""",
            },
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM returned empty content.")

    return content


def extract_job_requirements(job_title: str, research_context: str) -> str:
    """
    Agent type: Analyzer.
    Extract the most important job requirements from research context.
    """
    logger.info("Extracting job requirements for: %s", job_title)

    return _generate_from_context(
        system_prompt=(
            "Extract the key job requirements from the research context. "
            "List the main technical skills, tools, responsibilities, and important knowledge areas."
        ),
        job_title=job_title,
        research_context=research_context,
    )


def generate_interview_questions(job_title: str, research_context: str) -> str:
    """
    Agent type: Interview simulator.
    Generate realistic interview questions for the target role.
    """
    logger.info("Generating interview questions for: %s", job_title)

    return _generate_from_context(
        system_prompt=(
            "Generate a realistic interview question list for the target job title. "
            "Include HR questions, technical questions, and situational questions."
        ),
        job_title=job_title,
        research_context=research_context,
    )


def generate_preparation_tips(job_title: str, research_context: str) -> str:
    """
    Agent type: Coach.
    Generate practical interview preparation tips.
    """
    logger.info("Generating preparation tips for: %s", job_title)

    return _generate_from_context(
        system_prompt=(
            "Generate practical interview preparation tips for this job title. "
            "Focus on study priorities, practice suggestions, and what to review before the interview."
        ),
        job_title=job_title,
        research_context=research_context,
    )

