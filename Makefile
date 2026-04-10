POETRY = poetry
PYTHON = $(POETRY) run python
MAIN = main.py
CONFIG = config.txt


install:
	$(POETRY) install

run:
	$(PYTHON) $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

.PHONY: install run clean