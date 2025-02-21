# Contribute to project
## Install development environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install --install-hooks
[[ ! -e .env ]] && cp .env.sample .env
```
Then, populate `.env` file with your api key.

## Tests
Launch tests
```bash
pytest
```
Record new HTTP request
```bash
pytest --record-mode=once
```
Force overwrite already recorded HTTP requests
```bash
pytest --record-mode=all  -k test_name tests/test_file.py
```
