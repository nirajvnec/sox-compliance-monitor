"""SOX Compliance Monitor - A simple infrastructure monitoring API."""

from fastapi import FastAPI
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

# Include routes
app.include_router(auth_router)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
