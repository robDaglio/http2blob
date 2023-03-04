import json
import asyncio

from uuid import uuid4

from main import log, cfg
from models.models import Event
from azure_blob.blob_storage import AzureBlob

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = InferringRouter()
security = HTTPBasic()


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not ((credentials.username == cfg.api_user) and (credentials.password == cfg.api_pass)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Basic'}
        )

    return credentials.username


@cbv(router)
class Endpoints:
    def __init__(self):
        """
        The Endpoints class exposes a handler that listens for requests on a specific port
        and forwards them to Azure blob storage. It is composed of the handler itself as
        well as an instance of the AzureBlob class that handles forwarding to azure storage.

        """

        self.queue = asyncio.Queue()
        self.azure_blob_uploader = AzureBlob(cfg.connection_string, cfg.container_name)

    @router.get('/echo', status_code=200)
    async def echo(self):
        raise HTTPException(status_code=200, detail='OK')

    @router.post('/blob', status_code=200)
    async def handler(self, event: Event, username: str = Depends(auth)) -> str:

        incoming_data = jsonable_encoder(event)
        log.info(f'Request received:\n{json.dumps(incoming_data, indent=4)}')

        log.info('Appending data to incoming queue.')
        await self.queue.put(json.dumps(incoming_data))

        result = await self.forward_to_blob()

        await self.queue.join()
        log.debug(result)

        return result

    async def forward_to_blob(self):
        task_id = asyncio.current_task().get_name()
        outgoing_data = await self.queue.get()

        if not outgoing_data:
            log.debug('No data provided.')
            self.queue.task_done()
            return

        log.info('Pushing data to blob storage.', extra={'id': task_id})
        upload_result = await self.azure_blob_uploader.upload_data(outgoing_data)
        self.queue.task_done()

        return upload_result
