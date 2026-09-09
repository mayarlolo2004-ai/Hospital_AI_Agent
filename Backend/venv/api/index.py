import sys
from pathlib import Path

# Add project root to path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app

# Create Vercel entrypoint app
app = FastAPI()

# Enable CORS for all origins (Streamlit Cloud integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount original application
app.mount("/", fastapi_app)