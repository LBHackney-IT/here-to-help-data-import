.PHONY: lint,

lint:
	cd lib_src/ && find . -type f -name "*.py" | xargs pylint


fix_lint:
	cd lib_src/ && find . -type f -name "*.py" | xargs autopep8 --in-place --aggressive --aggressive
