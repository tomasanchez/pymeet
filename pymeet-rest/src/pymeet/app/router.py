"""Application configuration - root APIRouter.

Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from pymeet.entrypoints import base

root_api_router_v1 = APIRouter(prefix="/api/v1")
base_router = APIRouter()

# Base Routers
base_router.include_router(base.router)

# API Routers
