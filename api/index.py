import sys
import os

# Add current and parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

# Entrypoint for Vercel Serverless Function
app = app
