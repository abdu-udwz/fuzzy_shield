from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated
from pydantic import UrlConstraints
from pydantic_core import Url


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='fuzzy_', env_file='.env')

    # The default URL expects the app to run using Docker and docker-compose.
    redis_url: Annotated[Url, UrlConstraints(
        allowed_schemes=['redis'], default_host="localhost", default_port="6379", default_path="/0")] = "redis://localhost:6379"
