
import os
import glob
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, export_text

def load_data(data_dir):
    """Loads and aggregates all CSV files from the directory."""
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in {data_dir}")
        return None
        
    print(f"Loading {len(all_files)} files from {data_dir}...")
    
    # Use a generator/iterator approach if memory is an issue, but for <20k files of 100 rows, 
    # it might fit in memory. Let's try loading all.
    df_list = []
    for f in all_files:
        try:
            df = pd.read_csv(f)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if not df_list:
        return None
        
    return pd.concat(df_list, ignore_index=True)

def run_modeling(df):
    """Runs the 3 requested ML models."""
    
    # 1. Prep Data
    feature_cols = ['coop_rate', 'first_move_c', 'provocability', 'retaliation_rate', 'forgiveness_rate']
    target_col = 'Median_score'
    
    # Drop rows with missing features or target
    df_clean = df.dropna(subset=feature_cols + [target_col])
    
    X = df_clean[feature_cols]
    y = df_clean[target_col]
    
    print(f"\nData Shape for Modeling: {X.shape}")
    
    # --- MODEL 1: LINEAR REGRESSION ---
    print("\n" + "="*40)
    print("MODEL 1: LINEAR REGRESSION (Global Weights)")
    print("="*40)
    
    lr = LinearRegression()
    lr.fit(X, y)
    
    coeffs = pd.Series(lr.coef_, index=feature_cols)
    coeffs_sorted = coeffs.sort_values(key=abs, ascending=False)
    
    print("\nFeature Coefficients (sorted by magnitude):")
    print(coeffs_sorted)
    
    print("\nInterpretation:")
    nasty_features = ['provocability', 'retaliation_rate']
    nice_features = ['coop_rate', 'forgiveness_rate', 'first_move_c']
    
    positive_impact = coeffs[coeffs > 0].index.tolist()
    negative_impact = coeffs[coeffs < 0].index.tolist()
    
    print(f"Features that INCREASE Score: {positive_impact}")
    print(f"Features that DECREASE Score: {negative_impact}")

    # --- MODEL 2: DECISION TREE ---
    print("\n" + "="*40)
    print("MODEL 2: DECISION TREE (Rule Extraction)")
    print("="*40)
    
    dt = DecisionTreeRegressor(max_depth=3, random_state=42)
    dt.fit(X, y)
    
    tree_rules = export_text(dt, feature_names=feature_cols)
    print("\nDecision Tree Rules:")
    print(tree_rules)
    
    return

def main():
    processed_dir = r"processed_data"
    
    # 1. Load
    df = load_data(processed_dir)
    
    if df is not None:
        # 2. Run Models
        run_modeling(df)

if __name__ == "__main__":
    main()
