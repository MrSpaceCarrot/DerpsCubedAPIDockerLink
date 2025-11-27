# Module Imports
from fastapi import APIRouter, Depends
from auth import Authenticator

router = APIRouter()

@router.get("/help", tags=["dockerlink"], dependencies=[Depends(Authenticator())])
def help():
    return "Test"