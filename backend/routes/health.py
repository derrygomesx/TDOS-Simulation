"""
Health routes.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def root():

    return {

        "application": "TrackGuard Digital Operations Sandbox",

        "version": "1.0.0",

        "status": "running",

    }


@router.get("/health")
def health():

    return {

        "service": "TDOS",

        "status": "healthy",

    }