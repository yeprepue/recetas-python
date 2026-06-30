import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import uvicorn

if __name__ == "__main__":
    os.chdir(ROOT)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
