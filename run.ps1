# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py