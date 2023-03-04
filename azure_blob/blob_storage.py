import asyncio
from azure.storage.blob.aio import BlobServiceClient
from azure.core.exceptions import HttpResponseError
from main import log
from uuid import uuid4


class AzureBlob:
    def __init__(self, connection_string: str, container_name: str) -> None:
        """
        The AzureBlob class takes a connection string and azure blob container name
        and creates an instance of BlobServiceClient that will upload passed data
        to Azure blob storage.

        :param connection_string: predefined connection string generated in azure used to connect to azure blob storage.
        :param container_name: the azure blob container to connect to.
        """

        self.connection_string = connection_string
        self.container_name = container_name

    async def upload_data(self, data) -> str:
        log.debug('Creating Blob Service Client')
        task_id = asyncio.current_task().get_name()

        try:
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

            async with blob_service_client:
                blob_client = blob_service_client.get_blob_client(
                    container=self.container_name, blob=f'{uuid4()}.json')

                log.info('Uploading via Azure Blob service client.', extra={'id': task_id})
                result = await blob_client.upload_blob(data)

            return result['client_request_id']

        except HttpResponseError as e:
            log.error(e)
            return f'Upload failed! | {e}'

