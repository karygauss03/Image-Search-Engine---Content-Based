from pydantic import BaseSettings

class Settings(BaseSettings):
    host: str
    port: int
    index_name: str
    scheme: str
    
    class Config:
        env_file = '.env'
    
settings = Settings()
