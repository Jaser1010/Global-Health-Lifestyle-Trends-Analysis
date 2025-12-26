import pandas as pd
import matplotlib.pyplot as plt
from common import config
from common import data_loader

def run():
    print("\n--- Question 1: COVID Search Trends (Enhanced) ---")
    
    # 1. Fetch Data (now fetches both keywords)
    data_loader.fetch_google_trends()
    
    # 2. Load Data
    try:
        trends_df = pd.read_csv(config.FILE_TRENDS)
        if 'date' in trends_df.columns:
            trends_df['date'] = pd.to_datetime(trends_df['date'])
            trends_df.set_index('date', inplace=True)
    except FileNotFoundError:
        print("Error: Trends data file not found.")
        return

    # 3. Analyze/Plot
    print("Generating Figure 3 (Comparative Trends)...")
    plt.figure(figsize=(12, 6))
    
    if not trends_df.empty and 'home_workout' in trends_df.columns and 'gym_membership' in trends_df.columns:
        # Plot Home Workout
        plt.plot(trends_df.index, trends_df['home_workout'], color='teal', linewidth=2, label='Home Workout')
        # Plot Gym Membership
        plt.plot(trends_df.index, trends_df['gym_membership'], color='orange', linewidth=2, label='Gym Membership')
        
        plt.axvline(pd.to_datetime('2020-03-11'), color='red', linestyle='--', label='Pandemic Declared')
        plt.title('Figure 3: Search Interest - "Home Workout" vs "Gym Membership" (2018-2024)', fontsize=14)
        plt.ylabel('Relative Search Interest')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(config.FIG_TRENDS)
        plt.close()
        print(f"Saved to {config.FIG_TRENDS}")
        
        # Calculate Correlation
        corr = trends_df['home_workout'].corr(trends_df['gym_membership'])
        print(f"Correlation between 'Home Workout' and 'Gym Membership': {corr:.4f}")
        
    else:
        print("Warning: Trends dataframe missing expected columns.")
