# -*- coding: utf-8 -*-
"""
Configuration Module
--------------------
Centralizes file paths, constants, and configuration settings for the project.
"""
import os

# --- Paths ---
# Adjusted for location in common/config.py (one level deeper than root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# --- Input Files ---
FAOSTAT_FILENAME = 'FAOSTAT_data_en_12-18-2025.csv'
FAOSTAT_FILE_PATH = os.path.join(DATA_DIR, FAOSTAT_FILENAME)

# --- Output Data Files ---
FILE_TRENDS = os.path.join(DATA_DIR, 'data_trends_google_v2.csv')
FILE_SUGAR = os.path.join(DATA_DIR, 'data_sugar_cleaned_v2.csv')
FILE_DIABETES = os.path.join(DATA_DIR, 'data_diabetes_wb_v2.csv')
FILE_OBESITY = os.path.join(DATA_DIR, 'data_obesity_scraped_v2.csv')
FILE_GYM = os.path.join(DATA_DIR, 'data_gym_manual_v2.csv')
FILE_FINAL_PANEL = os.path.join(DATA_DIR, 'final_project_dataset_panel.csv')

# --- Output Figure Files ---
FIG_SUGAR_DIABETES = os.path.join(FIGURES_DIR, 'fig1_sugar_diabetes.png')
FIG_GYM_OBESITY = os.path.join(FIGURES_DIR, 'fig2_gym_obesity.png')
FIG_TRENDS = os.path.join(FIGURES_DIR, 'fig3_trends.png')
FIG_TOP_SUGAR = os.path.join(FIGURES_DIR, 'fig4_top_sugar.png')

# --- Parameters ---
WB_DIABETES_INDICATOR = 'SH.STA.DIAB.ZS'
DATE_RANGE_WB = range(2010, 2025)
DATE_RANGE_TRENDS = '2018-01-01 2024-12-31'
KW_LIST = ["home workout", "gym membership"]
