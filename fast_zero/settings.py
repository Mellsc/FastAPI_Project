from pydantic_settings import (BaseSettings, SettingsConfigDict)
 

class Settings(BaseSetiings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_enconding='utf-8'
    )
    
    DATABASE_URL: str