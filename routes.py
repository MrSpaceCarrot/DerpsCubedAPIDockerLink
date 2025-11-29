# Module Imports
from typing import Optional, List
from datetime import datetime, timezone
import docker
import logging
from fastapi import APIRouter, Depends
from auth import Authenticator
from config import settings
from schemas import ServerStatus, ServerStatusList

router = APIRouter()

# Logger
logger = logging.getLogger("services")

# Create docker client
docker_client = docker.APIClient(base_url=settings.DOCKER_SOCKET_ENDPOINT)

@router.post("/info", tags=["dockerlink"], dependencies=[Depends(Authenticator())], response_model=List[ServerStatus])
def get_container_info_multiple(servers: ServerStatusList):
    # Get containers from docker socket
    containers = docker_client.containers()

    # Create list to store results
    server_statuses: List[ServerStatus] = []

    # Check all given servers
    for server in servers.servers:
        
        # Set variable to check if that server is running or not
        server_present = False

        # Check each container
        for container in containers:
            
            # Check every server name
            for name in container["Names"]:
                if str(server) in name:
                    server_present = True

        # Add item to list
        if server_present == True:
            container_created = container["Created"]
            now = int(datetime.now(timezone.utc).timestamp())
            container_uptime = now - container_created

            server_statuses.append(ServerStatus(uuid=server, running=True, created=container_created, uptime=container_uptime))
        else:
            server_statuses.append(ServerStatus(uuid=server, running=False, created=None, uptime=None))      
    
    # Return final list
    return server_statuses


@router.get("/info/{uuid}", tags=["dockerlink"], dependencies=[Depends(Authenticator())], response_model=Optional[ServerStatus])
def get_container_info_single(uuid: str):
    # Get containers from docker socket
    containers = docker_client.containers()

    # Find the correct container based on uuid
    for container in containers:
        for name in container["Names"]:
            if str(uuid) in name:
                container_created = container["Created"]
                now = int(datetime.now(timezone.utc).timestamp())
                container_uptime = now - container_created

                return ServerStatus(uuid=uuid, running=True, created=container_created, uptime=container_uptime)
            
    return ServerStatus(uuid=uuid, running=False, created=None, uptime=None)
