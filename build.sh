#!/usr/bin/env bash
# Install dependencies
pip install -r requirements.txt
# Install Playwright browsers
playwright install chromium
playwright install-deps chromium
