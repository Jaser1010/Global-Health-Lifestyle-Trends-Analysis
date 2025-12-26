import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from common import config
from common import data_loader
from common import utils

def run():
    print("\n--- Question 3: Gym Penetration vs Obesity (Enhanced) ---")
    
    # 1. Fetch Data
    data_loader.fetch_obesity_data()
    data_loader.create_gym_data()
    
    # 2. Load Data
    try:
        obes_df = pd.read_csv(config.FILE_OBESITY) # Country, Obesity
        gym_df = pd.read_csv(config.FILE_GYM) # Country, Gym
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return

    # 3. Preprocessing
    print("Merging Data...")
    obes_df = utils.standardize_country_names(obes_df, 'Country')
    gym_df = utils.standardize_country_names(gym_df, 'Country')
    
    # Merge on std_country
    merged = pd.merge(gym_df, obes_df, on='std_country', how='inner', suffixes=('_gym', '_obes'))
    
    # Fix Country Name (prefer Gym's country name)
    if 'Country_gym' in merged.columns:
        merged['Country'] = merged['Country_gym']
    
    merged.dropna(subset=['Gym_Penetration_pct', 'Obesity_Prevalence_pct'], inplace=True)
    
    print(f"Integrated Dataset: {len(merged)} records.")

    # 4. Hypothesis Testing (T-Test)
    print("Performing Hypothesis Test...")
    # Group countries into "High Gym Use" vs "Low Gym Use"
    median_gym = merged['Gym_Penetration_pct'].median()
    merged['Gym_Group'] = merged['Gym_Penetration_pct'].apply(lambda x: 'High (>Median)' if x > median_gym else 'Low (<=Median)')
    
    group_high = merged[merged['Gym_Group'] == 'High (>Median)']['Obesity_Prevalence_pct']
    group_low = merged[merged['Gym_Group'] == 'Low (<=Median)']['Obesity_Prevalence_pct']
    
    t_stat, p_val = stats.ttest_ind(group_high, group_low, equal_var=False)
    
    print(f"T-Test Results (High vs Low Gym Penetration):")
    print(f"   - T-Statistic: {t_stat:.4f}")
    print(f"   - P-Value: {p_val:.4e}")
    if p_val < 0.05:
        print("   -> Conclusion: Statistically significant difference in obesity rates.")
    else:
        print("   -> Conclusion: No statistically significant difference found.")

    # 5. Visualization
    sns.set_theme(style="whitegrid")
    
    # Figure 2a: Gym vs Obesity Scatter
    print("Generating Figure 2a (Scatter)...")
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(data=merged, x='Gym_Penetration_pct', y='Obesity_Prevalence_pct', 
                    s=100, hue='Country', legend=False)
    
    for i in range(len(merged)):
        plt.text(x=merged.Gym_Penetration_pct.iloc[i]+0.2, 
                 y=merged.Obesity_Prevalence_pct.iloc[i], 
                 s=merged.Country.iloc[i], 
                 fontdict=dict(color='black', size=9))
                 
    plt.title('Figure 2a: Gym Membership Rate vs. Obesity Levels', fontsize=14)
    plt.xlabel('Gym Penetration (%)')
    plt.ylabel('Obesity Prevalence (%)')
    plt.grid(True)
    plt.savefig(config.FIG_GYM_OBESITY)
    plt.close()
    
    # Figure 2b: Boxplot
    print("Generating Figure 2b (Boxplot)...")
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=merged, x='Gym_Group', y='Obesity_Prevalence_pct', palette='Set2')
    plt.title(f'Figure 2b: Obesity Rates by Gym Usage Group (P={p_val:.3f})', fontsize=14)
    plt.ylabel('Obesity Prevalence (%)')
    plt.savefig(config.FIG_GYM_OBESITY.replace('.png', '_boxplot.png'))
    plt.close()

    # 6. Correlation
    if len(merged) > 2:
        corr, p_val_corr = stats.pearsonr(merged['Gym_Penetration_pct'], merged['Obesity_Prevalence_pct'])
        print(f"Gym Penetration vs Obesity (Correlation N={len(merged)}):")
        print(f"   - Correlation: {corr:.4f}, P-value: {p_val_corr:.4e}")
