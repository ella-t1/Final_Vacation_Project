# Installation Guide

## Windows Installation

On Windows, especially when using Git Bash, use the `py` launcher instead of `pip` directly.

### Install Dependencies

```bash
# In Git Bash or PowerShell
py -m pip install -r requirements.txt
```

### Alternative Commands

If `py` doesn't work, try:
- `python -m pip install -r requirements.txt`
- `python3 -m pip install -r requirements.txt`
- `pip3 install -r requirements.txt`

### Run the API Server

```bash
py run_api.py
```

Or:
```bash
python run_api.py
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

```bash
# Create virtual environment
py -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Git Bash)
source .venv/Scripts/activate

# Install dependencies
py -m pip install -r requirements.txt

# Run API
py run_api.py
```


