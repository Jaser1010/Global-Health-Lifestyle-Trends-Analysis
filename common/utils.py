# -*- coding: utf-8 -*-
"""
Utilities Module
----------------
Helper functions for data cleaning and standardization.
"""
import pandas as pd

def standardize_country_names(df: pd.DataFrame, country_col: str) -> pd.DataFrame:
    """
    Standardizes country names for consistent merging across different datasets.
    
    Args:
        df (pd.DataFrame): The dataframe containing the country column.
        country_col (str): The name of the column containing country names.
        
    Returns:
        pd.DataFrame: DataFrame with a new 'std_country' column.
    """
    mapping = {
        'united states of america': 'united states', 'usa': 'united states',
        'united kingdom of great britain and northern ireland': 'united kingdom', 'uk': 'united kingdom',
        'russian federation': 'russia',
        'korea, rep.': 'south korea', 'republic of korea': 'south korea',
        'iran (islamic republic of)': 'iran', 'iran, islamic rep.': 'iran',
        'venezuela (bolivarian republic of)': 'venezuela', 'venezuela, rb': 'venezuela',
        'bolivia (plurinational state of)': 'bolivia',
        'egypt, arab rep.': 'egypt', 'turkiye': 'turkey'
    }
    
    def clean(name):
        if not isinstance(name, str): 
            return name
        name = name.lower().strip()
        return mapping.get(name, name)
        
    df['std_country'] = df[country_col].apply(clean)
    return df
