from fastapi import APIRouter, HTTPException
from database import get_pool
from models import FasilitasCreate
import json

router = APIRouter(prefix="/api/fasilitas", tags=["Fasilitas"])

# 1. GET GeoJSON (Paling atas agar tidak tertimpa rute {id})
@router.get("/geojson")
async def get_fasilitas_geojson():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, nama, jenis, 
            ST_AsGeoJSON(geom) as geom 
            FROM fasilitas_publik
        """)
        features = []
        for row in rows:
            features.append({
                "type": "Feature",
                "geometry": json.loads(row["geom"]),
                "properties": {
                    "id": row["id"],
                    "nama": row["nama"],
                    "jenis": row["jenis"]
                }
            })
        return {"type": "FeatureCollection", "features": features}

# 2. GET Nearby (Pencarian Radius)
@router.get("/nearby")
async def get_nearby(lat: float, lon: float, radius: int = 1000):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, nama, jenis, 
            ROUND(ST_Distance(geom::geography, ST_Point($1,$2)::geography)::numeric, 2) as jarak_m 
            FROM fasilitas_publik 
            WHERE ST_DWithin(geom::geography, ST_Point($1,$2)::geography, $3) 
            ORDER BY jarak_m
        """, lon, lat, radius)
        return [dict(row) for row in rows]

# 3. GET All Data
@router.get("/")
async def get_all_fasilitas():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, nama, jenis, ST_AsText(geom) as geom FROM fasilitas_publik LIMIT 100")
        return [dict(row) for row in rows]

# 4. GET by ID
@router.get("/{id}")
async def get_fasilitas_by_id(id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id, nama, jenis, alamat, 
            ST_X(geom) as longitude, ST_Y(geom) as latitude 
            FROM fasilitas_publik WHERE id=$1
        """, id)
        if not row:
            raise HTTPException(status_code=404, detail="Fasilitas tidak ditemukan")
        return dict(row)

# 5. POST Input Data Baru
@router.post("/", status_code=201)
async def create_fasilitas(data: FasilitasCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO fasilitas_publik (nama, jenis, alamat, geom) 
            VALUES ($1, $2, $3, ST_SetSRID(ST_Point($4,$5), 4326)) 
            RETURNING id, nama, jenis, alamat, ST_X(geom) as longitude, ST_Y(geom) as latitude
        """, data.nama, data.jenis, data.alamat, data.longitude, data.latitude)
        return dict(row)