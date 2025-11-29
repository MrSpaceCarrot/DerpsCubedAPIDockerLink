# Module Imports
from typing import Optional, List
from pydantic import BaseModel


# Schemas
# ServerStatus
class ServerStatus(BaseModel):
    uuid: str
    running: bool
    uptime: Optional[int]

# ServerStatusList
class ServerStatusList(BaseModel):
    servers: List[str]
