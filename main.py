from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import database and models
from db import init_db
from routes.manufacturers.manufacturers_routes import router as manufacturers_router
from routes.retailers.retailers_routes import router as retailers_router

# Load environment variables
load_dotenv()

# Get server configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    init_db()
    yield
    # Shutdown event
    pass

# Create FastAPI application
app = FastAPI(& Retailers API",
    description="Backend API for BHUKK manufacturers and retailers management",
    version="1.0.0",
    lifespan=lifespan
)

# Register routers
app.include_router(manufacturers_router)
app.include_router(retail
app.include_router(manufacturers_router)

# Serve static files (assets)
if not os.path.exists("./assets"):
    os.makedirs("./assets", exist_ok=True)

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")

# Favicon endpoint
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    # Serve favicon from assets directory
    favicon_path = "./assets/logo.svg"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    return JSONResponse({"detail": "Favicon not found"}, status_code=404)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    # API health check endpoint
    return {"status": "healthy", "message": "API is running"}

# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    # Root endpoint with API information
    return {
        "message": "BHUKK Manufacturers API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT
    )
