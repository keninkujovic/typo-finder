venv:
	python3 -m venv .venv
develop:
	pip install -r requirements.txt
server:
	uvicorn server:app --reload
