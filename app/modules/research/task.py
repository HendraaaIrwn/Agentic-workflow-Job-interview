import logging

from app.celery_app import celery_app
from app.modules.research.methods import run_interview_prep_workflow

logger = logging.getLogger(__name__)


@celery_app.task
def interview_prep_task(topic: str) -> dict:
    logger.info("Starting Celery task for topic: %s", topic)
    result = run_interview_prep_workflow(topic)
    logger.info("Finished Celery task for topic: %s", topic)
    return result