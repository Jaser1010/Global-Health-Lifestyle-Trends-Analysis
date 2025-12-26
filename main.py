# -*- coding: utf-8 -*-
"""
Main Execution Script
---------------------
Runs the analysis for each question module sequentially.
"""
from q1_trends import analyze as q1
from q2_sugar_diabetes import analyze as q2
from q3_gym_obesity import analyze as q3
import warnings

# Suppress minor warnings for cleaner output
warnings.filterwarnings('ignore')

def main():
    print("Starting Global Health & Lifestyle Trends Analysis...")
    
    # Question 1: COVID Search Trends
    q1.run()
    
    # Question 2: Sugar vs Diabetes
    q2.run()
    
    # Question 3: Gym vs Obesity
    q3.run()
    
    print("\nAll analyses complete.")

if __name__ == "__main__":
    main()
