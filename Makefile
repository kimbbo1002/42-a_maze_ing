PYTHON = poetry run python3
MAIN = a_maze_ing.py
CONFIG = config.txt
VENV = .venv

install:
	poetry install

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . --explicit-package-bases --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --explicit-package-bases --strict

clean:
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf .mypy_cache

fclean: clean
	rm -rf output.txt
	rm -rf $(VENV)
	rm -rf poetry.lock
	rm -rf dist
	rm -rf mazegen-1.0.0-py3-none-any.whl

build:
	poetry build
	cp dist/mazegen-1.0.0-py3-none-any.whl ./
	rm -rf dist


.PHONY: install run debug clean lint lint-strict fclean build