# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, authors, books, borrow
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="📚 Library Management API",
    description="A FastAPI-based library system with JWT auth",
    version="1.0.0",
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    # ✅ Add Bearer JWT auth to Swagger UI
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **Bearer <token>**"
        }
    }
    # ✅ Apply to all non-auth endpoints
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "tags" in operation and "Auth" not in operation["tags"]:
                operation["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
# CORS (for frontend/postman)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(borrow.router)

@app.on_event("startup")
async def startup():
    # Create tables (⚠️ only for dev!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the Library API! 📖", "docs": "/docs"}