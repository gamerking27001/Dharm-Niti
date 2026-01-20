import os
import pandas as pd
import numpy as np
import glob

def calculate_features(df):
    """
    Calculates behavioral features for a given DataFrame.
    """

    df['coop_rate'] = df['Cooperation_rating']


    df['first_move_c'] = df['Initial_C_rate']

    #  provocability
    opp_coop_prob = df['CC_rate'] + df['DC_rate']
    prob_defect_given_opp_c = (
        (1 - df['CC_to_C_rate']) * df['CC_rate'] + 
        (1 - df['DC_to_C_rate']) * df['DC_rate']
    )
   
    df['provocability'] = np.where(opp_coop_prob > 0, prob_defect_given_opp_c / opp_coop_prob, 0.0)

    #  retaliation_rate
    opp_defect_prob = df['CD_rate'] + df['DD_rate']
    prob_defect_given_opp_d = (
        (1 - df['CD_to_C_rate']) * df['CD_rate'] + 
        (1 - df['DD_to_C_rate']) * df['DD_rate']
    )
    df['retaliation_rate'] = np.where(opp_defect_prob > 0, prob_defect_given_opp_d / opp_defect_prob, 0.0)

    #  forgiveness_rate
    df['forgiveness_rate'] = df['DC_to_C_rate']

  
    features_to_clean = ['provocability', 'retaliation_rate', 'forgiveness_rate', 'coop_rate', 'first_move_c']
    df[features_to_clean] = df[features_to_clean].fillna(0.0)
    df[features_to_clean] = df[features_to_clean].clip(0.0, 1.0)

  
    df['Median_score'] = pd.to_numeric(df['Median_score'], errors='coerce')
    df = df.dropna(subset=['Median_score'])
    
    return df

def load_and_process_data(data_dir, output_dir):
    """
    Loads CSV files, processes them individually, samples 100 rows, and saves them.
    Returns a sample of the processed data for analysis.
    """
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not all_files:
        print(f"No CSV files found in {data_dir}")
        return None

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    summary_dfs = []
    
    print(f"Processing {len(all_files)} files...")
    
    for filename in all_files:
        try:
         
            df = pd.read_csv(filename)
            
            
            basename = os.path.basename(filename)
            noise_level_str = os.path.splitext(basename)[0]
            if noise_level_str.isdigit():
                 df['Noise_Level'] = int(noise_level_str)
            else:
                 df['Noise_Level'] = np.nan

            df = calculate_features(df)

            if len(df) > 100:
                df = df.sample(n=100, random_state=42)
            
            # Save INDIVIDUAL processed file
            output_path = os.path.join(output_dir, basename)
            df.to_csv(output_path, index=False)
            
        
            summary_dfs.append(df)
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    if not summary_dfs:
        return None

    print(f"Successfully saved individual processed files to {output_dir}")

    return pd.concat(summary_dfs, ignore_index=True)

def main():
    raw_data_path = r"c:\Users\malik\Downloads\Dharma_Niti\raw_data\noise-data"
    output_dir = "processed_data"
    
    print(f"Loading data from: {raw_data_path}")
    
    df = load_and_process_data(raw_data_path, output_dir)
    
    if df is not None:
        print("\n--- Processed Sample Head (from aggregated results) ---")
        print(df[['Name', 'coop_rate', 'first_move_c', 'provocability', 'retaliation_rate', 'forgiveness_rate', 'Median_score']].head())
        
        print("\n--- Correlation Matrix (Features vs Score) ---")
        correlation_cols = ['coop_rate', 'first_move_c', 'provocability', 'retaliation_rate', 'forgiveness_rate', 'Median_score']
        corr_matrix = df[correlation_cols].corr()
        print(corr_matrix)

if __name__ == "__main__":
    main()
