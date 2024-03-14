help: ## Show list of commands
	@printf "\033[33m%s:\033[0m\n\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


run: ## Run app
	cd example; python app.py
