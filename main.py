from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Import database and models
from db import init_db
from models.manufacturers.manufacturers_models import Manufacturer
from models.retailers.retailers_models import Retailer
from models.distributors.distributors_models import Distributor
from models.partners.partners_models import Partner
from models.terms_conditions.terms_conditions_models import TermsConditions
from models.portfolio.portfolio_models import Portfolio
from models.contact.contact_models import BhukkContact
from routes.manufacturers.manufacturers_routes import router as manufacturers_router
from routes.retailers.retailers_routes import router as retailers_router
from routes.distributors.distributors_routes import router as distributors_router
from routes.partners.partners_routes import router as partners_router
from routes.terms_conditions.terms_conditions_routes import router as terms_conditions_router
from routes.portfolio.portfolio_routes import router as portfolio_router
from routes.contact.contact_routes import router as contact_router

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
app = FastAPI(
    title="BHUKK Pvt. Ltd.",
    description="Backend API for BHUKK is running",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow cross-origin requests from frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(retailers_router)
app.include_router(manufacturers_router)
app.include_router(distributors_router)
app.include_router(partners_router)
app.include_router(terms_conditions_router)
app.include_router(portfolio_router)
app.include_router(contact_router)

# Serve static files (assets)
if not os.path.exists("./assets"):
    os.makedirs("./assets", exist_ok=True)

app.mount("/assets", StaticFiles(directory="./assets"), name="assets")
# Serve uploaded files so saved file URLs are reachable at /uploads/...
if not os.path.exists("./uploads"):
    os.makedirs("./uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")

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
