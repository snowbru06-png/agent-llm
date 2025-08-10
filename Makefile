    .PHONY: dev fmt run

    dev:
    	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

    run:
    	uvicorn app.main:app --reload

    fmt:
    	python - <<'PY'
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'ruff'])
subprocess.run(['ruff', 'check', '--fix', '.'])
PY
