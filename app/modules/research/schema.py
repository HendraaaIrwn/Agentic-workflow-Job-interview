from pydantic import BaseModel, Field
from typing import List


class QueriesSchema(BaseModel):
    queries: List[str] = Field(
        description="List of search queries generated from the target job title."
    )


class InterviewPrepRequest(BaseModel):
    topic: str = Field(description="Topic for the interview prep.")