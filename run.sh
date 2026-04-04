#!/bin/bash

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip (recommended)
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py