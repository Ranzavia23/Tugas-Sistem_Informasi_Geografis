from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_pool, close_pool
from routers import fasilitas
from fastapi.middleware.cors import CORSMiddleware # 1. Tambahkan import ini

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    print("Database connected")
    yield
    await close_pool()
    print("Database disconnected")

app = FastAPI(
    title="WebGIS API SIG Lampung",
    description="REST API untuk data fasilitas publik Rajabasa",
    version="1.0.0",
    lifespan=lifespan
)

# 2. Tambahkan blok ini agar React (port 5173) diizinkan masuk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fasilitas.router)