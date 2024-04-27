import pandas as pd
from scipy import stats
import numpy as np

class DataProcessor:
    def __init__(self):
        self.dft = pd.DataFrame()

    def preprocess_numerical_data(self, df):
        # Fill missing values with mean for numerical columns
        
        
        numerical_columns = df.select_dtypes(include=['float'])
        for col in numerical_columns:
            df[col] = df[col].fillna(df[col].mean())
        return df

    def preproccess_categorical_data(self, df):
        df=df.replace('undefined',np.nan)
        categorical_cols = df.select_dtypes(exclude=['float']).columns
        mode_values = df[categorical_cols].mode().iloc[0]
        df.loc[:, categorical_cols] = df[categorical_cols].fillna(mode_values)
        return df
    
    

    def remove_outliers_zscore(self, df, z_threshold=3):
        
        """
        Remove outliers from a DataFrame using Z-scores.
        
        Parameters:
        - df: pandas DataFrame
            Input DataFrame containing numerical columns.
        - z_threshold: float, optional (default=3)
            Z-score threshold to identify outliers.
            
        """
        
        # Select numerical columns
        numerical_cols = df.select_dtypes(include=['float']).columns
        
        # Calculate Z-scores
        z_scores = stats.zscore(df[numerical_cols])
        abs_z_scores = np.abs(z_scores)
        
        # Create boolean mask to filter outliers
        filtered_entries = (abs_z_scores < z_threshold).all(axis=1)
        
        # Update DataFrame by keeping only non-outlier rows
        df_clean = df[filtered_entries]
        
        return df_clean
    
    
    
    def euclidean_distance(x1, x2):
        return np.sqrt(np.sum((x1 - x2) ** 2))
