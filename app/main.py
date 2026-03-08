import logging

from fastapi import FastAPI
from app.modules.research.schema import InterviewPrepRequest
from app.modules.research.task import interview_prep_task

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Interview Preparation Agent")


@app.get("/")
def root():
    return {"message": "AI Interview Preparation Agent is running"}


@app.post("/interview-prep")
def start_interview_prep(body: InterviewPrepRequest):
    task = interview_prep_task.delay(body.topic)  # type: ignore[attr-defined]

    return {
        "message": "Interview preparation task submitted",
        "task_id": task.id,
        "topic": body.topic,
    }