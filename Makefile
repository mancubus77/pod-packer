SHELL := /bin/bash
.ONESHELL:

.PHONY: run run_detailed

run:
	ls -la
	. ./.venv-py-39/bin/activate
	python main.py -i data_sample/example.csv

run_detailed:
	ls -la
	. ./.venv-py-39/bin/activate
	python main.py -i data_sample/example.csv
