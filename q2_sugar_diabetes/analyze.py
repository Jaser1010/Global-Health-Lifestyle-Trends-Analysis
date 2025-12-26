import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from common import config
from common import data_loader
from common import utils

def run():
    print("\n--- Question 2: Sugar Consumption vs Diabetes (Enhanced - No ML) ---")
    
    # 1. Fetch Data
    data_loader.process_faostat_data()
    data_loader.fetch_diabetes_data()
    
    # 2. Load Data
    try:
        sugar_df = pd.read_csv(config.FILE_SUGAR) # Country, Year, Sugar
        diab_df = pd.read_csv(config.FILE_DIABETES) # Country, Year, Diabetes
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    # 3. Preprocessing
    print("Merging and Imputing Data...")
    sugar_df = utils.standardize_country_names(sugar_df, 'Country')
    diab_df = utils.standardize_country_names(diab_df, 'Country')
    
    master = sugar_df.copy()
    master = pd.merge(master, diab_df, on=['std_country', 'Year'], how='left', suffixes=('_sugar', '_diab'))
    
    if 'Country_diab' in master.columns:
        master['Country'] = master['Country_sugar'].fillna(master['Country_diab'])
        master.drop(columns=['Country_sugar', 'Country_diab'], inplace=True)
        
    master['Diabetes_Prevalence_pct'] = master.groupby('std_country')['Diabetes_Prevalence_pct'].ffill().bfill()
    master.dropna(subset=['Diabetes_Prevalence_pct', 'Sugar_Consumption_kg'], inplace=True)
    
    print(f"Final Integrated Dataset: {len(master)} records.")

    # 4. Categorization (Manual Clustering)
    # Since sklearn is not available, we categorize based on Quartiles
    print("Categorizing Countries by Sugar Consumption (Quartiles)...")
    master['Sugar_Quartile'] = pd.qcut(master['Sugar_Consumption_kg'], 3, labels=['Low', 'Medium', 'High'])

    # 5. Visualization
    sns.set_theme(style="whitegrid")
    
    # Figure 1: Clustered Scatter (using Quartiles)
    print("Generating Figure 1 (Sugar Categories)...")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=master, x='Sugar_Consumption_kg', y='Diabetes_Prevalence_pct', 
                    hue='Sugar_Quartile', palette='viridis', alpha=0.6, s=30)
    plt.title(f'Figure 1: Sugar vs Diabetes - Consumption Groups', fontsize=14)
    plt.xlabel('Sugar Consumption (kg/capita/year)')
    plt.ylabel('Diabetes Prevalence (%)')
    plt.savefig(config.FIG_SUGAR_DIABETES)
    plt.close()
    
    # Figure 4: Top 10
    print("Generating Figure 4 (Top 10)...")
    plt.figure(figsize=(10, 8))
    avg_sugar = master.groupby('Country')['Sugar_Consumption_kg'].mean().sort_values(ascending=False).head(10).reset_index()
    sns.barplot(data=avg_sugar, x='Sugar_Consumption_kg', y='Country', palette='viridis')
    plt.title('Figure 4: Top 10 Countries by Average Sugar Consumption', fontsize=14)
    plt.xlabel('Avg Sugar Consumption (kg/capita/year)')
    plt.savefig(config.FIG_TOP_SUGAR)
    plt.close()

    # 6. Analysis
    print("Calculating Stats...")
    if len(master) > 2:
        corr, p_val = stats.pearsonr(master['Sugar_Consumption_kg'], master['Diabetes_Prevalence_pct'])
        print(f"Sugar Consumption vs Diabetes (N={len(master)}):")
        print(f"   - Correlation: {corr:.4f}, P-value: {p_val:.4e}")
        
    print("\nMean Diabetes by Sugar Group:")
    print(master.groupby('Sugar_Quartile')['Diabetes_Prevalence_pct'].mean())
