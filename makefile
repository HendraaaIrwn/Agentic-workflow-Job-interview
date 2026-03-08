dev :
	uv run uvicorn app.main:app --reload

celery :
	uv run celery -A app.celery_app:celery_app worker --loglevel=info
	
test_local:
	python test_local.py
