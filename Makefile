.PHONY: setup test run clean docker-build docker-run

PYTHON := python3

setup:
	$(PYTHON) -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp -n .env.example .env || true
	@echo "Setup complete. Don't forget to add your OpenAI API key to .env"

test:
	. venv/bin/activate && pytest

run:
	. venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t o1a-visa-assessment .

docker-run:
	docker run -p 8000:8000 --env-file .env o1a-visa-assessment 