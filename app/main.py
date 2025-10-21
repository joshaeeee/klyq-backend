from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, webhooks, data, actions, admin
from .config import settings

app = FastAPI(title="Clique AI CMO Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(actions.router, prefix="/api/actions", tags=["actions"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/")
async def root():
    return {"message": "Clique AI CMO Backend API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
