.PHONY: lint, fix_lint, setup, test

lint:
	cd lib_src/ && find . -type f -name "*.py" | xargs pylint


fix_lint:
	cd lib_src/ && find . -type f -name "*.py" | xargs autopep8 --in-place --aggressive --aggressive

setup:
	. venv/bin/activate && pipenv install

test: setup
	pytest
