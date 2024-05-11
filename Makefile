# Makefile

# Variables
VENV_NAME := environment
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

# Default target (run the application)
server: 
	$(PYTHON) run.py



# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt
	@echo "Virtual environment created."

# Install project dependencies
install: venv

# Clean up generated files and directories
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	@echo "Cleaned up."

# Help message
help:
	@echo "Available targets:"
	@echo "  run        : Run the application"
	@echo "  install    : Install project dependencies"
	@echo "  clean      : Clean up generated files and directories"
	@echo "  help       : Show this help message"

.PHONY: run install clean help