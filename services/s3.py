from contextlib import asynccontextmanager
from typing import Optional

from aiobotocore.session import get_session

from core.config import settings


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client(
            "s3", **self.config, verify=False
        ) as client:
            yield client

    async def upload_bytes(
        self,
        data: bytes,
        key: str,
        content_type: str,
        bucket_name: str,
        disposition: str = "inline",
        acl: Optional[str] = None,
    ) -> str:
        extra = {}
        if acl:
            extra["ACL"] = acl
        async with self.get_client() as client:
            await client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=data,
                ContentType=content_type,
                ContentDisposition=disposition,
            )
        return key

    async def get_object(
        self,
        key: str,
        bucket_name: str,
    ) -> Optional[tuple[bytes, str]]:
        async with self.get_client() as client:
            try:
                response = await client.get_object(Bucket=bucket_name, Key=key)
                data = await response["Body"].read()
                content_type = response.get("ContentType", "application/octet-stream")
                return data, content_type
            except client.exceptions.NoSuchKey:
                return None

    def object_url(self, key: str, bucket_url: str) -> str:
        return f"{f"https://{bucket_url}.tkirbis30.ru".rstrip('/')}/{key}"

    async def presigned_get_url(
        self, bucket_name: str, key: str, expires_in: int = 3600
    ) -> str:
        async with self.get_client() as client:
            return client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )


s3_client = S3Client(
    access_key=settings.S3_ACCESS_KEY,
    secret_key=settings.S3_SECRET_KEY,
    endpoint_url=settings.S3_ENDPOINT_URL,
)
