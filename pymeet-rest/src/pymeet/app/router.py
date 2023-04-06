"""Application configuration - root APIRouter.

Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from pymeet.entrypoints import base
from pymeet.entrypoints.v1 import user

root_api_router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
base_router = APIRouter()

# Base Routers
base_router.include_router(base.router)

# API Routers

# V1
root_api_router_v1.include_router(user.router)
