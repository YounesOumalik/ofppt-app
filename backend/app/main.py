from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import SessionLocal, engine
from .seed import init_db, seed_admin
from .routers import auth, admin, import_excel, parametrage, data, dashboard

app = FastAPI(title="OFPPT Management", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(import_excel.router)
app.include_router(parametrage.router)
app.include_router(data.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    seed_admin(db)
    db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
