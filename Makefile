venv:
	uv venv
	source .venv/bin/activate
	uv sync


activate:
	source .venv/bin/activate

install:
	uv sync	

serve:
	chainlit run app.py -w

clean:
	rm -rf .venv/ __pycache__/ .chainlit/