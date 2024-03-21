SHELL := /bin/bash
.ONESHELL:

.PHONY: install run run-detailed

INPUT?=data_sample/example.csv

install:
	python3 -m venv .venv
	. ./.venv/bin/activate
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	. ./.venv/bin/activate
	python main.py -i data_sample/example.csv

run-detailed:
	. ./.venv/bin/activate
	python main.py -i ${INPUT} -d

run-debug:
	. ./.venv/bin/activate
	export LOGLEVEL=DEBUG; python main.py -i data_sample/example.csv
