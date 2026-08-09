import os
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
   config_folder: Path = Path(__file__).parent
   
   project_root: Path = config_folder.parent
   
   RAW_DATA_PATH: Path = project_root / 'data' / 'raw'
   
   PROCESSED_PATH: Path = project_root / 'data' / 'processed'
   
   QUARANTINE_PATH: Path = project_root / 'data' / 'quarantine'
   
   LOGS_PATH: Path = project_root / 'data' / 'logs'
   
   DB_HOST: str = os.getenv('DB_HOST', 'localhost')
   
   DB_PORT: str = os.getenv('DB_PORT', '5432')
   
   DB_NAME: str = os.getenv('DB_NAME', 'hospital_system')
      
   DB_USER: str = os.getenv('DB_USER', 'naga')
      
   DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
   
   @property
   def database_url(self):
      return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
   
   def ensure_directories(self):
      self.RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
      
      self.PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
      
      self.QUARANTINE_PATH.mkdir(parents=True, exist_ok=True)
      
      self.LOGS_PATH.mkdir(parents=True, exist_ok=True)
      
settings = Settings()

settings.ensure_directories()
