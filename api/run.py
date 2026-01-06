"""
Simple script to run the FastAPI application.

Run this from the repository root:
    python api/run.py

Or from the api directory:
    python run.py
"""

import uvicorn
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

