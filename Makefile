GITCOMMIT := $(shell git rev-parse --short HEAD)

.PHONY: lint
lint:
	@pylint -j 4 --rcfile=.pylintrc ./pylox/*.py

.PHONY: test
test:
	python3 -m pytest tests

.PHONY: generate-ast
generate-ast:
	./generate_ast.py
