import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv(dotenv_path="./dotenv-file/.env")


class S3_configs(BaseModel):
    local_path: str = os.environ.get("LOCAL_PATH")
    endpoint: str = os.environ.get("ENDPOINT_URL")
    _bucket: str = os.environ.get("BUCKET")
    _path: str = os.environ.get("BUCKET_PATH")
    key_id: str = os.environ.get("KEY_ID")
    access_key: str = os.environ.get("ACCESS_KEY")
    token: str = os.environ.get("TOKEN")
