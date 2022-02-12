SHELL := /bin/bash
.ONESHELL:

.PHONY: run run_detailed

install:
	python3 -m venv .venv
	. ./.venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	. ./.venv/bin/activate
	python main.py -i data_sample/example.csv
