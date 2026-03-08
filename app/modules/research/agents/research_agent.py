from __future__ import annotations

import logging

from app.modules.research.agents.query_agent import generate_queries
from app.utils.openai_client import DEFAULT_MODEL, openai_client
from app.utils.tavily_client import tavily_client

logger = logging.getLogger(__name__)


def search_web(query: str) -> str:
    """
    Agent type: Researcher.
    Search the web using Tavily and summarize results into research notes.
    """
    logger.info("Searching web for query: %s", query)

    result = tavily_client.search(
        query=query,
        search_depth="advanced",
        include_raw_content=True,
        max_results=5,
    )

    response = openai_client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize these search results into useful interview preparation notes. "
                    "Focus on job requirements, skills, tools, responsibilities, and interview topics."
                ),
            },
            {
                "role": "user",
                "content": str(result),
            },
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Failed to summarize web search result.")

    return content


def build_research_context(job_title: str) -> str:
    """
    Agent type: Research orchestrator.
    Generate queries, search them one by one, and combine to one context.
    """
    logger.info("Building research context for job title: %s", job_title)

    queries = generate_queries(job_title)
    research_context = ""

    for index, query in enumerate(queries.queries, start=1):
        logger.info("Processing query %s/%s: %s", index, len(queries.queries), query)
        summarized_result = search_web(query)
        research_context += f"Query: {query}\n{summarized_result}\n\n"

    return research_context

