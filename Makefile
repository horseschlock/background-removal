PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
PYTHONPATH ?= src
APP_MODULE = background_removal.api:app
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install run api cli test

install:
	$(PIP) install -r requirements.txt

run: api

api:
	PYTHONPATH=$(PYTHONPATH) uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

cli:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m background_removal.cli --help

test:
	PYTHONPATH=$(PYTHONPATH) pytest
