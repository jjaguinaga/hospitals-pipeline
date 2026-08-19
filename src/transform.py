import pandas as pd
import re
from config.settings import settings
from src.logger import get_logger
from datetime import datetime

class DataTransformer:
   
   def __init__(self):
      self.logger = get_logger('transform')
      
      self.quarantine_dfs = []
      
      self._clear_quarantine()
      
   def _clear_quarantine(self):
      for file in settings.QUARANTINE_PATH.glob('quarantine_*.csv'):
         file.unlink()
         
      self.logger.info('Cleared old quarantine files')
         
   def _save_quarantine(self, df, name):
      timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
      
      if df.empty:
         return
      
      filename = settings.QUARANTINE_PATH / f'quarantine_{name}_{timestamp}.csv'
      
      df.to_csv(filename, index=False)
      
      self.logger.info(f'Quarantined {len(df)} rows to {filename}')
      
      self.quarantine_dfs.append(df)
      
   def _parse_datetime(self, column):
      return pd.to_datetime(column, format='mixed', errors='coerce')
   
   def _to_float(self, column):
      if column is None or str(column).lower() in ('none', 'nan', ''):
         return None
      
      else:
         return float(re.sub(r'[^\d.]', '', str(column)))
      
   def _normalize_disposition(self, value):
      if pd.isna(value):
         return None
      
      else:
         mapping = {
            'home': 'Home',
            'HOME': 'Home',
            'Rehab': 'Rehabilitation',
            'SNF': 'Skilled Nursing Facility',
            'LAMA': 'Left Against Medical Advice'
         }
         
         result = mapping.get(str(value).strip(), str(value).strip())
         
         return result
      
   def _normalize_readmission(self, row):
      if pd.isna(row['readmission_30_day_flag']):
         if row['is_active'] == True:
            return pd.NA
         
         else: 
            return False
         
      else:
         mapping = {
            'N': False,
            'No': False,
            'Y': True,
            '0': False,
            'Yes': True,
            'FALSE': False,
            '1': True,
            'TRUE': True
         }
         
         result = mapping.get(row['readmission_30_day_flag'])
         
         return result
      
   def transform_admissions(self, df):
      self.logger.info('Transforming admissions...')
      
      df = df.drop(columns=['room_number'], errors='ignore')
      
      df['admission_date'] = df['admission_date'].apply(self._parse_datetime)
      
      df['discharge_date'] = df['discharge_date'].apply(self._parse_datetime)
      
      bad_discharge = df['discharge_date'].isna()
      
      has_disposition = df['discharge_disposition'].notna()
      
      inconsistent = bad_discharge & has_disposition
      
      if inconsistent.any():
         self._save_quarantine(df[inconsistent], 'admissions_bad_discharge_date')
         
      df = df[~inconsistent].copy()
      
      df['is_active'] = df['discharge_date'].isna() & df['discharge_disposition'].isna()
      
      df['total_bill_amount'] = df['total_bill_amount'].apply(self._to_float)
      
      df['insurance_approved_amount'] = df['insurance_approved_amount'].apply(self._to_float)
      
      bad_codes = df['icd10_code'].isna()
      
      if bad_codes.any():
         self._save_quarantine(df[bad_codes], 'admissions_bad_icd10_codes')
         
      df = df[~bad_codes].copy()
      
      bad_department = df['department_id'].isna()
      
      if bad_department.any():
         self._save_quarantine(df[bad_department], 'admissions_null_department')
         
      df = df[~bad_department].copy()
      
      df['discharge_disposition'] = df['discharge_disposition'].apply(self._normalize_disposition)
      
      df['length_of_stay_days'] = (df['discharge_date'] - df['admission_date']).dt.days
      
      df['readmission_30_day_flag'] = df.apply(self._normalize_readmission, axis=1)
      
      null_insurance = df['insurance_approved_amount'].isna()
      
      discharged = df['is_active'] == False
      
      bad_insurance = null_insurance & discharged
      
      if bad_insurance.any():
         self._save_quarantine(df[bad_insurance], 'admissions_bad_insurance')
         
      df = df[~bad_insurance].copy()
      
      return df 