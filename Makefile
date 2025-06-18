.PHONY: help build up down manage shell bash test test_fast

ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

# Default target, display available commands
help:
	@echo "Available commands:"
	@echo "  make build \n\t Build the Docker containers"
	@echo "  make up \n\t Start the Docker containers"
	@echo "  make stop \n\t Stop the Docker containers"
	@echo "  make bash \n\t Open a bash shell in the Django container"
	@echo "  make -- manage command [args] \n\t Run a Django management command"
	@echo "  make shell \n\t Open a shell_plus in Django container"
	@echo "  make -- test [args] [test_name] \n\t Run Django tests"

# FIXME: "ENV" doesn't sound like the best option here.
ENV = docker compose
DJANGO_ENV = $(ENV) run --rm app

build:
	${ENV} --progress plain build
up:
	${ENV} up
stop:
	${ENV} stop

bash:
	${DJANGO_ENV} bash
manage:
	${DJANGO_ENV} python manage.py $(ARGS)
shell:
	${DJANGO_ENV} python manage.py shell_plus
test:
	${DJANGO_ENV} pytest $(ARGS)
