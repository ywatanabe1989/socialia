# Socialia - Makefile
# Run `make` or `make help` for available commands

.PHONY: help install test post delete dry-run setup check twitter linkedin reddit analytics clean

# Default target
help:
	@echo "Socialia - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install package in development mode"
	@echo "  make setup        Show setup instructions"
	@echo "  make check        Verify credentials are configured"
	@echo ""
	@echo "Posting:"
	@echo "  make twitter MSG='text'     Post to Twitter"
	@echo "  make linkedin MSG='text'    Post to LinkedIn"
	@echo "  make dry-run P=twitter MSG='text'  Preview without posting"
	@echo ""
	@echo "Analytics:"
	@echo "  make analytics-track E='event_name'    Track event in GA"
	@echo "  make analytics-pageviews               Get page view metrics"
	@echo "  make analytics-sources                 Get traffic sources"
	@echo ""
	@echo "Management:"
	@echo "  make delete P=twitter ID=123  Delete a post"
	@echo "  make test         Run tests"
	@echo "  make clean        Remove build artifacts"
	@echo ""
	@echo "Help:"
	@echo "  make help-cli     Show CLI help"
	@echo "  make help-all     Show all CLI commands"
	@echo ""
	@echo "Examples:"
	@echo "  make twitter MSG='Hello World!'"
	@echo "  make linkedin MSG='Professional update'"
	@echo "  make dry-run P=twitter MSG='Test post'"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-mcp:
	pip install -e ".[mcp]"

install-reddit:
	pip install -e ".[reddit]"

install-analytics:
	pip install -e ".[analytics]"

install-all:
	pip install -e ".[all]"

# Setup
setup:
	@./scripts/setup.sh all

setup-twitter:
	@./scripts/setup.sh twitter

setup-linkedin:
	@./scripts/setup.sh linkedin

setup-reddit:
	@./scripts/setup.sh reddit

setup-youtube:
	@./scripts/setup.sh youtube

setup-analytics:
	@./scripts/setup.sh analytics

# Status (calls CLI)
status:
	@socialia status

# Check credentials
check:
	@echo "Checking credentials..."
	@echo ""
	@echo "Twitter:"
	@if [ -n "$$SCITEX_X_CONSUMER_KEY" ]; then echo "  SCITEX_X_CONSUMER_KEY: SET"; else echo "  SCITEX_X_CONSUMER_KEY: NOT SET"; fi
	@if [ -n "$$SCITEX_X_CONSUMER_KEY_SECRET" ]; then echo "  SCITEX_X_CONSUMER_KEY_SECRET: SET"; else echo "  SCITEX_X_CONSUMER_KEY_SECRET: NOT SET"; fi
	@if [ -n "$$SCITEX_X_ACCESSTOKEN" ]; then echo "  SCITEX_X_ACCESSTOKEN: SET"; else echo "  SCITEX_X_ACCESSTOKEN: NOT SET"; fi
	@if [ -n "$$SCITEX_X_ACCESSTOKEN_SECRET" ]; then echo "  SCITEX_X_ACCESSTOKEN_SECRET: SET"; else echo "  SCITEX_X_ACCESSTOKEN_SECRET: NOT SET"; fi
	@echo ""
	@echo "LinkedIn:"
	@if [ -n "$$LINKEDIN_ACCESS_TOKEN" ]; then echo "  LINKEDIN_ACCESS_TOKEN: SET"; else echo "  LINKEDIN_ACCESS_TOKEN: NOT SET"; fi
	@echo ""
	@echo "Reddit:"
	@if [ -n "$$REDDIT_CLIENT_ID" ]; then echo "  REDDIT_CLIENT_ID: SET"; else echo "  REDDIT_CLIENT_ID: NOT SET"; fi
	@if [ -n "$$REDDIT_CLIENT_SECRET" ]; then echo "  REDDIT_CLIENT_SECRET: SET"; else echo "  REDDIT_CLIENT_SECRET: NOT SET"; fi
	@echo ""
	@echo "Google Analytics:"
	@if [ -n "$$GA_MEASUREMENT_ID" ]; then echo "  GA_MEASUREMENT_ID: SET"; else echo "  GA_MEASUREMENT_ID: NOT SET"; fi
	@if [ -n "$$GA_API_SECRET" ]; then echo "  GA_API_SECRET: SET"; else echo "  GA_API_SECRET: NOT SET"; fi
	@if [ -n "$$GA_PROPERTY_ID" ]; then echo "  GA_PROPERTY_ID: SET"; else echo "  GA_PROPERTY_ID: NOT SET (optional)"; fi
	@echo ""
	@echo "Run 'source .env' if credentials not loaded"

# Posting commands
twitter:
ifndef MSG
	@echo "Error: MSG required. Usage: make twitter MSG='your message'"
	@exit 1
endif
	socialia post twitter "$(MSG)"

linkedin:
ifndef MSG
	@echo "Error: MSG required. Usage: make linkedin MSG='your message'"
	@exit 1
endif
	socialia post linkedin "$(MSG)"

# Platform-agnostic post
post:
ifndef P
	@echo "Error: P (platform) required. Usage: make post P=twitter MSG='text'"
	@exit 1
endif
ifndef MSG
	@echo "Error: MSG required. Usage: make post P=twitter MSG='text'"
	@exit 1
endif
	socialia post $(P) "$(MSG)"

# Dry run
dry-run:
ifndef P
	@echo "Error: P (platform) required. Usage: make dry-run P=twitter MSG='text'"
	@exit 1
endif
ifndef MSG
	@echo "Error: MSG required. Usage: make dry-run P=twitter MSG='text'"
	@exit 1
endif
	socialia post $(P) "$(MSG)" --dry-run

# Delete
delete:
ifndef P
	@echo "Error: P (platform) required. Usage: make delete P=twitter ID=123"
	@exit 1
endif
ifndef ID
	@echo "Error: ID required. Usage: make delete P=twitter ID=123"
	@exit 1
endif
	socialia delete $(P) $(ID)

# Thread posting
thread:
ifndef P
	@echo "Error: P (platform) required. Usage: make thread P=twitter FILE=thread.txt"
	@exit 1
endif
ifndef FILE
	@echo "Error: FILE required. Usage: make thread P=twitter FILE=thread.txt"
	@exit 1
endif
	socialia thread $(P) --file $(FILE)

# Reddit posting
reddit:
ifndef MSG
	@echo "Error: MSG required. Usage: make reddit MSG='your message' SUB=python"
	@exit 1
endif
	socialia post reddit "$(MSG)" --subreddit $(or $(SUB),test) $(if $(TITLE),--title "$(TITLE)",)

# Analytics commands
analytics-track:
ifndef E
	@echo "Error: E (event name) required. Usage: make analytics-track E='page_view'"
	@exit 1
endif
	socialia analytics track "$(E)"

analytics-pageviews:
	socialia analytics pageviews $(if $(START),--start $(START),) $(if $(END),--end $(END),)

analytics-sources:
	socialia analytics sources $(if $(START),--start $(START),) $(if $(END),--end $(END),)

analytics-realtime:
	socialia analytics realtime

# Help
help-cli:
	socialia --help

help-all:
	socialia help-recursive

# Testing
test:
	@echo "Running dry-run tests..."
	socialia post twitter "Test" --dry-run
	socialia post linkedin "Test" --dry-run
	@echo "All tests passed!"

test-real:
	@echo "Testing real post (will be deleted)..."
	@ID=$$(socialia --json post twitter "CLI test - deleting" | grep -o '"id": "[^"]*"' | cut -d'"' -f4); \
	if [ -n "$$ID" ]; then \
		echo "Posted: $$ID"; \
		sleep 2; \
		socialia delete twitter $$ID; \
		echo "Deleted: $$ID"; \
	fi

# Cleaning
clean:
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Version
version:
	socialia --version
