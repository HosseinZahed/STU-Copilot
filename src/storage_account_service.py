from azure.storage.blob import BlobServiceClient
from typing import Any
import os

class StorageAccountService:
    def __init__(self, account_name: str = None, account_key: str = None):
        if account_name is None:
            account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        if account_key is None:
            account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={account_name};"
            f"AccountKey={account_key};"
            f"EndpointSuffix=core.windows.net"
        )
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def upload_blob(self, container_name: str, blob_name: str, data: Any, overwrite: bool = True):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.upload_blob(name=blob_name, data=data, overwrite=overwrite)

    def download_blob(self, container_name: str, blob_name: str) -> bytes:
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def list_blobs(self, container_name: str):
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def delete_blob(self, container_name: str, blob_name: str):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.delete_blob(blob_name)