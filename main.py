from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.auth.routes import auth_router
from app.nft.routes import nft_router
from app.user.routes import user_router
from app.database import init_db, db

app = FastAPI(title="pixora API",
              description="Blockchain-based Photos/Digital Art publishing, buying & selling platform")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    await init_db()
    yield

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/user", tags=["Users"])
app.include_router(nft_router, prefix="/api/nft", tags=["NFTs"])


@app.get("/")
def read_root():
    return {"Pixora FastAPI"}

@app.get("/health", tags=["Health"])
async def health_check():
    try:
        # Check if MongoDB is connected
        await db.client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}