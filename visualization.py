
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor

sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12})

def load_data(data_dir):
    """Loads and aggregates all CSV files from the directory."""
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in {data_dir}")
        return None
        
    print(f"Loading {len(all_files)} files from {data_dir}...")
    
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

def plot_feature_importance(df, feature_cols, target_col):
    """Viz 1: Random Forest Feature Importance"""
    print("Generating Feature Importance Plot...")
    
    df_clean = df.dropna(subset=feature_cols + [target_col])
    X = df_clean[feature_cols]
    y = df_clean[target_col]
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importances, x='Importance', y='Feature', palette='viridis')
    plt.title('Feature Importance: What Drives the Score?', fontsize=16)
    plt.xlabel('Relative Importance')
    plt.ylabel('Behavioral Feature')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300)
    plt.close()
    print("Saved feature_importance.png")

def plot_winner_loser_comparison(df, feature_cols, target_col):
    """Viz 3: Top 10% vs Bottom 10% Profile"""
    print("Generating Winner vs Loser Comparison...")
    
    df_clean = df.dropna(subset=feature_cols + [target_col])
    
    # Define thresholds
    top_threshold = df_clean[target_col].quantile(0.90)
    bottom_threshold = df_clean[target_col].quantile(0.10)
    
    winners = df_clean[df_clean[target_col] >= top_threshold][feature_cols].mean()
    losers = df_clean[df_clean[target_col] <= bottom_threshold][feature_cols].mean()
    
    # Prepare data for plotting
    comparison_df = pd.DataFrame({
        'Feature': feature_cols,
        'Winners (Top 10%)': winners,
        'Losers (Bottom 10%)': losers
    })
    
    comparison_melted = comparison_df.melt(id_vars='Feature', var_name='Group', value_name='Average Value')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=comparison_melted, x='Feature', y='Average Value', hue='Group', palette=['gold', 'grey'])
    
    plt.title('Strategy DNA: Winners vs. Losers', fontsize=16)
    plt.xlabel('Behavioral Feature')
    plt.ylabel('Average Rate (0-1)')
    plt.ylim(0, 1)
    plt.legend(title='Performance Group')
    plt.tight_layout()
    plt.savefig('comparison.png', dpi=300)
    plt.close()
    print("Saved comparison.png")

def main():
    processed_dir = r"processed_data"
    
    # 1. Load Data
    df = load_data(processed_dir)
    
    if df is not None:
        feature_cols = ['coop_rate', 'first_move_c', 'provocability', 'retaliation_rate', 'forgiveness_rate']
        target_col = 'Median_score'
        
        # 2. Generate Plots
        plot_feature_importance(df, feature_cols, target_col)
        plot_heatmap(df)
        plot_winner_loser_comparison(df, feature_cols, target_col)
        print("\nAll visualizations completed.")

if __name__ == "__main__":
    main()
