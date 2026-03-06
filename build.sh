#!/usr/bin/env bash
# Install dependencies
pip install -r requirements.txt
# Install Playwright browser ONLY (No deps to avoid root error)
playwright install chromium