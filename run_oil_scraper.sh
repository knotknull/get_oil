#!/bin/bash
#
# Wrapper script for the oil price scraper application.
# This script sets up the environment and executes the Python application.
#

# Exit on any error
set -e

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Application root directory
# APP_DIR="${SCRIPT_DIR}/oil_price_scraper"
APP_DIR="${SCRIPT_DIR}"

# Log file
LOG_FILE="${SCRIPT_DIR}/logs/scraper.log"

# Python path
PYTHON="${SCRIPT_DIR}/.venv/bin/python"

# Check if .env file exists
if [ ! -f "${SCRIPT_DIR}/.env" ]; then
    echo "Error: .env file not found. Please create it based on .env.template" | tee -a "${LOG_FILE}"
    exit 1
fi

# Set only essential variables that aren't in .env
export LOG_LEVEL=${LOG_LEVEL:-INFO}

# Log start of execution
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting oil price scraper" >> "${LOG_FILE}"

# Ensure we're in the script directory
cd "${SCRIPT_DIR}"

# Check if virtual environment exists, create if it doesn't
if [ ! -d "${SCRIPT_DIR}/.venv" ]; then
    echo "Virtual environment not found, creating..." >> "${LOG_FILE}"
    uv venv
    "${SCRIPT_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt"
fi

# Run the scraper
echo "Running oil price scraper..." >> "${LOG_FILE}"
"${PYTHON}" oil_price_scraper.py "$@"

# Capture exit code
EXIT_CODE=$?

# Log results
if [ $EXIT_CODE -ne 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Scraper failed with exit code ${EXIT_CODE}" >> "${LOG_FILE}"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Scraper completed successfully" >> "${LOG_FILE}"
fi

# Return exit code
exit $EXIT_CODE 
