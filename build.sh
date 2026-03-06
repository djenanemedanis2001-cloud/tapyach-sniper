#!/usr/bin/env bash

# N-forciw Playwright y-sauvegarder Chrome f' l'dossier actuel machi f' l'Cache
export PLAYWRIGHT_BROWSERS_PATH=0

pip install -r requirements.txt
playwright install chromium