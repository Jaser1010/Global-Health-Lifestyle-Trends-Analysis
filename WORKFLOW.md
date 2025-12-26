# Analysis Workflow & Architecture

This document outlines the data processing pipeline and architectural decisions for the Global Health Trends Analysis project.

## 1. Initialization & Configuration

* **Module:** `common/config.py`
* Sets up absolute paths for `data/` and `figures/` directories to ensure portability.
* Defines constants for API indicators (World Bank), date ranges, and target keywords.

## 2. Data Ingestion (ETL)

* **Module:** `common/data_loader.py`
* **Google Trends:** Fetches weekly interest data for "home workout" (2018-2024) to analyze pandemic impacts.
* **FAOSTAT Sugar:** Processes raw CSV data, filtering for valid Country/Year/Value tuples.
* **World Bank Diabetes:** Queries `wbgapi` for diabetes prevalence (% of population ages 20-79).
* **Obesity Data:** Scrapes HTML tables from *World Population Review* for latest static obesity rates.
* **Gym Data:** Generates a static reference dataframe for gym penetration rates.

## 3. Data Cleaning & Standardization

* **Module:** `common/utils.py`
* **Country Mapping:** A critical step is standardizing country names (e.g., "USA" -> "united states", "Korea, Rep." -> "south korea") to ensure successful merges across disparate data sources.
* **Type Casting:** Ensures numeric columns are correctly typed and years are integers.

## 4. Integration (Panel Data Strategy)

* **Module:** `main.py`
* **Merge Logic:**
    1. Uses **Sugar Consumption** (FAOSTAT) as the base spine (Country-Year) due to its high granularity (~2400 rows).
    2. Left-joins Diabetes data on `[Country, Year]`.
    3. Left-joins static data (Obesity, Gym) on `[Country]`.
* **Imputation:** Since Diabetes data is often periodic, missing values are imputed using forward-fill (`ffill`) and backward-fill (`bfill`) per country to maximize the sample size for correlation analysis.

## 5. Analysis & Reporting

* **Modules:** `q1_trends/analyze.py`, `q2_sugar_diabetes/analyze.py`, `q3_gym_obesity/analyze.py`
* **Exploratory Data Analysis (EDA):** Each module generates specific visualizations using `matplotlib` and `seaborn`.
* **Statistical Tests:** Performs correlation and hypothesis tests (`scipy.stats`) to quantify relationships:
  * Q1: Search interest correlation (Home Workout vs Gym Membership)
  * Q2: Sugar Intake ↔ Diabetes Prevalence
  * Q3: Gym Membership ↔ Obesity Rates

## 6. Artifact Generation

* The final cleaned panel dataset is serialized to CSV.
* High-resolution figures are saved to the `figures/` directory.
