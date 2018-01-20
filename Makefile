.PHONY: all

init:
ifdef PIPENV_ACTIVE
	pipenv install
else
	@echo "Run 'pipenv shell' first." ;
	@exit 1
endif

lint: init
	flake8 lib support tests

test: init
	pytest tests

all: lint test
