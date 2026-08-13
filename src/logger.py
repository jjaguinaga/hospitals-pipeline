import logging
import sys
from config.settings import settings

def get_logger(name: str):
   logger = logging.getLogger(name)
   
   logger.setLevel(logging.INFO)
   
   if not logger.handlers:
      
      console_handler = logging.StreamHandler(sys.stdout)
      
      console_handler.setLevel(logging.INFO)
      
      file_handler = logging.FileHandler(settings.LOGS_PATH/'pipeline.log')
      
      file_handler.setLevel(logging.INFO)
      
      formatter = logging.Formatter(
      '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
      )
      
      console_handler.setFormatter(formatter)
      
      file_handler.setFormatter(formatter)
      
      logger.addHandler(console_handler)
      
      logger.addFilter(file_handler)
      
   return logger