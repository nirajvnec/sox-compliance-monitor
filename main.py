"""SOX Compliance Monitor - A simple infrastructure monitoring API."""

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import router
from auth import auth_router

app = FastAPI(
    title="SOX Compliance Monitor",
    description="""
## Infrastructure Monitoring & SOX Compliance Tool

### Authentication
- Use **/auth/login** to get an access token
- Sample accounts: **admin / admin123** or **viewer / viewer123**
- Click the **Authorize** button (lock icon) and enter the token
""",
    version="1.0.0",
)

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router)
app.include_router(router)

# Serve React frontend (production build)
# In production, FastAPI serves both the API and the React app
# Check both paths: "frontend/dist" (local dev) and "frontend" (Azure deploy)
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dist = os.path.join(base_dir, "frontend", "dist")
if not os.path.exists(frontend_dist):
    frontend_dist = os.path.join(base_dir, "frontend")

if os.path.exists(os.path.join(frontend_dist, "index.html")):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="static")

    @app.get("/{full_path:path}")
    async def serve_react(request: Request, full_path: str):
        """Serve React app for any non-API route."""
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
