# -*- coding: utf-8 -*-
"""
Data Loader Module
------------------
Functions to fetch, scrape, and process data from various sources.
"""
import pandas as pd
import wbgapi as wb
from pytrends.request import TrendReq
from . import config

def fetch_google_trends():
    """Fetches weekly search interest data from Google Trends and saves to CSV."""
    print(f"[1/4] Fetching Google Trends data -> Saving to '{config.FILE_TRENDS}'...")
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(config.KW_LIST, cat=0, timeframe=config.DATE_RANGE_TRENDS, geo='')
        df = pytrends.interest_over_time()
        
        if 'isPartial' in df.columns:
            df = df.drop(columns=['isPartial'])
        
        # Clean column names
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Save to CSV
        df.to_csv(config.FILE_TRENDS)
        print(f"      -> Saved {len(df)} records.")
    except Exception as e:
        print(f"      -> Error: {e}")
        # Create empty placeholder if failed
        pd.DataFrame(columns=['date', 'home_workout', 'gym_membership']).to_csv(config.FILE_TRENDS, index=False)

def process_faostat_data():
    """Loads FAOSTAT CSV, cleans it, and saves the result to a new CSV."""
    print(f"[2/4] Processing FAOSTAT data (Time Series) -> Saving to '{config.FILE_SUGAR}'...")
    input_filepath = config.FAOSTAT_FILE_PATH
    try:
        df = pd.read_csv(input_filepath)
        # Keep Year column for panel analysis
        # Assuming 'Area' is Country, 'Year' is Year, 'Value' is consumption
        clean_df = df[['Area', 'Year', 'Value']].copy()
        clean_df.columns = ['Country', 'Year', 'Sugar_Consumption_kg']
        
        # Ensure Year is int
        clean_df['Year'] = pd.to_numeric(clean_df['Year'], errors='coerce').fillna(0).astype(int)
        clean_df = clean_df[clean_df['Year'] > 0]
        
        # Save to CSV
        clean_df.to_csv(config.FILE_SUGAR, index=False)
        print(f"      -> Saved {len(clean_df)} records (Panel Data).")
    except FileNotFoundError:
        print(f"      -> Error: File {input_filepath} not found.")
        pd.DataFrame(columns=['Country', 'Year', 'Sugar_Consumption_kg']).to_csv(config.FILE_SUGAR, index=False)

def fetch_diabetes_data():
    """Fetches Diabetes data from World Bank API and saves to CSV."""
    print(f"[3a/4] Fetching World Bank Diabetes data (Time Series) -> Saving to '{config.FILE_DIABETES}'...")
    try:
        df_raw = wb.data.DataFrame(config.WB_DIABETES_INDICATOR, time=config.DATE_RANGE_WB, labels=True, skipAggs=True)
        df_raw.reset_index(inplace=True)

        id_vars = ['economy', 'Country']
        value_vars = [col for col in df_raw.columns if col.startswith('YR')]
        df_melted = df_raw.melt(id_vars=id_vars, value_vars=value_vars, var_name='year_col', value_name='value')
        
        df_melted['Year'] = df_melted['year_col'].str.replace('YR', '').astype(int)
        
        # Keep all years, just drop NaNs
        df_clean = df_melted.dropna(subset=['value']).sort_values(['Country', 'Year'])
        
        df_clean = df_clean[['Country', 'Year', 'value']]
        df_clean.columns = ['Country', 'Year', 'Diabetes_Prevalence_pct']
        
        # Save to CSV
        df_clean.to_csv(config.FILE_DIABETES, index=False)
        print(f"      -> Saved {len(df_clean)} records (Panel Data).")
    except Exception as e:
        print(f"      -> Error: {e}")
        pd.DataFrame(columns=['Country', 'Year', 'Diabetes_Prevalence_pct']).to_csv(config.FILE_DIABETES, index=False)

def fetch_obesity_data():
    """Scrapes Obesity data and saves to CSV."""
    print(f"[3b/4] Scraping Obesity data (Static) -> Saving to '{config.FILE_OBESITY}'...")
    url = 'https://worldpopulationreview.com/country-rankings/obesity-rates-by-country'
    try:
        tables = pd.read_html(url)
        df = tables[0]
        # Dynamically find the obesity column
        obesity_col = [c for c in df.columns if 'Obesity' in c or 'Rate' in c][-1]
        
        clean_df = df[['Country', obesity_col]].copy()
        clean_df.columns = ['Country', 'Obesity_Prevalence_pct']
        
        # Clean percentage strings if necessary
        if clean_df['Obesity_Prevalence_pct'].dtype == object:
            clean_df['Obesity_Prevalence_pct'] = clean_df['Obesity_Prevalence_pct'].astype(str).str.replace('%', '').str.strip()
            clean_df['Obesity_Prevalence_pct'] = pd.to_numeric(clean_df['Obesity_Prevalence_pct'], errors='coerce')
            
        clean_df.dropna(inplace=True)
        
        # Save to CSV
        clean_df.to_csv(config.FILE_OBESITY, index=False)
        print(f"      -> Saved {len(clean_df)} records (Static).")
    except Exception as e:
        print(f"      -> Error: {e}")
        pd.DataFrame(columns=['Country', 'Obesity_Prevalence_pct']).to_csv(config.FILE_OBESITY, index=False)

def create_gym_data():
    """Creates gym data manually and saves to CSV."""
    print(f"[4/4] Creating Gym membership data (Static) -> Saving to '{config.FILE_GYM}'...")
    data = {
        'Country': ['United States', 'United Kingdom', 'Switzerland', 'New Zealand', 'Germany',
                    'Sweden', 'Norway', 'Netherlands', 'Denmark', 'Canada', 'Australia',
                    'Spain', 'Italy', 'France', 'Brazil', 'Japan', 'China', 'India', 'Mexico', 'United Arab Emirates'],
        'Gym_Penetration_pct': [23.7, 15.9, 14.9, 13.6, 13.4, 22.0, 22.0, 18.0, 18.0, 16.7, 15.3,
                                11.5, 9.5, 9.2, 4.6, 4.0, 3.0, 0.6, 3.2, 5.8]
    }
    df = pd.DataFrame(data)
    df.to_csv(config.FILE_GYM, index=False)
    print(f"      -> Saved {len(df)} records.")
