import logging
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_local_file(self, file_path: str):
        object_name = file_path.split("/")[-1]  # /users/artem/cat.jpg
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                logger.info(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise e

    async def upload_data(self, data, path):
        try:
            async with self.get_client() as client:
                resp = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=path,
                    Body=data,
                )
                logger.info(f"File {path} uploaded to {self.bucket_name}")
                return resp
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise e

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            raise e

    async def download_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(
                    Bucket=self.bucket_name, Key=object_name
                )
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                logger.info(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            raise e


# async def main():
#     s3_client = S3Client(
#         access_key="",
#         secret_key="",
#         endpoint_url="",  # для Selectel используйте https://s3.storage.selcloud.ru
#         bucket_name="wml",
#     )

#     # Проверка, что мы можем загрузить, скачать и удалить файл
#     await s3_client.upload_local_file("./n2wml.np.d/receipts/040__00__ИБП.jpeg")
#     await s3_client.download_file("test.txt", "text_local_file.txt")
#     await s3_client.delete_file("test.txt")


# if __name__ == "__main__":
#     asyncio.run(main())
