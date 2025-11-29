# Module Imports
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# Schemas
# ServerStatus
class ServerStatus(BaseModel):
    uuid: str
    running: bool
    created: Optional[datetime]
    uptime: Optional[int]

# ServerStatusList
class ServerStatusList(BaseModel):
    servers: List[str]
