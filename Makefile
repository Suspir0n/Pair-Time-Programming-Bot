# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
SHELL := /bin/bash

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

SOURCE_PATH=${PWD}/venv/bin/activate
configure-dependencies: ## Configure dependencies to run server
	source ${SOURCE_PATH}

PORT = 5000
run-server: ## Run Server without dependencies
	FLASK_APP=src flask run --host=127.0.0.1 --port=${PORT}

run-server-with-dependencies: configure-dependencies run-server ## Run server and configure dependencies