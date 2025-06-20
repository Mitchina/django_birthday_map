IN_CONTAINER := path_exists("/.dockerenv")
COMPOSE_CMD := "docker compose"
DJANGO_CMD := if IN_CONTAINER == "true" { "" } else { COMPOSE_CMD + " run --rm app" }

# List available commands
default:
    @just --list --unsorted

# Build the Docker containers
[group("compose")]
build *ARGS:
    {{ COMPOSE_CMD }} --progress plain build {{ ARGS }}

# Start the Docker containers
[group("compose")]
up *ARGS:
    {{ COMPOSE_CMD }} up {{ ARGS }}

# Stop the Docker containers
[group("compose")]
stop *ARGS:
    {{ COMPOSE_CMD }} stop {{ ARGS }}

# Open a bash shell in the Django container
[group("django")]
bash:
    {{ DJANGO_CMD }} bash

# Run a Django management command
[group("django")]
manage *ARGS:
    {{ DJANGO_CMD }} python manage.py {{ ARGS }}

# Open a shell_plus in Django container
[group("django")]
shell:
    {{ DJANGO_CMD }} python manage.py shell_plus

# Run Django tests
[group("django")]
test *ARGS:
    {{ DJANGO_CMD }} pytest {{ ARGS }}
