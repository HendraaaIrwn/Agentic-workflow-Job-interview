from __future__ import annotations

import logging

from app.modules.research.schema import QueriesSchema
from app.utils.openai_client import DEFAULT_MODEL, openai_client

logger = logging.getLogger(__name__)


def generate_queries(job_title: str) -> QueriesSchema:
    """
    Agent type: Planner.
    Generate exactly 5 web search queries for interview preparation.
    """
    logger.info("Generating queries for job title: %s", job_title)

    response = openai_client.beta.chat.completions.parse(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate exactly 5 useful web search queries for preparing a job interview "
                    "based on the given target job title."
                ),
            },
            {
                "role": "user",
                "content": f"Job title: {job_title}",
            },
        ],
        response_format=QueriesSchema,
    )

    parsed = response.choices[0].message.parsed
    if not parsed:
        raise ValueError("Failed to generate search queries.")

    return parsed

