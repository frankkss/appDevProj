#!/usr/bin/env bash
# Build script for Render

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade
