from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    #PRUEBA1="HOLA"
    supabase_url:str=Field(default="",alias="SUPABASE_URL")
    supabase_key:str=Field(default="",alias="SUPABASE_KEY")
    supabase_schema:str=Field(default="public",alias="SUPABASE_SCHEMA")
    supabase_table:str=Field(default="products",alias="SUPABASE_TABLE")
    allowed_origins:list[str]=Field(default=[],alias="ALLOWED_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",#el valor por default es "forbid"
    )
config = Config()  

print(config.supabase_url)
print(config.supabase_key)
