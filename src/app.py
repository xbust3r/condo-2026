# FastAPI Main Application
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from library.dddpy.shared.schemas.response_schema import ResponseSchema
import os
from mangum import Mangum

# Import routers


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



