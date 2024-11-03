# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# MAKEFILE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# General variables
PYTHON = python3
VENV_DIR = .venv
PYTEST_CMD = python -m pytest -vv -rfEsP --maxfail=1 --tb=long --color=yes --code-highlight=yes
PYTEST_CMD_WITH_THREADING = $(PYTEST_CMD) -n 5

.PHONY: help run test install-lint update-lint lint lint-all clean clean-build clean-pyc clean-lint clean-test create-migrations apply-migrations import-data truncate-tables

help:
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "RUN"
	@echo "  run                            run the Django app locally"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "TEST"
	@echo "  test                           run all unit and integration tests"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "LINT"
	@echo "  install-lint                   install python linting tools"
	@echo "  update-lint                    update python linting tools"
	@echo "  lint                           run autopep8, ruff, black and other linting tools on staged files"
	@echo "  lint-all                       run autopep8, ruff, black and other linting tools on the entire repo"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "CLEAN"
	@echo "  clean                          clean build, test, coverage, python artifacts and AWS outputs"
	@echo "  clean-build                    clean python build artifacts"
	@echo "  clean-pyc                      clean python file artifacts"
	@echo "  clean-lint                     clean python file artifacts"
	@echo "  clean-test                     clean python test and coverage artifacts"
	@echo "-----------------------------------------------------------------------------------------------------------"
	@echo "DATABASE"
	@echo "  create-migrations              create the database migration files from the model files"
	@echo "  apply-migrations               apply the database migration files from the model files"
	@echo "  import-data                    import D0010 flow files"
	@echo "  truncate-tables                truncate all database tables"
	@echo "  create-superuser               create superuser for database"

# -------------------------------------------------------------------------------------------------
# Run commands
# -------------------------------------------------------------------------------------------------
run:
	python manage.py runserver

# -------------------------------------------------------------------------------------------------
# Test commands
# -------------------------------------------------------------------------------------------------
test:
	pytest

# -------------------------------------------------------------------------------------------------
# Lint commands
# -------------------------------------------------------------------------------------------------
# Set up the git hook scripts
install-lint:
	pip install pre-commit
	pre-commit install

# Update version numbers of each pre-commit hook
update-lint:
	pre-commit autoupdate

# Run pre-commit hooks on staged files
# Note: you can run a specific pre-commit by doing:
# `pre-commit run black`
# Note: if you want to run ruff (isort module) manually:
# `ruff check --select I .`
# See docs/fond-dev-guide/content/lint for more.
lint:
	pre-commit run

# Run pre-commit hooks on entire repo
lint-all:
	pre-commit run -a

# -------------------------------------------------------------------------------------------------
# Clean commands
# -------------------------------------------------------------------------------------------------
# Remove all build, test, coverage and python artifacts.
clean: clean-build clean-pyc clean-lint clean-test

# Remove build artifacts
clean-build:
	find . -name '.eggs' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# Remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# Remove lint artifacts
clean-lint:
	find . -name '.ruff_cache' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +

# Remove test and coverage artifacts
clean-test:
	find . -name '.pytest_cache' -exec rm -fr {} +

# -------------------------------------------------------------------------------------------------
# Database commands
# -------------------------------------------------------------------------------------------------
create-migrations:
	python manage.py makemigrations

apply-migrations:
	python manage.py migrate

import-data:
	python manage.py import_d0010_files ../data

truncate-tables:
	python manage.py truncate_all_tables

create-superuser:
	python manage.py createsuperuser
