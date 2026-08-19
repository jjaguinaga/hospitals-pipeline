import pandas as pd
from pathlib import Path
from config.settings import settings
from src.logger import get_logger

class DataExtractor:
   
   def __init__(self, raw_path=None):
      self.raw_path = raw_path or settings.RAW_DATA_PATH
      
      self.logger = get_logger('extract')
      
   def _read_csv(self, filename: str):
      file_path = self.raw_path / filename
      
      self.logger.info(f'Reading {filename}')
      
      df = pd.read_csv(file_path, dtype=str, keep_default_na=True)
      
      self.logger.info(f'Loaded {len(df)} rows from {filename}')
      
      return df

   def extract_addmissions(self):
      return self._read_csv('admissions.csv')
   
   def extract_appointments(self):
      return self._read_csv('appointments.csv')
   
   def extract_billings(self):
      return self._read_csv('billing.csv')
   
   def extract_departments(self):
      return self._read_csv('departments.csv')
   
   def extract_doctors(self):
      return self._read_csv('doctors.csv')
   
   def extract_hospitals(self):
      return self._read_csv('hospitals.csv')
   
   def extract_lab_results(self):
      return self._read_csv('lab_results.csv')
   
   def extract_nurse_assign(self):
      return self._read_csv('nurse_assignments.csv')
   
   def extract_nurses(self):
      return self._read_csv('nurses.csv')
   
   def extract_patients(self):
      return self._read_csv('patients.csv')
   
   def extract_prescriptions(self):
      return self._read_csv('prescriptions.csv')
   
   def extract_supplies(self):
      return self._read_csv('supplies.csv')
   
   def extract_supply_usage(self):
      return self._read_csv('supply_usage.csv')
   
   def extract_surgeries(self):
      return self._read_csv('surgeries.csv')
   
   def extract_vitals(self):
      return self._read_csv('vitals.csv')