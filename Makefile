PYTHON := python3
PIP := pip3
TEST_COMMAND := pytest

.PHONY: install test clean

install:
    $(PIP) install -r requirements.txt

test:
    $(TEST_COMMAND)

clean:
    rm -rf __pycache__ *.pyc

run:
    $(PYTHON) main.py
