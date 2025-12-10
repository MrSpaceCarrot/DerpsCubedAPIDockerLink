#!/usr/bin/env python3

# Module Imports
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings, log_config
import routes

# Tags metadata
tags_metadata = [{"name": "dockerlink"}]

# Create app
app = FastAPI(title=settings.APP_TITLE, 
              summary=settings.APP_SUMMARY,
              version=settings.APP_VERSION,
              redirect_slashes=False)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.APP_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup router
app.include_router(routes.router, prefix="")

# Run app
if __name__ == "__main__":
    logging.config.dictConfig(log_config)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.APP_RELOAD,
        log_config=log_config,
        reload_excludes='*.log'
    )
