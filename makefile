SHELL := /bin/bash

.PHONY: help doc test clean

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "    doc     (Make documentation)"
	@echo "    test    (Execute tests)"
	@echo "    clean   (Remove temporary files)"

doc:
	cd ./docs; make

test:
	python run_tests.py

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


