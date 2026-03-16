# FastAPI Main Application
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from library.dddpy.shared.schemas.response_schema import ResponseSchema
import os
from mangum import Mangum

# Import routers
from api.condominiums.routes import router as condominiums_router
from api.buildings_types.routes import router as buildings_types_router
from api.buildings.routes import router as buildings_router
from api.unittys_types.routes import router as unittys_types_router
from api.unitys.routes import router as unitys_router
from api.users.routes import router as users_router
from api.residents.routes import router as residents_router

app = FastAPI(
    title="Condo-Py API",
    description="Backend for Condominium Management System",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseSchema(
            success=False,
            message="Internal server error",
            errors=[str(exc)]
        ).model_dump()
    )



# Health check
@app.get("/health")
def health_check():
    return ResponseSchema(success=True, message="API is running", data={"status": "healthy"})


# Include routers
app.include_router(condominiums_router)
app.include_router(buildings_types_router)
app.include_router(buildings_router)
app.include_router(unittys_types_router)
app.include_router(unitys_router)
app.include_router(users_router)
app.include_router(residents_router)
