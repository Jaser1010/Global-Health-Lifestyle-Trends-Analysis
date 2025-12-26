# Global Health & Lifestyle Trends Analysis

A data science project analyzing the impact of lifestyle choices on health outcomes using real-world data (Google Trends, World Bank, FAOSTAT).

## Structure

The project is divided into three analysis modules:

* `common/`: Shared data loaders and configuration.
* `q1_trends/`: COVID-19 Search Trends analysis.
* `q2_sugar_diabetes/`: Sugar vs Diabetes analysis.
* `q3_gym_obesity/`: Gym Penetration vs Obesity analysis.

## Setup

1. **Install Dependencies:**

    ```bash
    pip install pandas matplotlib seaborn scipy pytrends wbgapi lxml
    ```

2. **Data:**
    * The code automatically attempts to fetch/scrape data.
    * If API limits are hit, it falls back to placeholder CSVs or requires manual CSV placement in `data/`.

## How to Run

To run the full analysis and generate all figures:

```bash
python main.py
```

## Output

* **Figures:** Saved in `figures/`
* **Data:** Processed CSVs saved in `data/`
* **Report:** See `REPORT.md` for the full analysis and conclusions.
